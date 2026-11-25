
from backend.llm.providers.openai_provider import OpenAIProvider


def test_openai_provider():

    print("\n--- TESTING OPENAI PROVIDER ---")

    provider = OpenAIProvider()

    # Test 1: Provider initialization
    print("\n1. Testing provider initialization...")

    assert provider.client is None

    print("Provider initialized successfully!")
    print("Model:", provider.model_name)

    # Test 2: Check missing API key
    print("\n2. Testing missing API key...")

    try:
        provider.validate()

    except RuntimeError as e:
        print("Expected message:", e)

    else:
        raise AssertionError(
            "Expected missing API key error."
        )

    # Test 3: Verify no client was created
    assert provider.client is None

    print("\nAll OpenAI Provider tests passed!")


if __name__ == "__main__":
    test_openai_provider()
