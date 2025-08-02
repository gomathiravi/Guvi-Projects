import streamlit as st
import mysql.connector as sql
import pandas as pd
from base_data_base import BaseDatabase

db_object = BaseDatabase()

def display_score_options():
    # Fetch latest_project_score
    df_project_score = db_object.run_query("SELECT DISTINCT latest_project_score FROM programming ORDER BY latest_project_score")
    latest_project_score = df_project_score["latest_project_score"].tolist()
    st.write(latest_project_score)
    return st.multiselect("Select Multiple Project scores", latest_project_score)

# Streamlit App Title
st.set_page_config(page_title="Students Placement Data Analysis", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Project Introduction", "Student Data Visualization", "Student Placement Insight"])

# -------------------------------- PAGE 1: Page Introduction --------------------------------
if page == "Project Introduction":
    st.title("Student Data Analysis")
    st.subheader(" An App for Exploring Students Data For Placements")
    st.write("""
    This project helps view data of all the students enrolled.
    It provides to view students information with various parameters i.e: their programming skills, scores, soft skills, placement eligibility.

    **Features:**
    - View and filter student data by city, batch, or scores.
    - Generate dynamic visualizations for multiple programming and soft skill features.
    - Run predefined SQL queries to explore insights.

    **Database Used:** `students_db`
    """)

# -------------------------------- PAGE 2: Students Data Visualization --------------------------------
elif page == "Student Data Visualization":
    st.title("Student Data Visualizer")

    # Fetch batch list
    course_batch = db_object.run_query("SELECT DISTINCT course_batch FROM students")["course_batch"].tolist()

    # Filters
    selected_batch = st.selectbox("Select Batch", course_batch)
    filter_option = st.radio("Filter By:", ["Placements", "Scores", "Specific Year", "Specific City"])

    query = f"SELECT * FROM students WHERE course_batch = '{selected_batch}'"
    table_header = "Students"
    if filter_option == "Placements":
        placement_query = db_object.run_query("SELECT DISTINCT placement_status FROM placements")["placement_status"].tolist()
        selected_status = st.selectbox("Select Placement Status", placement_query)

        if selected_status == "Placed":
            table_header = "Placed"
            query = f"""
            SELECT s.name, s.course_batch, pl.placement_status, pl.company_name,
            pl.placement_package,pl.placement_date
            FROM students s
            JOIN placements pl ON s.student_id = pl.student_id
            WHERE placement_status = '{selected_status}';"""
        elif selected_status == "Ready":
            programme_query = db_object.run_query("SELECT DISTINCT language FROM programming")["language"].tolist()
            language_status = st.selectbox("Select Language ", programme_query)
            query = f"""
            SELECT s.name, s.course_batch, pr.language, pr.problems_solved,
            pr.assessments_completed, pr.mini_projects, pr.certifications_earned, pr.latest_project_score
            FROM students s
            JOIN programming pr ON s.student_id = pr.student_id
            WHERE language = '{language_status}';"""
        else:
            query = f"""
            SELECT s.name, s.course_batch, pr.language, pr.problems_solved,
            pr.assessments_completed, pr.mini_projects, pr.certifications_earned, pr.latest_project_score
            FROM programming pr
            JOIN students s ON s.student_id = pr.student_id;"""
    elif filter_option == "Scores":
        query = ""
        latest_score_selected = display_score_options()
        st.write(latest_score_selected)
        if len(latest_score_selected) != 0:
            latest_score_selected = sorted(latest_score_selected)
            max_score = latest_score_selected[len(latest_score_selected)-1]
            st.write(f"{latest_score_selected[0]},{max_score}" )
            query = f""" SELECT s.name, s.course_batch, pr.language, pr.problems_solved,
                pr.assessments_completed, pr.mini_projects, pr.certifications_earned, pr.latest_project_score
                FROM programming pr
                JOIN students s ON s.student_id = pr.student_id
                WHERE pr.latest_project_score BETWEEN {latest_score_selected[0]} AND {max_score};"""

    elif filter_option == "Specific Year":
        selected_year = st.selectbox("Choose a Year", range(2015, 2025))
        query += f" AND enrollment_year = '{selected_year}';"
    else:
        cities = db_object.run_query("SELECT DISTINCT city FROM students")["city"].tolist()
        selected_city = st.selectbox("Select City", cities)
        query += f" AND city = '{selected_city}';"

    st.write(query)
    df = db_object.run_query(query)

    if not df.empty:
        st.subheader(f"  {table_header}: {len(df)}")
        st.dataframe(df, hide_index=True)
    else:
        st.warning("No data available for the selected filters.")

# -------------------------------- PAGE 3: SQL Queries --------------------------------
elif page == "Student Placement Insight":
    st.title("Student Placement Eligibility Insight")

    queries = {
        "1. Count of Students based on Placement status": "SELECT placement_status, COUNT(*) AS student_count FROM Placements GROUP BY placement_status;",
        "2. Co-relate internship count with placement success": "SELECT internships_completed, placement_status,COUNT(*) AS student_count FROM Placements GROUP BY internships_completed, placement_status ORDER BY internships_completed;",
        "3. Companies hire the most students and offer the highest packages": "SELECT company_name,COUNT(student_id) AS students_hired, MAX(placement_package) AS highest_package FROM Placements WHERE placement_status = 'Placed' GROUP BY company_name ORDER BY students_hired DESC, highest_package DESC;",
        "4. Correlate soft skill scores with placement outcomes": "SELECT p.placement_status, ROUND(AVG(s.communication), 2) AS avg_communication, ROUND(AVG(s.teamwork), 2) AS avg_teamwork, ROUND(AVG(s.presentation), 2) AS avg_presentation, ROUND(AVG(s.leadership), 2) AS avg_leadership, ROUND(AVG(s.critical_thinking), 2) AS avg_critical_thinking, ROUND(AVG(s.interpersonal_skills), 2) AS avg_interpersonal_skills FROM soft_skills s JOIN placements p ON s.student_id = p.student_id GROUP BY p.placement_status;",
        "5. Students with consistently high soft skill scores": "SELECT s.name AS student_name, ROUND((SS.communication + SS.teamwork + SS.presentation + SS.leadership + SS.critical_thinking + SS.interpersonal_skills) / 6.0, 2) AS avg_soft_skill_score FROM soft_skills SS JOIN Students s ON SS.student_id = s.student_id WHERE (SS.communication + SS.teamwork + SS.presentation + SS.leadership + SS.critical_thinking + SS.interpersonal_skills) / 6.0 >= 75 ORDER BY avg_soft_skill_score DESC;",
        "6. Batch Placement overview": "SELECT s.course_batch, COUNT(p.student_id) AS students_placed, COUNT(s.student_id) AS total_students, ROUND(((COUNT(p.student_id)  * 100.0) / COUNT(s.student_id) ),2) AS placement_rate_percentage FROM Students s LEFT JOIN Placements p ON s.student_id = p.student_id AND p.placement_status = 'Placed' GROUP BY s.course_batch ORDER BY placement_rate_percentage DESC;",
        "7. Skill to placement package ": "SELECT s.student_id, s.name, pl.mock_interview_score, pl.internships_completed, pg.language, pg.problems_solved, pg.latest_project_score, ss.communication, ss.teamwork, ss.leadership, ss.critical_thinking, pl.placement_package FROM Students s JOIN Placements pl ON s.student_id = pl.student_id JOIN Programming pg ON s.student_id = pg.student_id JOIN Soft_skills ss ON s.student_id = ss.student_id WHERE pl.placement_package IS NOT NULL ORDER BY pl.placement_package DESC;",
        "8. Eligibily based on skill thresholds": "SELECT s.student_id, s.name, pg.latest_project_score, pg.problems_solved, ss.communication, ss.teamwork, ss.leadership, ss.critical_thinking, CASE WHEN pg.latest_project_score >= 80 AND pg.problems_solved >= 50 AND ss.communication >= 70 AND ss.teamwork >= 70 AND ss.leadership >= 60 AND ss.critical_thinking >= 60 THEN 'Eligible' ELSE 'Not Eligible' END AS eligibility_status FROM Students s JOIN Programming pg ON s.student_id = pg.student_id JOIN Soft_skills ss ON s.student_id = ss.student_id;",
        "9. Mapping Placements rounds to scores, projects and soft skills": "SELECT s.student_id, s.name, pl.interview_rounds_cleared, pl.mock_interview_score, pl.internships_completed, pg.latest_project_score, pg.certifications_earned, ss.communication, ss.leadership, pl.placement_package FROM Students s JOIN Placements pl ON s.student_id = pl.student_id JOIN Programming pg ON s.student_id = pg.student_id JOIN Soft_skills ss ON s.student_id = ss.student_id WHERE pl.placement_status = 'Placed' ORDER BY pl.interview_rounds_cleared DESC;"
     }

    selected_query = st.selectbox("Choose a Query", list(queries.keys()))
    query_result = db_object.run_query(queries[selected_query])

    st.write("### Query Result:")
    st.dataframe(query_result, hide_index=True)
