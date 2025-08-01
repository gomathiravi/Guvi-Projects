from students_data import StudentsData
from programming_data import ProgrammingData
from soft_skills_data import SoftSkillsData
from placements_data import PlacementsData

# create Students data
students = StudentsData()
student_ids = students.generate_data()
student_file_path = students.save_to_file("students")
students.store_data_in_db()

# create Programming data
programming = ProgrammingData(student_ids)
programming.generate_data()
programming_file_path = programming.save_to_file("programming")
programming.store_data_in_db()

# create Soft Skills data
soft_skills = SoftSkillsData(student_ids)
soft_skills.generate_data()
soft_skills_file_path = soft_skills.save_to_file("soft_skills")
soft_skills.store_data_in_db()

# create Placements data
placements = PlacementsData(student_ids)
placements.generate_data()
placements_file_path = placements.save_to_file("placements")
placements.store_data_in_db()
