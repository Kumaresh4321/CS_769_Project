# CS 769 Project: Multi-LLM Routing on Use Case and User Preferences
### Members: Abhijnya Menakur, Kumaresh Suresh Babu, and Kincannon Wilson

Our project is titled “**Multi-LLM Routing on Use Case and User Preferences**”. This project will be an extension to the paper “**RouterBench: A Benchmark for Multi-LLM Routing System**”. Our members are Abhijnya Menakur, Kumaresh Suresh Babu, and Kincannon Wilson. 


## Project Overview

This project introduces a dynamic routing system to direct user prompts to the most suitable Large Language Model (LLM) based on user-defined preferences such as cost, latency, and performance. It builds on existing benchmarks and incorporates advanced routing mechanisms to support both text and multimodal applications. The system automates model selection while balancing trade-offs efficiently, democratizing access to state-of-the-art AI capabilities.

## Process

- **Prompt Analysis**: Each user prompt is processed to generate a concise task description.
- **Task Embedding**: Task descriptions are converted into embeddings using lightweight models like MiniLM or DistilBERT.
- **kNN-based Routing**: Prompt embeddings or response embeddings are matched using cosine similarity to determine the best-performing models.
- **Clustering for Scalability**: K-Means clustering groups task embeddings, reducing the computational cost of model selection.
- **Embedding Differences**: Captures task-specific details by calculating differences between response embeddings and prompt embeddings.
- **Dynamic Updates**: The system adapts to new tasks or user preferences by re-ranking models based on evaluation metrics.

## LLM Ranking Methodology

1. **Dataset**: A refined prompt dataset of 1,000 prompts spanning text, image, video, and audio tasks.
2. **Model Evaluation**: Models (e.g., Claude-2, GPT-3.5-turbo, GPT-4, Mixtral-8x7B) are tested for each task.
3. **Judge Model**: Outputs are evaluated using a judge model (e.g., GPT-4) to assess performance.
4. **Human Ratings**: Results are validated against human preferences to ensure alignment.

The router uses these rankings to make cost-effective, accurate, and latency-aware decisions.

## Key Features

- **Adaptive Model Selection**: The system selects the best-performing model based on task requirements.
- **Task-Aware Routing**: Task embeddings improve routing decisions by capturing semantic context.
- **Multimodal Support**: Extends routing capabilities to images, videos, and audio.
- **Cost-Performance Trade-offs**: Supports user-defined criteria for balancing price, latency, and accuracy.

## Results

- Refined a dataset of 1,000 prompts covering 25 distinct tasks.
- Achieved 83.32% routing accuracy using kNN with embeddings.
- Demonstrated significant cost reductions using K-Means clustering.
- Validated embedding differences as a noise-resilient method for routing.
- Enhanced dynamic routing capabilities through task-aware embeddings.

---

# Implementation Guide for Multi-LLM Routing

## Prerequisites

Before starting, ensure you have the following installed on your system:

- Python 3.8 or above
- pip (Python package installer)

## Installation

1. **Clone or Download the Repository**

   - If you have not already, download the project files and extract them to a desired directory on your machine.

2. **Navigate to the Project Directory**

   ```bash
   cd path/to/project_code
   ```

3. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scriptsctivate`
   ```

   Ensure that the virtual environment is created using a compatible Python version (3.8 to 3.11). If you are using Python 3.12 and encounter compatibility issues, consider using an earlier version like Python 3.10. You can install a specific Python version and point the virtual environment to it:

   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**

   All required Python packages are listed in the `requirements.txt` file. Install them using:

   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

Here is an overview of the key files and their purposes:

- `clean_data.py`: Cleans and preprocesses raw data for further processing.
- `embeddings.py`: Generates and manages embeddings for tasks or data.
- `router.py`: Core logic for routing prompts to the optimal model.
- `utils.py`: Utility functions used across the project.
- `mlp_model.py` and `mini_lm_model.py`: Machine learning models used in the routing system.
- **Experiment Scripts**: Various experimental approaches to evaluate and refine the routing mechanism.
- `tasks.json`: Sample input file defining tasks with 1,000 different prompts across text, image, video, and audio modalities.
- `best_model.py`: Chooses the best model based on user preferences and performance metrics.
- Files like `add_embeddings_to_df.py`, `add_flan_to_df.py`, `add_task_to_df.py`: Scripts for manipulating data and adding features to datasets.
- `requirements.txt`: Lists all Python dependencies.
- `README.md`: Describes the project overview and implementation details.

## Running the Code

### Step 1: Prepare the Data

Ensure the required data files are present in the project directory. Use `clean_data.py` to preprocess your raw data:

```bash
python clean_data.py
```

### Step 2: Add Features to Dataset

Run the following scripts to manipulate datasets and add necessary features:

- To add embeddings:
  ```bash
  python add_embeddings_to_df.py
  ```
- To add FLAN model outputs:
  ```bash
  python add_flan_to_df.py
  ```
- To add tasks to the dataset:
  ```bash
  python add_task_to_df.py
  ```

### Step 3: Add Task Embeddings

Generate embeddings for the tasks using:

```bash
python add_task_embedding.py
```

### Step 4: Choose the Best Model

Use `best_model.py` to select the optimal model for your tasks based on the provided dataset and user-defined preferences:

```bash
python best_model.py
```

### Step 5: Run Experiments

Run specific experimental scripts to analyze routing performance. For example:

```bash
python exp1_topk_similarity.py
```

You can explore other experiments like clustering (`exp2_cluster_similarity.py`) or predictive models (`exp5_predict_output.py`).

### Step 6: Execute the Router

The main routing logic is implemented in `router.py`. **Make sure to set your own LLM API key before running the script**. The API key can be configured in `utils.py` at the following line:

```python
headers={
    "Authorization": "Bearer YOUR_LLM_API_KEY"
}
```
Replace YOUR_LLM_API_KEY with your valid API key for the respective LLM provider (e.g., OpenAI, Hugging Face, Anthropic).
Run this script to analyze and route prompts:
```python
python router.py
 ```


### Step 7: Visualize Results (Optional)

The `plotting.ipynb` notebook can be used to visualize results. Open it in Jupyter Notebook or Jupyter Lab:

```bash
jupyter notebook plotting.ipynb
```

## Notes

- Ensure all paths to data files and models are correctly set in the scripts.
- Replace all placeholder API keys with your own LLM API key where applicable.
- For any new dependencies or functionality, update `requirements.txt` and re-install.

## Troubleshooting

- **Missing Dependencies**: If you encounter an error about a missing package, ensure `requirements.txt` is up to date and run `pip install -r requirements.txt`.
- **Data Issues**: Verify that all required data files are present and properly formatted.
- **API Key Errors**: If you encounter issues with API access, ensure your API key is correctly configured in the relevant scripts.

For further assistance, refer to the original `README.md` file or contact the project maintainers.
