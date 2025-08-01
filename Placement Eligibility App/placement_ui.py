import streamlit as st
from base_data_base import BaseDatabase
import pandas as pd

class PlacementUi():
    def __init__(self):
        self.db = BaseDatabase()
        self.min_mock_score = 70
        self.min_internships = 1
        self.status_filter = "All"
        self.min_certifications = 1
        self.min_soft_skills_avg = 70

    def launch_ui(self):
        print("..... Placement Ui:: launch ui........")
        st.set_page_config(page_title="Placement Eligibility App", layout="wide")
        st.title("Students Placement Eligibility")
        self.display_sidebar_filters()
        query = self.build_query()
        results = self.fetch_data(query)
        self.db.close_db()
        self.show_results(results)

    def display_sidebar_filters(self):
        print("..... Placement Ui:: display_sidebar_filters........")
        # st.sidebar.header(" Criteria's...")

        self.student_year_filter = st.sidebar.slider("Enrolled Year", 2015, 2025, 2025 )
        self.ready_only = st.sidebar.checkbox("✅ Only Show 'Ready for Placement' Students")
        self.status_filter = st.sidebar.selectbox("Placement Status", ["All", "Ready", "Not Ready", "Placed"])

        self.min_mock_score = st.sidebar.slider("Minimum Mock Interview Score", 0, 100, 70)
        self.min_internships = st.sidebar.slider("Minimum Internships", 0, 5, 1)
        self.min_certifications = st.sidebar.slider("Minimum Programming Certifications", 0, 5, 1)
        self.min_soft_skills_avg = st.sidebar.slider("Minimum Soft Skills Avg Score", 0, 100, 70)

    def build_query(self):
        print("..... Placement Ui:: build_query........")
        base_query = f"""
            SELECT s.student_id, s.name, s.city, s.course_batch,
                   pl.mock_interview_score, pl.internships_completed, pl.placement_status,
                   p.certifications_earned,
                   (ss.communication + ss.teamwork + ss.presentation + ss.leadership +
                    ss.critical_thinking + ss.interpersonal_skills)/6 AS avg_soft_skills
            FROM students s
            JOIN placements pl ON s.student_id = pl.student_id
            JOIN programming p ON s.student_id = p.student_id
            JOIN soft_skills ss ON s.student_id = ss.student_id
            WHERE pl.mock_interview_score >= {self.min_mock_score}
              AND pl.internships_completed >= {self.min_internships}
              AND p.certifications_earned >= {self.min_certifications}
              AND (ss.communication + ss.teamwork + ss.presentation + ss.leadership +
                   ss.critical_thinking + ss.interpersonal_skills)/6 >= {self.min_soft_skills_avg}
        """
        if self.status_filter != "All":
            base_query += f" AND pl.placement_status = '{self.status_filter}'"

        # base_query += f" GROUP BY pl.placement_status = 'Ready'"
        print (f" Query = {base_query}")
        return base_query

    def fetch_data(self, query):
        print("..... Placement Ui:: fetch_data........")
        return self.db.run_query(query)

    def show_results(self, df):
        print(f"..... Placement Ui:: show_results........{len(df)}")
        st.subheader(f"  Eligible Students: {len(df)}")
        st.dataframe(df)

    def run(self):
        self.setup_ui()
        query = self.build_query()
        df = self.fetch_data(query)
        self.show_results(df)
