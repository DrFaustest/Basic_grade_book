import json
from typing import List, Dict, Tuple, Union

class GradebookController:
    def __init__(self):
        self.current_class_data = {}
        self.classes = []
        self.load_data()

    def load_data(self, class_id: str = None) -> None:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            self.classes = list(data.keys())
            if class_id:
                self.current_class_data = data.get(class_id, {})
        except Exception as e:
            print(f"Failed to load data: {e}")

    def get_students(self) -> List[str]:
        return list(self.current_class_data.keys())
    
    def get_grades_for_student(self, student_name: str) -> List[Union[int, str]]:
        grades = []
        student_grades = self.current_class_data.get(student_name, {})
        for assignment in student_grades.values():
            grades.append(assignment['score'])
        return grades

    def get_assignments(self) -> List[str]:
        assignments = set()
        for grades in self.current_class_data.values():
            assignments.update(grades.keys())
        return list(assignments)

    def get_grades(self, assignment_name: str) -> Dict[str, Union[int, str]]:
        assignment_grades = {}
        for student, student_grades in self.current_class_data.items():
            if assignment_name in student_grades:
                assignment_grades[student] = student_grades[assignment_name]['score']
        return assignment_grades

    def get_max_points(self, assignment_name: str) -> Union[int, None]:
        for student_grades in self.current_class_data.values():
            if assignment_name in student_grades:
                return student_grades[assignment_name]['max_points']

    def add_class(self, class_name: str) -> Tuple[bool, str]:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            if class_name in data:
                return False, "Class already exists."
            data[class_name] = {}
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            self.load_data(class_name)
            return True, "Class added successfully."
        except Exception as e:
            print(f"Failed to add class: {e}")
            return False, "Failed to add class."

    def add_student(self, class_id: str, student_name: str) -> Tuple[bool, str]:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            if class_id not in data:
                data[class_id] = {}
            if student_name not in data[class_id]:
                data[class_id][student_name] = {}
                assignments = self.get_assignments()
                for assignment in assignments:
                    data[class_id][student_name][assignment] = {"score": "Not Graded", "max_points": self.get_max_points(assignment)}
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            self.load_data(class_id)
            return True, "Student added successfully."
        except Exception as e:
            print(f"Failed to add student: {e}")
            return False, "Failed to add student."

    def add_assignment(self, class_id: str, assignment_name: str, max_points: Union[int, None] = None, initial_grade: Union[int, None] = None) -> Tuple[bool, str]:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            if class_id not in data:
                return False, "Class does not exist."
            for student in data[class_id]:
                data[class_id][student][assignment_name] = {"score": initial_grade if initial_grade is not None else "Not Graded", "max_points": max_points}
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            self.load_data(class_id)
            return True, "Assignment added successfully."
        except Exception as e:
            print(f"Failed to add assignment: {e}")
            return False, "Failed to add assignment."

    def update_grade(self, class_id: str, student_name: str, assignment_name: str, grade: int) -> bool:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            if class_id not in data or student_name not in data[class_id] or assignment_name not in data[class_id][student_name]:
                return False
            data[class_id][student_name][assignment_name]['score'] = grade
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            self.load_data(class_id)
            return True
        except Exception as e:
            print(f"Failed to update grade: {e}")
            return False

    def save_changes(self) -> bool:
        try:
            with open('data.json', 'w') as file:
                json.dump(self.current_class_data, file, indent=4)
            return True
        except Exception as e:
            print(f"Failed to save changes: {e}")
            return False

    def remove_student(self, class_id: str, student_name: str) -> Tuple[bool, str]:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            if class_id not in data:
                return False, "Class does not exist."
            if student_name not in data[class_id]:
                return False, "Student does not exist."
            del data[class_id][student_name]
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            self.load_data(class_id)
            return True, "Student removed successfully."
        except Exception as e:
            print(f"Failed to remove student: {e}")
            return False, "Failed to remove student."

    def remove_assignment(self, class_id: str, assignment_name: str) -> Tuple[bool, str]:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            if class_id not in data:
                return False, "Class does not exist."
            for student in data[class_id]:
                if assignment_name in data[class_id][student]:
                    del data[class_id][student][assignment_name]
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            self.load_data(class_id)
            return True, "Assignment removed successfully."
        except Exception as e:
            print(f"Failed to remove assignment: {e}")
            return False, "Failed to remove assignment."