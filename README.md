# Plagiarism Detection System

A Python-based text similarity detection system that compares multiple documents using TF-IDF and Cosine Similarity.

## Features

- Upload multiple text documents
- Calculate similarity percentages
- Classify similarity as Low, Moderate, or High
- View results in a table
- Download results as a CSV file

## How It Works

1. Documents are uploaded by the user.
2. Text is converted into TF-IDF vectors.
3. Cosine Similarity is calculated between document pairs.
4. Similarity scores are converted into percentages.
5. Results are classified using the following thresholds:

- Below 15% → Low similarity
- 15% to below 24% → Moderate similarity
- 24% or above → High similarity

## Technologies Used

- Python
- Pandas
- Scikit-learn
- Streamlit

## Important Note

This project measures textual similarity. A high similarity score does not by itself prove plagiarism. The classification thresholds are project-specific and are intended for demonstration.
