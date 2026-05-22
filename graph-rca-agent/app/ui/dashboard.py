import sys
import os

# PATH RESOLUTION: This path-handling block must run before importing any local app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
from app.agent.rca_agent import RCAAgent

st.set_page_config(
    page_title="GraphRCA Agent",
    layout="wide"
)

st.title("GraphRCA — AI Root Cause Analysis Agent")

st.markdown("""
AI-powered software failure diagnosis using:
- Neo4j Knowledge Graph
- Pytest Failure Analysis
- Gemini LLM
- GraphRAG-inspired retrieval
""")

test_name = st.text_input(
    "Test Name",
    value="test_login"
)

error_log = st.text_area(
    "Failure Log",
    value="""AssertionError:
Expected status code 200
Received 500 Internal Server Error"""
)

# Processing pipeline triggered on button action
if st.button("Analyze Failure"):

    with st.spinner("Analyzing failure with Gemini 2.5 + Neo4j..."):
        agent = RCAAgent()
        result = agent.analyze_failure(
            test_name=test_name,
            error_log=error_log
        )

    # Core Metric Output Cards
    st.markdown("---")
    st.subheader("AI RCA Report")

    st.subheader("Root Cause")
    st.error(result["root_cause"])

    st.subheader("Impacted Component")
    st.info(result["impacted_component"])

    st.subheader("Historical Bug")
    st.warning(result["historical_bug"])

    st.subheader("Suggested Fix")
    st.success(result["suggested_fix"])

    st.subheader("Confidence Score")
    st.metric(
        label="AI Confidence",
        value=f'{result["confidence_score"]}%'
    )