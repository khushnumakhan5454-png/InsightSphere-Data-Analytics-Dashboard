# align6.py

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio

# Set default template to white so exported images are not black
pio.templates.default = "plotly_white"

def load_data(file):
    return pd.read_csv(file)

def summary(df):
    return df.describe()

def insights(df):
    ins = []
    ins.append(f"Rows: {df.shape[0]}")
    ins.append(f"Columns: {df.shape[1]}")

    for col in df.select_dtypes(include='number').columns:
        ins.append(f"{col} Avg: {round(df[col].mean(),2)}")

    return ins

def recommendations(df):
    rec = []
    rec.append("Focus on high-value features")
    rec.append("Check correlation heatmap")
    rec.append("Handle missing values properly")
    return rec

def create_chart(df, chart_type, x, y, color):
    color_arg = color if color else None

    if chart_type == "Bar":
        return px.bar(df, x=x, y=y, color=color, template="plotly_white")
    elif chart_type == "Line":
        return px.line(df, x=x, y=y, color=color, template="plotly_white")
    elif chart_type == "Area":
        return px.area(df, x=x, y=y, color=color, template="plotly_white")
    elif chart_type == "Histogram":
        return px.histogram(df, x=x, color=color, template="plotly_white")
    elif chart_type == "Pie":
        return px.pie(df, names=x, values=y)
    elif chart_type == "Column":
        return px.bar(df, x=x, y=y, color=color, template="plotly_white")
    else:
        return px.scatter(df, x=x, y=y, color=color, template="plotly_white")

def heatmap(df):
    corr = df.select_dtypes(include='number').corr()
    return px.imshow(corr, text_auto=True, template="plotly_white")

# 🔥 Combine charts into ONE dashboard (fix download issue)
def create_dashboard(bar, line, hist, pie):
    dashboard = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Bar", "Line", "Histogram", "Pie"),
        specs=[[{"type": "xy"}, {"type": "xy"}],
               [{"type": "xy"}, {"type": "domain"}]]
    )

    for t in bar.data:
        dashboard.add_trace(t, row=1, col=1)

    for t in line.data:
        dashboard.add_trace(t, row=1, col=2)

    for t in hist.data:
        dashboard.add_trace(t, row=2, col=1)

    for t in pie.data:
        dashboard.add_trace(t, row=2, col=2)

    # Fix: white background so PNG export is not black
    dashboard.update_layout(
        height=800,
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black")
    )
    return dashboard
