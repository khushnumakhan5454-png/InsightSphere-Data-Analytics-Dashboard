import streamlit as st
from align6 import (
    load_data,
    summary,
    insights,
    recommendations,
    create_chart,
    heatmap,
    create_dashboard
)

st.set_page_config(layout="wide")

# Title
st.title("🚀 InsightSphere: Data Analytics Dashboard")

# Upload file
file = st.file_uploader("Upload CSV File", type=["csv"])

if file:
    df = load_data(file)

    # Preview
    st.subheader("Data Preview")
    st.dataframe(df.head())

    # Summary
    st.subheader("Statistical Summary")
    st.dataframe(summary(df))

    # Insights
    st.subheader("Insights")
    for i in insights(df):
        st.write(i)

    # Recommendations
    st.subheader("Recommendations")
    for r in recommendations(df):
        st.write(r)

    # Chart controls
    st.subheader("Create Chart")

    col1, col2, col3 = st.columns(3)

    with col1:
        x = st.selectbox("X-axis", df.columns)

    with col2:
        y = st.selectbox("Y-axis", df.columns)

    with col3:
        color = st.selectbox("Color", [None] + list(df.columns))

    chart_type = st.selectbox(
        "Chart Type",
        ["Bar", "Line", "Area", "Histogram", "Pie", "Column"]
    )

    fig = create_chart(df, chart_type, x, y, color)
    st.plotly_chart(fig, key="main_chart")

    # Heatmap
    st.subheader("Heatmap")
    heat_fig = heatmap(df)
    st.plotly_chart(heat_fig, key="heatmap")

    # Dashboard
    st.subheader("Dashboard")

    bar = create_chart(df, "Bar", x, y, color)
    line = create_chart(df, "Line", x, y, color)
    hist = create_chart(df, "Histogram", x, y, color)
    pie = create_chart(df, "Pie", x, y, color)

    colA, colB = st.columns(2)
    colA.plotly_chart(bar, key="bar")
    colB.plotly_chart(line, key="line")

    colC, colD = st.columns(2)
    colC.plotly_chart(hist, key="hist")
    colD.plotly_chart(pie, key="pie")

    # Download full dashboard
    dashboard = create_dashboard(bar, line, hist, pie)

    # Fix: try PNG export with kaleido; fallback to HTML if kaleido not installed
    try:
        img = dashboard.to_image(format="png")
        st.download_button(
            "⬇️ Download Dashboard (PNG)",
            data=img,
            file_name="dashboard.png",
            mime="image/png"
        )
    except ValueError:
        st.warning("⚠️ Kaleido not installed. Downloading as interactive HTML instead. To enable PNG export run: pip install --upgrade kaleido")
        html_bytes = dashboard.to_html(full_html=True).encode("utf-8")
        st.download_button(
            "⬇️ Download Dashboard (HTML)",
            data=html_bytes,
            file_name="dashboard.html",
            mime="text/html"
        )

    # Download data
    st.download_button(
        "⬇️ Download Data",
        data=df.to_csv(index=False),
        file_name="data.csv",
        mime="text/csv"
    )
