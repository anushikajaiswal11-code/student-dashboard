import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Data Visualization Demo",
    page_icon="📊",
    layout="wide"
)

# Title of the app
st.title("📊 Data Visualization with Streamlit")

# Create a sample dataset
@st.cache_data  # This decorator caches the data to improve performance
def create_sample_data():
    np.random.seed(42)
    data = {
        'Product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'] * 20,
        'Category': ['Electronics', 'Clothing', 'Food', 'Books', 'Sports'] * 20,
        'Sales': np.random.randint(100, 1000, 100),
        'Rating': np.random.uniform(1, 5, 100).round(1)
    }
    return pd.DataFrame(data)

# Function to initialize SQLite database
def init_db():
    conn = sqlite3.connect('sales_data.db')
    return conn

# Function to save DataFrame to SQLite
def save_to_db(df):
    conn = init_db()
    df.to_sql('sales', conn, if_exists='replace', index=False)
    conn.close()

# Function to load data from SQLite
def load_from_db():
    conn = init_db()
    df = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()
    return df

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Choose a page:", ["Data View", "Charts"])

# Generate sample data
df = create_sample_data()

# Save to database
save_to_db(df)

# Load from database
df = load_from_db()

if page == "Data View":
    st.header("📋 Data Display")
    
    # Display raw data
    st.subheader("Raw Data Display")
    st.dataframe(
        df,
        column_config={
            "Product": "Product Name",
            "Category": "Category",
            "Sales": st.column_config.NumberColumn("Sales ($)", format="$%d"),
            "Rating": st.column_config.NumberColumn("Rating", format="%.1f ⭐")
        },
        hide_index=True,
    )
    
    # Display basic statistics
    st.subheader("Data Statistics")
    st.dataframe(df.describe())

elif page == "Charts":
    st.header("📈 Data Visualization")
    
    # Select visualization type
    chart_type = st.selectbox(
        "Choose a chart type:",
        ["Bar Chart", "Pie Chart", "Histogram","Line Chart", "Scatter Plot"]
    )
    
    if chart_type == "Bar Chart":
        st.subheader("Average Sales by Category")
        bar_data = df.groupby('Category')['Sales'].mean()
        st.bar_chart(bar_data)

    elif chart_type == "Pie Chart":
        st.subheader("Sales Distribution by Category (Pie Chart)")
        pie_data = df.groupby('Category')['Sales'].sum().reset_index()
        fig = px.pie(pie_data, values='Sales', names='Category', title='Sales Distribution by Category')
        st.plotly_chart(fig)

    elif chart_type == "Histogram":
        st.subheader("Sales Distribution (Histogram)")
        fig = px.histogram(df, x='Sales', nbins=30, title='Distribution of Sales')
        st.plotly_chart(fig)

    elif chart_type == "Line Chart":
        st.subheader("Sales and Rating Over Rows (Line Chart)")
        st.line_chart(df[['Sales', 'Rating']])

    elif chart_type == "Scatter Plot":
        st.subheader("Sales vs Rating (Scatter Chart)")
        st.scatter_chart(df[['Sales', 'Rating']])

# Add some explanatory text
with st.expander("ℹ️ About this app"):
    st.markdown("""
    This demo app shows various features of Streamlit:
    - Loading and displaying data in tables
    - Storing data in SQLite database
    - Creating interactive visualizations
    - Using different chart types
    - Implementing a multi-page layout
    """)
