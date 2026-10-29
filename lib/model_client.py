import requests

import ollama

DEFAULT_MODEL_NAME = "llama3.2"
DEFAULT_BASE_URL = "http://localhost:11434"

EMBEDDING_MODEL = "embeddinggemma"


class ModelClientError(Exception):
    """Raised when the local model service cannot return a usable answer."""


def generate_answer(prompt, model_name=DEFAULT_MODEL_NAME, base_url=DEFAULT_BASE_URL):
    """Send the prompt to a local Ollama model and return the generated answer."""
    # TODO: Validate that prompt is a non-empty string.
    # TODO: POST to {base_url}/api/generate.
    # TODO: Send model, prompt, and stream=False as JSON.
    # TODO: Use a timeout.
    # TODO: Raise ModelClientError for request failures, bad JSON, or missing response.
    # TODO: Return the stripped response text.
    raise NotImplementedError("Implement generate_answer().")