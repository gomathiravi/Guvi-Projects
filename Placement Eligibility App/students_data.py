from base_data import BaseData, fake, np

students_table = (
        "CREATE TABLE IF NOT EXISTS Students ("
            "student_id VARCHAR(3) PRIMARY KEY,"
            "name VARCHAR(100),"
            "age INT,"
            "gender VARCHAR(10),"
            "email VARCHAR(100),"
            "phone VARCHAR(20),"
            "enrollment_year INT,"
            "course_batch VARCHAR(50),"
            "city VARCHAR(50),"
            "graduation_year INT"
            ");"
        )

class StudentsData(BaseData):
    def __init__(self):
        super().__init__("students", students_table)

    def generate_data(self):
        course_batches = ['Aws', 'Angular', 'Game Development', 'Full Stack Development', 'Dev Ops', 'Data Science', 'Cloud Computing', 'Cyber Security', 'Data Bases', 'Business Management' ]
        genders = ['Male', 'Female', 'Other']

        # Generate random fields using NumPy
        ages_list = np.random.randint(16, 60, self.num_data)
        genders_list = np.random.choice(genders, self.num_data)
        enrollment_years_list = np.random.randint(2015, 2025, self.num_data)
        course_batches_list = np.random.choice(course_batches, self.num_data)
        years_list = np.random.randint(2018, 2025, self.num_data)
        ids = self.generate_id()

        self.data = [{
            "student_id": ids[i],
            "name": fake.name(),
            "age": ages_list[i],
            "gender": genders_list[i],
            "email": fake.email(),
            "phone": fake.phone_number(),
            "enrollment_year": enrollment_years_list[i],
            "course_batch": course_batches_list[i],
            "city": fake.city(),
            "graduation_year": years_list[i] + 1
        } for i in range(self.num_data)]

        student_id_list = [row['student_id'] for row in self.data]
        return student_id_list

# course batch list : in another format
# f"Batch-{np.random.choice(['A','B','C'])}-{years[i]}",