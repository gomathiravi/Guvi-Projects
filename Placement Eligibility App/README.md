# Guvi-Projects
Projects at GUVI

*** Student data analysis
This project was built as part of training at GUVI.
This project is about student data analysis. Designed to provide real-time insights into placement readiness and other key educational metrics.

***** Data Management
All data classes inherit from BaseData, which handles:

* create and store data into text file in CSV format
* holds the local state such as table name, number of students data
* Insertion into a MySQL database

** The base database class BaseDatabase abstracts:
* Table creation
* Connection lifecycle
* Query execution

****** Application User Interface
* Project Introduction
    1. Overview of the Student Placement App
    2. Purpose and scope of the application

* Student Data Visualization
    1. Visualize datasets related to:
    2. Total students
    3. Programming skills
    4. Soft skills
    5. Placement stats
    6. Apply interactive filters to explore data

* SQL Queries
    1. Run custom or pre-defined SQL queries
    2. Gain insight into eligibility and placement factors


****** Project Structure
StudentPlacementApp/
│
├── student_placement.py         # Starts the Streamlit app with 3 main options:
│                                # - Project Introduction
│                                # - Student Data Visualization
│                                # - SQL Queries
│
├── base_data_base.py            # Base class for database operations:
│   └── class BaseDatabase       # - Initializes DB
│                                # - Creates tables
│                                # - Executes SQL queries
│
├── base_data.py                 # Base data handler derived from BaseDatabase:
│   └── class BaseData           # - Holds student metadata
│                                # - Saves data to CSV
│                                # - Inserts into DB
│
├── main.py                      # Starts the application
│                                # - creates a database
│                                # - creates a the relevant tables
│                                # - insert generated data into tables
│
├── placements_data.py
│   └── class PlacementData(BaseData)
│
├── programming_data.py
│   └── class ProgrammingData(BaseData)
│
├── soft_skills_data.py
│   └── class SoftSkillsData(BaseData)
│
├── students_data.py
│   └── class StudentsData(BaseData)
