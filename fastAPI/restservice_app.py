from fastapi import FastAPI
from typing import Dict
import pandas as pd
import numpy as np
import pickle

app = FastAPI()
@app.get("/api/v1/health", summary="Health check", description="Check if the API is up.")
async def get_health_check_status() -> Dict:
    """Generate a health check response for the applications."""
    return {"status": "UP", "details": "Application is running normally."}


# Load data, embeddings, and model
df = pd.read_csv('dataset.csv', low_memory=False, encoding='utf-8')
embedings_matrix = np.load("embeddings_matrix_v1.npy")
with open("bert.pkl", "rb") as f:
    bert = pickle.load(f)
with open("cos_sim.pkl", "rb") as f:
    cos_sim = pickle.load(f)


def get_top_k_matches(searchQuery, k=10):
    search_arr = np.array([searchQuery])
    search_embeddings = bert.encode(search_arr)
    similarity_matrix = cos_sim(search_embeddings, embedings_matrix)
    top_k_ids = np.argsort(similarity_matrix[0])[-k:][::-1]
    responses = []
    for id_ in top_k_ids:
        row = df.iloc[id_]
        answer = {
            "Title": row['Title'],
            "Source": row['Source'],
            "DateOfScrapping": row['DateOfScrapping'],
            "Content": row['Content']
        }
        responses.append(answer)
    return responses


def get_top_match(searchQuery):
    results = get_top_k_matches(searchQuery, k=1)
    result = results[0]
    result_source = result['Source']
    result_content = result['Content'].replace("\n", " ")
    response = "\n".join([result_content, f'<a href="{result_source}">{result_source}</a>', result['Title']])
    return response


@app.get("/api/v1/qa", summary="Question Answers", description="Returns Answer.")
async def qa(prompt):
    response = get_top_match(prompt)
    return response