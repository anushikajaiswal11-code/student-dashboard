import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(
    page_title="Student Data Visualization",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Student Data Analysis Dashboard")

# Function to get data from SQLite
@st.cache_data
def load_data():
    conn = sqlite3.connect('students.db')
    query = "SELECT * FROM students"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Load the data
df = load_data()

# Sidebar for filtering
st.sidebar.header("Filters")

# Department filter
selected_dept = st.sidebar.multiselect(
    "Select Department(s)",
    options=df['department'].unique(),
    default=df['department'].unique()
)

# Grade range filter
grade_range = st.sidebar.slider(
    "Grade Range",
    min_value=float(df['grade'].min()),
    max_value=float(df['grade'].max()),
    value=(float(df['grade'].min()), float(df['grade'].max()))
)

# Filter the dataframe
filtered_df = df[
    (df['department'].isin(selected_dept)) &
    (df['grade'].between(grade_range[0], grade_range[1]))
]

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
    # Average Grade by Department (Bar Chart)
    st.subheader("Average Grade by Department")
    dept_grade = filtered_df.groupby('department')['grade'].mean().reset_index()
    fig1 = px.bar(
        dept_grade,
        x='department',
        y='grade',
        title='Average Grade by Department',
        color='department'
    )
    st.plotly_chart(fig1, width='stretch')

    # Grade Distribution (Histogram)
    st.subheader("Grade Distribution")
    fig2 = px.histogram(
        filtered_df,
        x='grade',
        nbins=20,
        title='Grade Distribution',
        color='department'
    )
    st.plotly_chart(fig2, width='stretch')

with col2:
    # Attendance vs Grade (Scatter Plot)
    st.subheader("Attendance vs Grade")
    fig3 = px.scatter(
        filtered_df,
        x='attendance',
        y='grade',
        color='department',
        title='Attendance vs Grade by Department',
        trendline="ols"  # Add trend line
    )
    st.plotly_chart(fig3, width='stretch')

    # Department Distribution (Pie Chart)
    st.subheader("Department Distribution")
    dept_count = filtered_df['department'].value_counts()
    fig4 = px.pie(
        values=dept_count.values,
        names=dept_count.index,
        title='Students by Department'
    )
    st.plotly_chart(fig4, width='stretch')

# Additional Statistics
st.header("📈 Key Statistics")
col3, col4, col5 = st.columns(3)

with col3:
    st.metric(
        "Average Grade",
        f"{filtered_df['grade'].mean():.2f}",
        f"{filtered_df['grade'].mean() - df['grade'].mean():.2f}"
    )

with col4:
    st.metric(
        "Average Attendance",
        f"{filtered_df['attendance'].mean():.1f}%",
        f"{filtered_df['attendance'].mean() - df['attendance'].mean():.1f}%"
    )

with col5:
    st.metric(
        "Total Students",
        len(filtered_df),
        f"{len(filtered_df) - len(df)}"
    )

# Correlation Heatmap using Seaborn
st.header("📊 Correlation Heatmap")
numeric_cols = ['grade', 'attendance', 'age']
correlation = filtered_df[numeric_cols].corr()

# Create a heatmap using Seaborn
plt.figure(figsize=(8, 6)) #creates a blank figure to draw on
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)  #draws the heatmap on that figure
st.pyplot(plt) #displays it in the Streamlit UI

# Data Table
st.header("📋 Detailed Data View")
st.dataframe(
    filtered_df,
    column_config={
        "grade": st.column_config.NumberColumn(
            "Grade",
            format="%.2f",
            help="Student's grade point average"
        ),
        "attendance": st.column_config.NumberColumn(
            "Attendance %",
            format="%.1f%%"
        ),
    },
    hide_index=True
)

# Add download button for filtered data
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    "Download Filtered Data",
    csv,
    "filtered_student_data.csv",
    "text/csv",
    key='download-csv'
)

# About section
with st.expander("ℹ️ About this dashboard"):
    st.markdown("""
    This dashboard provides interactive visualization of student data:
    - Filter data by department and grade range
    - View various charts including bar charts, histograms, scatter plots, and pie charts
    - See key statistics and correlations
    - Download filtered data as CSV
    - Interactive data table with formatted columns
    """)