# CS 769 Project: Multi-LLM Routing on Use Case and User Preferences
### Members: Abhijnya Menakur, Kumaresh Suresh Babu, and Kincannon Wilson

Our project is titled “Multi-LLM Routing on Use Case and User Preferences”. This project will be an extension to the paper “RouterBench: A Benchmark for Multi-LLM Routing System”. Our members are Abhijnya Menakur, Kumaresh Suresh Babu, and Kincannon Wilson. 

In addition, five members from the CS 839 course on Foundation Models are also contributing to the project. These members are Yancheng Zhu, Jiawei Zhang, Xinyue Lin, Tianyi Li, Fahad Touseef, and Aydan Bailey.

For this report, Abhijnya conducted the literature survey, Kumaresh reimplemented the RouterBench results, and Kincannon completed the other sections. The five members from 839 did not contribute to the report.

## Project Overview
As API offerings from companies like OpenAI, Google, and Anthropic expand, selecting the best LLM for specific use cases has become increasingly complex. Users face challenges with performance benchmarks, frequent updates, emerging models, and diverse APIs. Existing benchmarks, such as GSM8K for math and MMLU for reasoning, offer insights but are limited and inconsistent across models. Multi-LLM routing systems, like RouterBench, simplify model selection by choosing models based on prompt, cost, and latency, though they still require technical knowledge.

This project aims to create an advanced routing system that automates model selection based on user needs, improving accessibility, efficiency, and adaptability without requiring manual testing. This approach will broaden LLM accessibility, driving innovation and expanding applications across industries.

## Proposed Ideas and Project Plan
1. Create the dataset of tasks
2. Create the list of models including price, latency, and wrapper functions for easily getting their output from an API
3. Create the human rankings for all models for each task
4. Create the prompts for how the judge model will be asked to evaluate models
5. Create a system for ranking models on a specific task based on price/latency/performance. We will create systems based on the win-rate compared to a judge model, pairwise comparison, and single comparison.
6. Decide on metric(s) for comparing ranking similarity (potential options include Intersection Count, Jaccard Similarity, and others)
7. Run experiments listed in the section above
8. Time permitting, we will begin to work on methods for efficient updates following changes to user prompts, user preferences, or model cost/latency/performance 

The work will be evenly divided among the group members. Please note that this report details all of the potential ideas we have for our presentation and project and that we may not be able to work on all of them within the time constraints of the course.
