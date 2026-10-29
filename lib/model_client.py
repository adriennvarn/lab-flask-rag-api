import requests

import ollama

DEFAULT_MODEL_NAME = "llama3.2"
DEFAULT_BASE_URL = "http://localhost:11434"


class ModelClientError(Exception):
    """Raised when the local model service cannot return a usable answer."""


def generate_answer(prompt, model_name=DEFAULT_MODEL_NAME, base_url=DEFAULT_BASE_URL):
    """Send the prompt to a local Ollama model and return the generated answer."""
    
    prompt = prompt.strip()
    if not prompt:
        raise ModelClientError("Prompt cannot be empty.")
    
    url = f"{base_url}/api/generate"
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
    except requests.RequestException as err:
        raise ModelClientError(f"API request failed: {err}")
    
    try:
        data = response.json()
    except ValueError as err:
        raise ModelClientError("Response included invalid JSON.") from err
    
    answer = data.get("response")
    
    if not answer or not answer.strip():
        raise ModelClientError("API returned no text.")
    
    return answer.strip()