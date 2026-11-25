from backend.llm.llm_manager import OllamaManager
from backend.llm.assistant import StockAIAssistant


def test_stock_ai_assistant():

    print("\n--- TESTING STOCK AI ASSISTANT ---")

    manager = OllamaManager()

    # Enable local AI
    manager.enable()

    assistant = StockAIAssistant(manager)

    sample_analysis = {
        "market_data": None,
        "technical_patterns": [
            {
                "Pattern": "Double Bottom",
                "Direction": "BULLISH"
            }
        ],
        "swing_points": None,
        "historical_matches": [],
        "cluster_interpretations": {},
        "processing_report": []
    }

    question = "Explain the detected technical pattern."

    print("\nQuestion:", question)

    response = assistant.ask_question(
        question,
        sample_analysis
    )

    print("\nAI RESPONSE:")
    print(response)

    assert isinstance(response, str)
    assert len(response) > 0

    # Disable AI
    manager.disable()

    print("\nStock AI Assistant test passed!")


if __name__ == "__main__":
    test_stock_ai_assistant()