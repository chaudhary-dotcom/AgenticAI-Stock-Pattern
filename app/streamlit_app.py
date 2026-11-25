
import sys
from pathlib import Path

import streamlit as st
import pandas as pd

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Add project root to Python's import path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import backend modules
from backend.agent.graph import build_stock_agent
from backend.analysis_report import create_analysis_report
from app.components.charts import create_pattern_chart
from backend.llm.llm_manager import OllamaManager
from backend.llm.assistant import StockAIAssistant

# Build LangGraph agent
stock_agent = build_stock_agent()

# Initialize LLM manager once per Streamlit session
if "llm_manager" not in st.session_state:
    st.session_state.llm_manager = OllamaManager()

if "ai_enabled" not in st.session_state:
    st.session_state.ai_enabled = False

if "ai_status" not in st.session_state:
    st.session_state.ai_status = "AI is disabled."

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def toggle_ai():

    manager = st.session_state.llm_manager

    if st.session_state.ai_enabled:

        try:
            message = manager.enable()
            st.session_state.ai_status = message

        except Exception as e:
            st.session_state.ai_enabled = False
            st.session_state.ai_status = str(e)

    else:
        message = manager.disable()
        st.session_state.ai_status = message

# Page configuration
st.set_page_config(
    page_title="Stock Pattern Agent",
    page_icon="📈",
    layout="wide"
)


# Application title
st.title("📈 Stock Pattern Agent")

st.write(
    "Upload your stock market data and automatically "
    "detect technical patterns."
)


# Sidebar
st.sidebar.header("Market Data")

st.sidebar.divider()

st.sidebar.subheader("AI Settings")

st.sidebar.checkbox(
    "Enable AI Assistant",
    key="ai_enabled",
    on_change=toggle_ai
)

st.sidebar.caption(st.session_state.ai_status)

st.sidebar.divider()

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)


# Main application
if uploaded_file is not None:

    st.success(f"Uploaded file: {uploaded_file.name}")

    if st.button("Analyze Market Data", type="primary"):

        try:

            # Save uploaded file temporarily
            upload_dir = Path("data/uploads")
            upload_dir.mkdir(parents=True, exist_ok=True)

            file_path = upload_dir / uploaded_file.name

            file_path.write_bytes(uploaded_file.getvalue())
            # Run LangGraph agent
            with st.spinner("Stock Pattern Agent is analyzing market data..."):

                initial_state = {
                    "user_query": "Analyze the uploaded stock market data.",
                    "file_path": str(file_path),
                    "market_data": None,
                    "processing_report": [],
                    "technical_patterns": [],
                    "swing_points": None,
                    "historical_matches": [],
                    "clustered_sequences": [],
                    "cluster_interpretations": {},
                    "final_report": "",
                    "report_path": "",
                    "error": None
                }


                result = stock_agent.invoke(initial_state)
                st.session_state.analysis_result = result

                st.session_state.chat_history = []

            if result.get("error"):
                st.error(f"Agent failed: {result['error']}")
                st.stop()

            # Prepare results for the existing Streamlit interface
            df = result["market_data"]
            patterns = result["technical_patterns"]
            swing_points = result["swing_points"]

            chart = create_pattern_chart(
                df=df,
                patterns=patterns,
                swing_points=swing_points
            )
            st.success("Market analysis completed!")

            # Summary metrics
            st.subheader("Market Summary")

            col1, col2, col3, col4 = st.columns(4)

            bullish_count = sum(
                1 for p in patterns
                if p["Direction"] == "BULLISH"
            )

            bearish_count = sum(
                1 for p in patterns
                if p["Direction"] == "BEARISH"
            )

            with col1:
                st.metric("Total Records", len(df))

            with col2:
                st.metric("Detected Patterns", len(patterns))

            with col3:
                st.metric("Bullish Patterns", bullish_count)

            with col4:
                st.metric("Bearish Patterns", bearish_count)

            # Interactive stock chart
            st.subheader("Stock Price Chart")

            st.plotly_chart(
                chart,
                width="stretch"
            )

            # Detected patterns
            st.subheader("Detected Technical Patterns")

            if patterns:
                pattern_df = pd.DataFrame(patterns)
                st.dataframe(
                    pattern_df,
                    width="stretch"
                )
            else:
                st.info("No technical patterns detected.")

            # Swing points
            st.subheader("Swing Highs and Lows")

            st.dataframe(
                swing_points,
                width="stretch"
            )

            # Data processing report
            st.subheader("Data Processing Report")

            for issue in result["processing_report"]:
                st.write("•", issue)
            # Download LangGraph agent report
            report_path = Path(result["report_path"])
            if report_path.exists():
                st.download_button(
                    label="Download Agent Report",
                    data=report_path.read_bytes(),
                    file_name="stock_analysis_report.txt",
                    mime="text/plain"
                )

        except Exception as e:

            st.error(f"Analysis failed: {e}")

else:

    st.info("Please upload a CSV or Excel stock market file to begin.")

# ==============================
# AI CHAT ASSISTANT
# ==============================
if st.session_state.ai_enabled:

    st.subheader("💬 Stock AI Assistant")

    if st.session_state.analysis_result is None:
        st.info("Please upload a market data file and run analysis first.")

    else:
        st.caption("Ask questions about your stock analysis.")

        # Display previous chat messages
        for message in st.session_state.chat_history:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        user_question = st.chat_input(
            "Ask something about your stock analysis..."
        )

        # Process user's question
        if user_question:

            # Save user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            # Display user message
            with st.chat_message("user"):
                st.markdown(user_question)

            # Generate AI response
            try:

                with st.chat_message("assistant"):

                    with st.spinner("AI is thinking..."):

                        assistant = StockAIAssistant(
                            st.session_state.llm_manager
                        )

                        response = assistant.ask_question(
                            user_question,
                            st.session_state.analysis_result
                        )

                    st.markdown(response)

                # Save AI response
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
            except Exception as e:
                st.error(f"AI Assistant Error: {e}")
