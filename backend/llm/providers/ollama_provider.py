
import json

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class OllamaProvider:

    def __init__(
        self,
        model_name="qwen2.5:1.5b-instruct",
        base_url="http://localhost:11434",
        timeout=180
    ):

        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, endpoint, payload=None):

        url = f"{self.base_url}{endpoint}"

        if payload is None:
            request = Request(url, method="GET")

        else:
            data = json.dumps(payload).encode("utf-8")

            request = Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(
                    response.read().decode("utf-8")
                )

        except HTTPError as e:
            error_message = e.read().decode(
                "utf-8", errors="replace"
            )
            raise RuntimeError(
                f"Ollama HTTP error {e.code}: {error_message}"
            )

        except URLError as e:
            raise RuntimeError(
                f"Cannot connect to Ollama: {e.reason}"
            )

    def validate(self):

        response = self._request("/api/tags")

        available_models = [
            model["name"]
            for model in response.get("models", [])
        ]

        if self.model_name not in available_models:
            raise RuntimeError(
                f"Model {self.model_name} is not installed."
            )

        return True

    def generate_response(self, prompt):

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        response = self._request(
            "/api/chat",
            {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "keep_alive": "5m",
                "options": {
                    "temperature": 0.2
                }
            }
        )

        return response["message"]["content"]

    def unload(self):

        self._request(
            "/api/generate",
            {
                "model": self.model_name,
                "keep_alive": 0
            }
        )

        return "Ollama model unloaded."
