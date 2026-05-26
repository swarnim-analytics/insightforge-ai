import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests

OLLAMA_URL = "http://ollama:11434/api/generate"


def generate_ai_summary(dataframe):

    sample_data = dataframe.head(5).to_string()

    prompt = f"""
    Analyze this dataset.

    Dataset shape:
    {dataframe.shape}

    Columns:
    {list(dataframe.columns)}

    Sample rows:
    {sample_data}

    Give:
    - key insights
    - trends
    - anomalies
    - business observations

    Keep response under 100 words.
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
            timeout=300
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

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_cols) > 0:

            metric_cols = st.columns(
                min(3, len(numeric_cols))
            )

            for i, col in enumerate(numeric_cols[:3]):

                metric_cols[i].metric(
                    col,
                    f"{df[col].sum():,.2f}"
                )

        st.subheader("Trend Analysis")

        if len(numeric_cols) > 0:

            selected_trend_col = st.selectbox(
                "Select Trend Column",
                numeric_cols,
                key="trend_select"
            )

            x_axis = df.columns[0]

            fig = px.line(
                df,
                x=x_axis,
                y=selected_trend_col,
                markers=True,
                title=f"{selected_trend_col} Trend"
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
                nbins=20,
                title=f"{selected_col} Distribution"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            fig3 = px.box(
                df,
                y=selected_col,
                title=f"{selected_col} Box Plot"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

    with tab3:

        st.subheader("Dataset Preview")

        st.dataframe(df)

        st.subheader("Dataset Information")

        st.write(df.describe(include="all"))

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