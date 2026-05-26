import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="InsightForge AI",
    layout="wide"
)

st.title("InsightForge AI Dashboard")

st.markdown(
    "### Production-Grade AI Analytics Platform"
)

st.sidebar.header("Dataset Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    st.subheader("Dataset Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_cols) > 0:

        selected_col = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        fig = px.histogram(
            df,
            x=selected_col,
            title=f"Distribution of {selected_col}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig2 = px.line(
            df,
            y=selected_col,
            title=f"Trend Analysis for {selected_col}"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

else:

    st.info(
        "Upload a CSV dataset to begin analytics."
    )