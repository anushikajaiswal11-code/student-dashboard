import streamlit as st;
import pandas as pd;
import plotly.express as px;
import sqlite3;

# Set page configuration
st.set_page_config(
    page_title="Practice Data",
    page_icon="📊",
    layout="centered"
)
# Title
st.title("📊 Practice Data chart")

def init_db():
    conn = sqlite3.connect('practice_data.db')
    return conn

def save_to_db(df):
    conn = init_db()
    df.to_sql('practice', conn, if_exists='replace', index=False)
    conn.close()

def load_from_db():
    conn = init_db()
    df = pd.read_sql('SELECT * FROM practice', conn)
    conn.close()
    return df

def create_dataset():
    data = {
        'Fruit': ['Apple', 'Banana', 'Orange', 'Grapes', 'Mango'] * 20,
        'Category': ['A', 'B', 'C', 'D', 'E'] * 20,
        'Quantity': [10, 15, 7, 20, 5] * 20,
        'Price': [1.2, 0.5, 0.8, 2.0, 1.5] * 20
    }
    return pd.DataFrame(data)

# Generate sample data
df = create_dataset()
save_to_db(df)
df = load_from_db()

st.sidebar.header("Navigation")
page = st.sidebar.radio("Choose a page:", ["Data View", "Charts"])
if page == "Data View":
    st.subheader("Data Table")
    st.dataframe(df, hide_index=True)
    st.dataframe(df.describe())

elif page == "Charts":
    chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])
    if chart_type == "Bar Chart":
        st.subheader("Average Sales by Category")
        bar_data = df.groupby('Fruit')['Price'].mean().reset_index()
        st.bar_chart(bar_data.set_index('Fruit'))
    elif chart_type == "Pie Chart":
        st.subheader("Price Distribution by Category (Pie Chart)")
        pie_data = df.groupby('Fruit')['Price'].sum().reset_index()
        fig = px.pie(pie_data, names='Fruit', values='Price', title='Sales Distribution by Category')
        st.plotly_chart(fig)




