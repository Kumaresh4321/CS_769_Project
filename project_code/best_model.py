import time
import json
import pandas as pd
from utils import (
    MODELS,
    get_model_response,
    compare_model_to_reference,
    get_output_from_response,
)
# Load the averages CSV file
averages_file = 'averages_by_modality_and_category.csv'  # Replace with your file path
averages_df = pd.read_csv(averages_file)

# Available models
models = [
    "anthropic/claude-2",
    "openai/gpt-3.5-turbo-1106",
    "openai/gpt-4-1106-preview",
    "mistralai/mistral-7b-instruct",
    "mistralai/mixtral-8x7b-instruct"
]

# Get user input
def get_user_input():
    print("Available modalities:", averages_df['modality'].unique())
    modality = input("Enter the modality: ").lower()

    print("Available categories:", averages_df['category'].unique())
    category = input("Enter the category: ").lower()

    prompt = input("Enter your prompt: ")

    preferred_latency = float(input("Enter your preferred maximum latency (e.g., 5): "))
    preferred_price = float(input("Enter your preferred maximum price (e.g., 1.5): "))
    preferred_accuracy = float(input("Enter your preferred minimum accuracy (e.g., 0.6): "))

    return modality, category, prompt, preferred_latency, preferred_price, preferred_accuracy

# Suggest the best model
def suggest_best_model(modality, category, preferred_latency, preferred_price, preferred_accuracy,prompt):
    # Filter the data for the specified modality and category
    filtered_df = averages_df[(averages_df['modality'] == modality) & (averages_df['category'] == category)]

    if filtered_df.empty:
        return "No data available for the specified modality and category."

    # Add a ranking column based on priority: price, latency, and accuracy
    for model in models:
        filtered_df[f'{model}_score'] = (
            (filtered_df[f'{model}:price'] <= preferred_price).astype(int) +
            (filtered_df[f'{model}:latency'] <= preferred_latency).astype(int) +
            (filtered_df[f'{model}:human_win_rate'] >= preferred_accuracy).astype(int) +
            (filtered_df[f'{model}:judge_win_rate'] >= preferred_accuracy).astype(int)
        )

    # Find the best model based on the highest score
    best_model = None
    best_score = -1

    for model in models:
        avg_score = filtered_df[f'{model}_score'].mean()
        if avg_score > best_score:
            best_score = avg_score
            best_model = model

    if best_model:
        response = get_model_response(best_model, prompt)
        return f"The best model for your prompt is: {best_model}, with a score of {best_score}. The response is: {response}"
    else:
        return "No suitable model found based on your preferences."

# Main program
def main():
    modality, category, prompt, preferred_latency, preferred_price, preferred_accuracy = get_user_input()
    result = suggest_best_model(modality, category, preferred_latency, preferred_price, preferred_accuracy,prompt)
    print(result)

if __name__ == "__main__":
    main()