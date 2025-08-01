from base_data import BaseData, fake, np
from datetime import datetime as dt

DEFAULT_DATE_STR = '01-01-1111'

placements_table = (
    "CREATE TABLE IF NOT EXISTS Placements ("
        "placement_id VARCHAR(3) PRIMARY KEY,"
        "student_id VARCHAR(3),"
        "mock_interview_score INT,"
        "internships_completed INT,"
        "placement_status VARCHAR(20),"
        "company_name VARCHAR(100),"
        "placement_package FLOAT,"
        "interview_rounds_cleared INT,"
        "placement_date DATE,"
        "FOREIGN KEY (student_id) REFERENCES students(student_id)"
        ");"
    )

class PlacementsData(BaseData):
    def __init__(self, student_ids):
        super().__init__("placements", placements_table, len(student_ids))
        self.student_ids = student_ids

    def generate_data(self):
        ids = self.generate_id()
        self.data = []
        default_date = dt.strptime(DEFAULT_DATE_STR, '%m-%d-%Y').date()

        for i in range(self.num_data):
            placement_status = np.random.choice(["Ready", "Not Ready", "Placed"])
            company = fake.company() if placement_status == "Placed" else "Unknown"
            package = round(np.random.uniform(40000, 120000), 2) if placement_status == "Placed" else 0
            date = fake.date_between(start_date='-1y', end_date='today') if placement_status == "Placed" else default_date

            self.data.append({
                "placement_id": ids[i],
                "student_id": self.student_ids[i],
                "mock_interview_score": np.random.randint(40, 100),
                "internships_completed": np.random.randint(0, 3),
                "placement_status": placement_status,
                "company_name": company,
                "placement_package": package,
                "interview_rounds_cleared": np.random.randint(1, 5),
                "placement_date": date
            })
