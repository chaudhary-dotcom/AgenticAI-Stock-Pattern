
from backend.llm.context_builder import build_analysis_context


class StockAIAssistant:

    def __init__(self, llm_manager):
        self.llm_manager = llm_manager

    def ask_question(self, question, analysis_result):

        if not self.llm_manager.enabled:
            raise RuntimeError(
                "AI Assistant is disabled."
            )

        if not question or not question.strip():
            raise ValueError(
                "Please enter a question."
            )

        # Prepare stock analysis context
        context = build_analysis_context(analysis_result)

        # Construct the prompt
        prompt = f"""
You are an intelligent Stock Market Analysis Assistant.

Answer the user's questions using the stock analysis
information provided below.

IMPORTANT RULES:
1. Use the provided analysis data.
2. Do not invent stock prices or patterns.
3. Explain technical concepts in simple language.
4. Clearly distinguish observations from predictions.
5. Never guarantee future stock performance.
6. If information is unavailable, say so.
7. Do not give guaranteed buy or sell recommendations.

STOCK ANALYSIS RESULTS:
{context}

USER QUESTION:
{question}

Provide a clear and beginner-friendly answer.
"""

        # Generate response using the local LLM
        response = self.llm_manager.generate_response(prompt)

        return response
