from base_data import BaseData, fake, np

class PlacementsData(BaseData):
    def __init__(self, student_ids):
        super().__init__(len(student_ids))
        self.student_ids = student_ids

    def generate_data(self):
        ids = self.generate_id()
        self.data = []
        for i in range(self.num_data):
            placement_status = np.random.choice(["Ready", "Not Ready", "Placed"])
            company = fake.company() if placement_status == "Placed" else None
            package = round(np.random.uniform(40000, 120000), 2) if placement_status == "Placed" else None
            date = fake.date_between(start_date='-1y', end_date='today') if placement_status == "Placed" else None

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
