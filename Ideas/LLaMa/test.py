# Use a pipeline as a high-level helper
from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")
pipe(messages)

#Note: I wouldn't recomend this model as it requires 2 GB for PyTorch + 5GB for model itself