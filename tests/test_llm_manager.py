
from backend.llm.llm_manager import OllamaManager


def test_llm_manager():

    print("\n--- TESTING OLLAMA MANAGER ---")

    # 1. Create manager
    manager = OllamaManager()

    print("\n1. Initial AI Status:")
    print("AI Enabled:", manager.enabled)

    assert manager.enabled is False

    # 2. Enable AI
    print("\n2. Enabling AI:")

    message = manager.enable()

    print(message)
    assert manager.enabled is True

    # 3. Generate response
    print("\n3. Generating AI Response:")

    prompt = """
    Explain a double bottom pattern in the stock market
    in simple words. Also explain how it is confirmed.
    """

    response = manager.generate_response(prompt)

    print("\nAI RESPONSE:")
    print(response)

    assert isinstance(response, str)
    assert len(response) > 0

    # 4. Disable AI
    print("\n4. Disabling AI:")

    message = manager.disable()

    print(message)
    assert manager.enabled is False

    # 5. Verify disabled state
    print("\n5. Testing Disabled State:")

    try:
        manager.generate_response("Explain stock patterns.")

    except RuntimeError as e:
        print("Expected error:", e)

    else:
        raise AssertionError(
            "AI generated a response even though it was disabled."
        )

    print("\nAll LLM Manager tests passed!")


if __name__ == "__main__":
    test_llm_manager()
