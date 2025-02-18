from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from transformers import AutoTokenizer, AutoModel, pipeline
import os

app = FastAPI()

class TextInput(BaseModel):
    text: str

class TextBatchInput(BaseModel):
    texts: List[str]

# Global variables for the model and tokenizer
model = None
tokenizer = None
embedder = None

@app.on_event("startup")
async def load_model():
    global model, tokenizer, embedder

    # Get model ID from environment variable or use a default one
    model_id = os.getenv("MODEL_ID", "bert-base-uncased")
    
    try:
        print(f"Loading model: {model_id}")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModel.from_pretrained(model_id)
        print(f"Model path {tokenizer.cache_dir} l")
        embedder = pipeline("feature-extraction", model=model, tokenizer=tokenizer)
        print(f"Model {model_id} loaded successfully!")
    except Exception as e:
        print(f"Failed to load model {model_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load model {model_id}")

@app.post("/embed")
async def embed(input: TextInput):
    global embedder
    if embedder is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        embeddings = embedder(input.text)
        # Pooling logic: Mean pooling across all tokens
        mean_embedding = [float(x) for x in map(lambda x: sum(x) / len(x), zip(*embeddings[0]))]
        return {"embedding": mean_embedding}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate embedding: {str(e)}")

@app.post("/embed-batch")
async def embed_batch(input: TextBatchInput):
    global embedder
    if embedder is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        embeddings_batch = []
        for text in input.texts:
            embeddings = embedder(text)
            # Pooling logic: Mean pooling across all tokens
            mean_embedding = [float(x) for x in map(lambda x: sum(x) / len(x), zip(*embeddings[0]))]
            embeddings_batch.append(mean_embedding)

        return {"embeddings": embeddings_batch}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate embeddings: {str(e)}")
