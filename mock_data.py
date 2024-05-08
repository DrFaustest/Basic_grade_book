import random
import json

class Gradebook:
    def __init__(self, course_name, num_students, num_assignments):
        self.course_name = course_name
        self.num_students = num_students
        self.num_assignments = num_assignments
        self.data = {self.course_name: {}}
        self.generate_mock_data()

    def generate_mock_data(self):
        # Generate random student names
        for i in range(self.num_students):
            student_name = f"Student {i+1}"

            # Initialize the student's record
            self.data[self.course_name][student_name] = {}

            # Generate random assignment data
            for j in range(self.num_assignments):
                assignment_name = f"Assignment {j+1}"
                score = random.randint(0, 100)  # Random score between 0 and 100
                max_points = 100  # Assuming all assignments out of 100 points
                if random.random() < 0.1:  # 10% chance of not graded yet
                    score = "Not Graded"

                # Assign scores and max points
                self.data[self.course_name][student_name][assignment_name] = {
                    "score": score,
                    "max_points": max_points
                }

    def get_data(self):
        return self.data

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.data, file, indent=4)

# Create an instance of the Gradebook class for a course
gradebook = Gradebook("Math101", 25, 20)
gradebook.save_to_file("data.json")