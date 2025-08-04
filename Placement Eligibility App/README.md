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


### Project Structure
## File Descriptions

### `main.py`
- Entry point for Running the application
- - **To create database**
  - **generate student data**
  - **save the student data in <given filename> with .csv file**
  - **Create tables and store all the students in the given table name**
  - **Close the data base connection**

### `student_placement.py`
- Entry point to launch the User Interface using the streamlit Modules with the following main sections:
  - **Project Introduction**
  - **Student Data Visualization**
  - **SQL Queries**

### `base_data_base.py`
- Contains `BaseDatabase` class:
  - Initializes database
  - Creates necessary tables
  - Provides method for executing SQL queries

### `base_data.py`
- Contains `BaseData` class derived from `BaseDatabase`:
  - Manages student metadata
  - Provides functionality to save data to CSV
  - Inserts data into the database

### `placements_data.py`
- Contains `PlacementData` class extending `BaseData`

### `programming_data.py`
- Contains `ProgrammingData` class extending `BaseData`

### `soft_skills_data.py`
- Contains `SoftSkillsData` class extending `BaseData`

### `students_data.py`
- Contains `StudentsData` class extending `BaseData`

## Requirements

- Python 3.8+
- Streamlit
- pandas
- sqlite3 (standard with Python)

## Usage

Run the app using:

```bash
streamlit run student_placement.py
