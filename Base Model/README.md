# CS 769 Project: Multi-LLM Routing on Use Case and User Preferences
### Members: Abhijnya Menakur, Kumaresh Suresh Babu, and Kincannon Wilson

## Base Paper: ROUTERBENCH: A Benchmark for Multi-LLM Routing System
### [Paper](https://arxiv.org/abs/2403.12031) | [Dataset](https://huggingface.co/datasets/withmartian/routerbench)

## Setup process
1. Create .env file in the root directory. With the following variables:
```
CONNECTION_STRING='your mongodb connection string'
```

You can also set the CONNECTION_STRING in your terminal using the following command:
```
export CONNECTION_STRING="your mongodb connection string"  # On macOS/Linux
set CONNECTION_STRING="your mongodb connection string"      # On Windows
```
if you want to use MongoDB as an embedding cache. Our implementation uses MongoDB for an embedding cache.

2. In root directory, run `pip install -e .` to install the packages.

## Running the pipeilne 

The pipeline relies on various command line arguments to specify the configuration. Alternatively, you can specify the 
configuration in a yaml file and pass it to the command line. Example configurations are in the `configs/` directory.

First, if desired, make sure there is a MongoDB instance running that you can connect to. If there is not one, ensure that `local_cache: true` to ensure that 
the code only uses local files for caching. Our results in the report used a MongoDB instance.

Second, run `convert_data.py --config=configs/convert_data.yaml` to process the different data formats into a common format.
    This script can take raw format from `martian-evals` repo, as well as other relevant input formats.

Third, run `evaluate_routers.py --config=configs/evaluate_routers.yaml` to use the processed data to evaluate different routers. It generates a csv file (long format) with the results of the evaluation, and creates an EvaluationCollection containing the results.

Fourth, run `visualize_results.py --config=configs/visualize.yaml` uses the EvaluationCollection to visualize the results in a performance-vs-cost plot.

For these configurations, the paths to the data files will need to be updated to use your local paths. Example files to recreate results from the paper are available on [Hugging Face](https://huggingface.co/datasets/withmartian/routerbench).


## Contribution Guide

The code is designed to be easily extended. To add a new router, or convertor for a different input data format, simply look
at the abstract classes `AbstractRouter` and `AbstractConvertor` in `routers/` and `convertors/` respectively.

- For each PR, please run flake8, black, isort
```bash
flake8 $(git ls-files '*.py')
black $(git ls-files '*.py')
isort $(git ls-files '*.py')
```
`$(git ls-files '*.py')` is for running only the files tracked by git, so exclude virtual env files or data files.
You may need to run `pip install flake8 black isort` if you don't have them installed.

## Modal update Guide
To deploy the updated modal app, run the following commands:
```bash
modal deploy modal_router.py
```
