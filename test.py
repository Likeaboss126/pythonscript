import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Load data
df = pd.read_csv("data.csv")
df["DateTime"] = pd.to_datetime(df["DateTime"])

# ---------------------------------
# Streamlit Page Config
# ---------------------------------
st.set_page_config(page_title="API Dashboard", layout="wide")
st.title("🚀 API Response Dashboard")

# ---------------------------------
# Sidebar: Filters and Initialization
# ---------------------------------
with st.sidebar:
    st.header("🔎 Filters")

    # Reset button
    if st.button("🔄 Reset Filters"):
        st.session_state.clear()
        st.rerun()

    # Time range selection
    time_range = st.selectbox(
        "Select Time Range",
        ["All Time", "Last 7 Days", "Last 30 Days", "Last 60 Days", "Last 1 Year"],
        index=1  # Default: Last 7 Days
    )

    # Dropdown values
    all_funcs = sorted(df["Functionality"].unique())
    all_apis = sorted(df["API"].unique())

    # Initialize session state for filters
    if "selected_funcs" not in st.session_state:
        st.session_state.selected_funcs = [all_funcs[0]] if all_funcs else []
    if "selected_apis" not in st.session_state:
        st.session_state.selected_apis = []

    # Filter available API options based on selected functionality
    filtered_apis = df[df["Functionality"].isin(st.session_state.selected_funcs)]["API"].unique()
    filtered_apis = sorted(filtered_apis)

    # Functionality multiselect
    selected_funcs = st.multiselect(
        "Select Functionality",
        options=all_funcs,
        default=None,
        key="selected_funcs"
    )

    # API multiselect (filtered by selected functionality)
    selected_apis = st.multiselect(
        "Select API",
        options=filtered_apis,
        default=None,
        key="selected_apis"
    )

# ---------------------------------
# Filter Data Based on Selections
# ---------------------------------
filtered_df = df.copy()

# Filter by time range
if time_range != "All Time":
    days = int(time_range.split()[1])
    cutoff_date = datetime.now() - timedelta(days=days)
    filtered_df = filtered_df[filtered_df["DateTime"] >= cutoff_date]

# Filter by Functionality and API
if st.session_state.selected_funcs:
    filtered_df = filtered_df[filtered_df["Functionality"].isin(st.session_state.selected_funcs)]
if st.session_state.selected_apis:
    filtered_df = filtered_df[filtered_df["API"].isin(st.session_state.selected_apis)]

# ---------------------------------
# Display Plot
# ---------------------------------
st.subheader("📊 Response Time Over Time")
if not filtered_df.empty:
    fig = px.line(
        filtered_df,
        x="DateTime",
        y="Response Time",
        color="Functionality",
        markers=True,
        title="Response Time Trend"
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Response Time (ms)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for selected filters.")

# ---------------------------------
# Optional: Raw Data Viewer
# ---------------------------------
with st.expander("📄 Show Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)
