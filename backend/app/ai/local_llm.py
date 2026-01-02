import subprocess
import json


class LocalLLM:
    """
    Local LLM adapter using Ollama (free).
    """

    def __init__(self, model: str = "llama3.1"):
        self.model = model

    def generate(self, prompt: str) -> str:
        result = subprocess.run(
            ["ollama", "run", self.model, prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.stdout.strip()
