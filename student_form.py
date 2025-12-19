import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Student Data Collection",
    page_icon="👨‍🎓",
    layout="wide"
)

# Initialize database
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            grade REAL,
            department TEXT,
            attendance REAL,
            interests TEXT,
            submission_date TEXT
        )
    ''')
    conn.commit()
    return conn

# Title and description
st.title("📚 Student Data Collection Form")
st.markdown("Please fill in the following details:")

# Create form
with st.form("student_form"):
    # Text input for name
    name = st.text_input("Student Name", placeholder="Enter full name")
    
    # Two columns for age and grade
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Age", min_value=18, max_value=30, value=20)
    with col2:
        grade = st.slider("Current Grade", min_value=0.0, max_value=4.0, value=3.0, step=0.1)
    
    # Radio button for department
    department = st.radio(
        "Select Department",
        ["Computer Science", "Engineering", "Business", "Arts", "Science"]
    )
    
    # Slider for attendance
    attendance = st.slider(
        "Attendance Percentage",
        min_value=0.0,
        max_value=100.0,
        value=75.0,
        step=0.1
    )
    
    # Multi-select for interests
    interests = st.multiselect(
        "Select Your Interests",
        ["Programming", "Data Science", "AI/ML", "Web Development", 
         "Mobile Apps", "Networking", "Cybersecurity", "Design", 
         "Business Analytics", "Cloud Computing"]
    )
    
    # Submit button
    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    if not name:  # Check if name is empty
        st.error("Please enter student name!")
    else:
        # Initialize database
        conn = init_db()
        
        # Save data to database
        try:
            c = conn.cursor()
            c.execute('''
                INSERT INTO students (name, age, grade, department, attendance, interests, submission_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, age, grade, department, attendance, ','.join(interests), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            st.success("Data saved successfully! 🎉")
        except Exception as e:
            st.error(f"Error saving data: {e}")
        finally:
            conn.close()

# Display saved records
st.markdown("---")
st.subheader("📊 Saved Records")

conn = init_db()
df = pd.read_sql_query("SELECT * FROM students", conn)
conn.close()

if not df.empty:
    # Format the dataframe
    df['interests'] = df['interests'].fillna('')
    df['submission_date'] = pd.to_datetime(df['submission_date'])
    
    # Display as an interactive table
    st.dataframe(
        df,
        column_config={
            "id": "ID",
            "name": "Student Name",
            "age": "Age",
            "grade": st.column_config.NumberColumn("Grade", format="%.1f"),
            "department": "Department",
            "attendance": st.column_config.NumberColumn("Attendance %", format="%.1f%%"),
            "interests": "Interests",
            "submission_date": st.column_config.DatetimeColumn("Submitted On", format="D MMM YYYY, h:mm a")
        },
        hide_index=True,
    )
    
    # Add some statistics
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Students", len(df))
    with col2:
        st.metric("Average Grade", f"{df['grade'].mean():.2f}")
    with col3:
        st.metric("Average Attendance", f"{df['attendance'].mean():.1f}%")
else:
    st.info("No records found. Submit the form to see the data here!")