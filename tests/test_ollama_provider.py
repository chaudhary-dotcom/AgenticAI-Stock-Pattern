
from backend.llm.providers.ollama_provider import OllamaProvider


def test_ollama_provider():

    print("\n--- TESTING OLLAMA PROVIDER ---")

    provider = OllamaProvider()

    # Test 1: Validate Ollama connection and model
    print("\n1. Checking Ollama connection...")

    assert provider.validate() is True

    print("Ollama connection successful!")
    print("Model:", provider.model_name)

    # Test 2: Generate AI response
    print("\n2. Testing AI response generation...")

    prompt = "Explain what a double bottom pattern is in simple words."

    response = provider.generate_response(prompt)

    print("\nAI RESPONSE:")
    print(response)

    assert isinstance(response, str)
    assert len(response) > 0

    # Test 3: Unload model
    print("\n3. Unloading Ollama model...")

    result = provider.unload()

    print(result)

    print("\nAll Ollama Provider tests passed!")


if __name__ == "__main__":
    test_ollama_provider()
