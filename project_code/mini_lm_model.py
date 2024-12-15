"""
A Mini-LM-L6-v2 model (initialized with default weights) that takes in a prompt
embedding and after training attempts outputs output embedding.

Key changes from what's normal: defines custom CosineLoss so that output of the 
finetuned model matches the output embeddings generated by the normal model. The whole
encoder is trained since the finetuned model encodes the prompt. 
"""

import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from sentence_transformers import SentenceTransformer


class CosineLoss(torch.nn.Module):
    def __init__(self):
        super(CosineLoss, self).__init__()

    def forward(self, predictions, targets):
        """
        Compute the loss as 1 - cosine similarity between predictions and targets.

        Args:
            predictions (torch.Tensor): Predicted embeddings of shape (batch_size, embedding_dim)
            targets (torch.Tensor): Ground truth embeddings of shape (batch_size, embedding_dim)

        Returns:
            torch.Tensor: Mean loss across the batch
        """
        cosine_sim = F.cosine_similarity(predictions, targets, dim=1)
        loss = 1 - cosine_sim  # Cosine distance
        return loss.mean()  # Mean loss over the batch


# Define a custom dataset
class FinetuningDataset(Dataset):
    def __init__(self, prompts: list[str], output_embeddings: np.ndarray):
        self.prompts = prompts
        self.output_embeddings = torch.tensor(output_embeddings, dtype=torch.float32)

    def __len__(self):
        return len(self.prompts)

    def __getitem__(self, idx):
        return self.prompts[idx], self.output_embeddings[idx]


# Define a model for fine-tuning
class EmbeddingFineTuner(nn.Module):
    def __init__(
        self,
        pretrained_model_name="all-MiniLM-L6-v2",
        device="cuda",
        save_path=None,
        output_dim=384,
        hidden_dim=384,
    ):  # hidden_dim was 512
        super(EmbeddingFineTuner, self).__init__()

        if (
            save_path is None
            or not save_path.endswith(".ckpt")
            or os.path.isdir(os.path.isdir(os.path.dirname(save_path)))
        ):
            raise RuntimeError(f"Bad path {save_path=}")
        
        self.save_path = save_path

        # Load the pre-trained MiniLM encoder
        self.encoder = SentenceTransformer(pretrained_model_name).to(device)

        # Transformation layers to map from encoder output to output embedding
        self.fc1 = nn.Linear(384, hidden_dim)  # MiniLM output size is 384
        self.fc2 = nn.Linear(hidden_dim, output_dim)  # Map to the output embedding size

        # Optional: Non-linear activation function (e.g., ReLU)
        self.relu = nn.ReLU()

    def forward(self, x):
        # Get the prompt embedding from the encoder
        x = self.encoder.encode(
            x, convert_to_tensor=True
        )  # Convert input text to tensor
        x = x.unsqueeze(0)  # Add batch dimension if necessary

        # Pass through the transformation layers
        x = self.fc1(x)
        x = self.relu(x)  # Activation after first transformation
        x = self.fc2(x)  # Output transformation to target embedding

        return x


# Define training loop
def train_model(
    model,
    train_dataloader,
    eval_dataloader,
    optimizer,
    criterion,
    epochs=5,
    device="cuda",
    eval_every=10,
    max_evals_without_improvement=5,
):
    model.train()

    # Early stop behavior
    val_losses = []
    evals_without_improvement = 0

    for epoch in range(epochs):
        total_loss = 0.0
        for prompts, output_embeds in train_dataloader:
            output_embeds = output_embeds.to(device)

            # Zero gradients
            optimizer.zero_grad()

            # Forward pass
            predictions = model(prompts)
            loss = criterion(predictions, output_embeds)

            # Backward pass
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        # Evaluation
        if epoch % eval_every == 0:
            val_loss = evaluate_model(model, eval_dataloader, criterion, device)
            if len(val_losses) == 0 or val_loss < min(val_losses):
                val_losses.append(val_loss)
                print(f"Saving. Eval loss: {val_loss:.4f}")
                torch.save(model.state_dict(), model.save_path)
                evals_without_improvement = 0
            else:
                evals_without_improvement += 1
                if evals_without_improvement == max_evals_without_improvement:
                    print(f"Early stop at {max_evals_without_improvement=}.")
                    break

        # Print
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(train_dataloader):.4f}.")


# Define evaluation function
def evaluate_model(model, eval_dataloader, criterion, device="cuda"):
    model.eval()
    total_loss = 0.0
    with torch.no_grad():
        for prompts, output_embeds in eval_dataloader:
            output_embeds = output_embeds.to(device)
            predictions = model(prompts)
            loss = criterion(predictions, output_embeds)
            total_loss += loss.item()
    return total_loss / len(eval_dataloader)