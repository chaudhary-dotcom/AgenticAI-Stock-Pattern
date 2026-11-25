
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class OllamaManager:

    def __init__(
        self,
        model_name="qwen2.5:1.5b-instruct",
        base_url="http://localhost:11434",
        timeout=180
    ):
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        # AI is disabled by default.
        self.enabled = False

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
                return json.loads(response.read().decode("utf-8"))

        except HTTPError as e:
            error_message = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"Ollama HTTP error {e.code}: {error_message}"
            )

        except URLError as e:
            raise RuntimeError(
                f"Cannot connect to Ollama: {e.reason}"
            )

    def enable(self):

        # Check Ollama without loading the model.
        response = self._request("/api/tags")

        available_models = [
            model["name"]
            for model in response.get("models", [])
        ]

        if self.model_name not in available_models:
            raise RuntimeError(
                f"Model {self.model_name} is not installed."
            )

        self.enabled = True

        return "AI enabled successfully."

    def disable(self):

        # Disable AI immediately.
        self.enabled = False

        # Ask Ollama to unload the model.
        try:
            self._request(
                "/api/generate",
                {
                    "model": self.model_name,
                    "keep_alive": 0
                }
            )

            return "AI disabled. Model unloaded."

        except RuntimeError as e:
            return f"AI disabled. Model unload status: {e}"

    def generate_response(self, prompt):

        if not self.enabled:
            raise RuntimeError(
                "AI is disabled. Enable AI before generating responses."
            )

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        system_prompt = """
        You are an assistant for a stock market analysis application.

        Follow these rules:

        1. Explain technical concepts accurately.
        2. Never invent stock prices or market data.
        3. Use only the information provided by the user.
        4. Clearly distinguish historical observations from predictions.
        5. Never guarantee future stock performance.
        6. A double bottom is generally a bullish reversal pattern.
        7. A double bottom is normally confirmed by a breakout
           above the neckline.
        8. Do not provide guaranteed buy or sell recommendations.
        """

        response = self._request(
            "/api/chat",
            {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
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
