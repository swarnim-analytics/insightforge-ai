import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

import requests

OLLAMA_URL = "http://ollama:11434/api/generate"


def generate_ai_summary(dataframe):

    prompt = f"""
    Analyze this dataset summary.

    Columns:
    {list(dataframe.columns)}

    Provide:
    - trends
    - anomalies
    - business insights
    - observations

    Keep response concise.
    """

    payload = {
        "model": "phi3:mini",
        "prompt": prompt,
        "stream": False
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        result = response.json()

        return result.get(
            "response",
            "No AI response generated."
        )

    except Exception as e:

        return f"Error: {str(e)}"

st.set_page_config(
    page_title="InsightForge AI",
    layout="wide"
)

st.title("InsightForge AI Dashboard")

st.markdown(
    "### Production-Grade AI Analytics Platform"
)

st.sidebar.header("Dataset Controls")

use_sample = st.sidebar.checkbox(
    "Use Sample Dataset",
    value=True
)

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

df = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)

elif use_sample:

    np.random.seed(42)

    df = pd.DataFrame({
        "Month": pd.date_range(
            start="2025-01-01",
            periods=12,
            freq="ME"
        ),

        "Revenue": np.random.randint(
            1000,
            5000,
            12
        ),

        "Users": np.random.randint(
            100,
            1000,
            12
        ),

        "Orders": np.random.randint(
            50,
            500,
            12
        )
    })

if df is not None:

    tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Analytics",
    "Raw Data",
    "AI Insights"
])

    with tab1:

        st.subheader("Key Metrics")

        col1, col2, col3 = st.columns(3)

        if "Revenue" in df.columns:
            col1.metric(
                "Total Revenue",
                f"${df['Revenue'].sum():,}"
            )

        if "Users" in df.columns:
            col2.metric(
                "Total Users",
                f"{df['Users'].sum():,}"
            )

        if "Orders" in df.columns:
            col3.metric(
                "Total Orders",
                f"{df['Orders'].sum():,}"
            )

        st.subheader("Revenue Trend")

        if "Revenue" in df.columns:

            fig = px.line(
                df,
                x="Month",
                y="Revenue",
                markers=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with tab2:

        st.subheader("Data Distribution")

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_cols) > 0:

            selected_col = st.selectbox(
                "Select Column",
                numeric_cols
            )

            fig2 = px.histogram(
                df,
                x=selected_col,
                nbins=20
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

    with tab3:

        st.subheader("Dataset Preview")

        st.dataframe(df)

    with tab4:

        st.subheader("AI Dataset Insights")

        st.write(
            "Generate AI-powered insights using Ollama."
        )

        if st.button("Generate AI Summary"):

            with st.spinner(
                "Analyzing dataset..."
            ):

                ai_summary = generate_ai_summary(df)

            st.success("Analysis Complete")

            st.write(ai_summary)

else:

    st.warning(
        "Upload a CSV file or use sample dataset."
    )