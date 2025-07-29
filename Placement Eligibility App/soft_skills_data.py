from base_data import BaseData, np

class SoftSkillsData(BaseData):
    def __init__(self, student_ids):
        super().__init__(len(student_ids))
        self.student_ids = student_ids

    def generate_data(self):
        ids = self.generate_id()
        self.data = [{
            "soft_skill_id": ids[i],
            "student_id": self.student_ids[i],
            "communication": np.random.randint(30, 100),
            "teamwork": np.random.randint(50, 100),
            "presentation": np.random.randint(50, 100),
            "leadership": np.random.randint(50, 100),
            "critical_thinking": np.random.randint(50, 100),
            "interpersonal_skills": np.random.randint(50, 100)
        } for i in range(self.num_data)]
