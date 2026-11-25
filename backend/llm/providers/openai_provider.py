
import os
from openai import OpenAI


class OpenAIProvider:

    def __init__(self, model_name=None):

        self.model_name = (
            model_name
            or os.getenv("OPENAI_MODEL", "gpt-5.5")
        )

        # Client will be created only when needed.
        self.client = None

    def validate(self):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OpenAI API key is missing. "
                "Configure OPENAI_API_KEY when you are ready."
            )

        self.client = OpenAI(api_key=api_key)

        return True

    def generate_response(self, prompt):

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        # Initialize client only when an API key is available.
        if self.client is None:
            self.validate()

        try:

            response = self.client.responses.create(
                model=self.model_name,

                instructions=(
                    "You are an assistant for a stock market "
                    "analysis application. Explain information "
                    "accurately. Never invent stock data or "
                    "guarantee future market performance. "
                    "A double bottom is generally bullish and "
                    "is normally confirmed by a breakout above "
                    "the neckline."
                ),

                input=prompt
            )

            return response.output_text

        except Exception as e:
            raise RuntimeError(
                f"OpenAI response generation failed: {e}"
            )
