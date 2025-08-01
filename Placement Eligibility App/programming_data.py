from base_data import BaseData, np

programming_table = (
    "CREATE TABLE IF NOT EXISTS Programming ("
        "programming_id VARCHAR(3) PRIMARY KEY,"
        "student_id VARCHAR(3),"
        "language VARCHAR(20),"
        "problems_solved INT,"
        "assessments_completed INT,"
        "mini_projects INT,"
        "certifications_earned INT,"
        "latest_project_score INT,"
        "FOREIGN KEY (student_id) REFERENCES students(student_id)"
        ");"
    )

class ProgrammingData(BaseData):
    def __init__(self, student_ids):
        super().__init__("programming", programming_table, len(student_ids))
        self.student_ids = student_ids

    def generate_data(self):
        langugages = ['Python', 'SQL', 'Java','C++']

        # Generate random fields using NumPy
        langugages_list = np.random.choice(langugages, self.num_data)
        ids = self.generate_id()

        self.data = [{
            "programming_id": ids[i],
            "student_id": self.student_ids[i],
            "language": langugages_list[i],
            "problems_solved": np.random.randint(20, 200),
            "assessments_completed": np.random.randint(1, 10),
            "mini_projects": np.random.randint(0, 5),
            "certifications_earned": np.random.randint(0, 4),
            "latest_project_score": np.random.randint(50, 100)
        } for i in range(self.num_data)]
