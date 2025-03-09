from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import asyncio

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/embed")
async def embed(input: TextInput):
    await asyncio.sleep(0.1)  # Simulate asynchronous processing
    vector = np.random.rand(128).tolist()  # Generate a random vector of size 128
    return {"vector": vector}
