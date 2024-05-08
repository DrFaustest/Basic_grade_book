import json
from typing import List, Dict, Tuple, Union

class GradebookController:
    def __init__(self):
        """
        Initializes a GradebookController object.
        """
        self.current_class_data = {}
        self.classes = []
        self.load_data()

    def load_data(self, class_id: str = None) -> None:
        """
        Loads the data from the 'data.json' file and updates the class data.

        Parameters:
        - class_id (str): The ID of the class to load data for. If not provided, loads data for all classes.

        Returns:
        None
        """
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            self.classes = list(data.keys())
            if class_id:
                self.current_class_data = data.get(class_id, {})
        except Exception as e:
            print(f"Failed to load data: {e}")

    def get_students(self) -> List[str]:
        """
        Returns a list of student names in the current class.

        Returns:
        - List[str]: A list of student names.
        """
        return list(self.current_class_data.keys())
    
    def get_grades_for_student(self, student_name: str) -> List[Union[int, str]]:
        """
        Returns a list of grades for a specific student.

        Parameters:
        - student_name (str): The name of the student.

        Returns:
        - List[Union[int, str]]: A list of grades for the student.
        """
        grades = []
        student_grades = self.current_class_data.get(student_name, {})
        for assignment in student_grades.values():
            grades.append(assignment['score'])
        return grades

    def get_assignments(self) -> List[str]:
        """
        Returns a list of assignment names in the current class.

        Returns:
        - List[str]: A list of assignment names.
        """
        assignments = []
        for grades in self.current_class_data.values():
            for assignment in grades.keys():
                if assignment not in assignments:
                    assignments.append(assignment)
        return assignments

    def get_grades(self, assignment_name: str) -> Dict[str, Union[int, str]]:
        """
        Returns a dictionary of grades for a specific assignment.

        Parameters:
        - assignment_name (str): The name of the assignment.

        Returns:
        - Dict[str, Union[int, str]]: A dictionary of grades for the assignment, with student names as keys and grades as values.
        """
        assignment_grades = {}
        for student, student_grades in self.current_class_data.items():
            if assignment_name in student_grades:
                assignment_grades[student] = student_grades[assignment_name]['score']
        return assignment_grades

    def get_max_points(self, assignment_name: str) -> Union[int, None]:
        """
        Returns the maximum points for a specific assignment.

        Parameters:
        - assignment_name (str): The name of the assignment.

        Returns:
        - Union[int, None]: The maximum points for the assignment, or None if the assignment does not exist.
        """
        for student_grades in self.current_class_data.values():
            if assignment_name in student_grades:
                return student_grades[assignment_name]['max_points']

    def add_class(self, class_name: str) -> Tuple[bool, str]:
        """
        Adds a new class to the gradebook.

        Parameters:
        - class_name (str): The name of the class to add.

        Returns:
        - Tuple[bool, str]: A tuple indicating whether the class was added successfully (True/False) and a message describing the result.
        """
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
        """
        Adds a new student to a class.

        Parameters:
        - class_id (str): The ID of the class to add the student to.
        - student_name (str): The name of the student to add.

        Returns:
        - Tuple[bool, str]: A tuple indicating whether the student was added successfully (True/False) and a message describing the result.
        """
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
        """
        Adds a new assignment to a class.

        Parameters:
        - class_id (str): The ID of the class to add the assignment to.
        - assignment_name (str): The name of the assignment to add.
        - max_points (Union[int, None]): The maximum points for the assignment. Defaults to None.
        - initial_grade (Union[int, None]): The initial grade for the assignment. Defaults to None.

        Returns:
        - Tuple[bool, str]: A tuple indicating whether the assignment was added successfully (True/False) and a message describing the result.
        """
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
        """
        Updates the grade for a specific assignment of a student.

        Parameters:
        - class_id (str): The ID of the class.
        - student_name (str): The name of the student.
        - assignment_name (str): The name of the assignment.
        - grade (int): The new grade for the assignment.

        Returns:
        - bool: True if the grade was updated successfully, False otherwise.
        """
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
        """
        Saves the changes made to the gradebook.

        Returns:
        - bool: True if the changes were saved successfully, False otherwise.
        """
        try:
            with open('data.json', 'w') as file:
                json.dump(self.current_class_data, file, indent=4)
            return True
        except Exception as e:
            print(f"Failed to save changes: {e}")
            return False

    def remove_student(self, class_id: str, student_name: str) -> Tuple[bool, str]:
        """
        Removes a student from a class.

        Parameters:
        - class_id (str): The ID of the class to remove the student from.
        - student_name (str): The name of the student to remove.

        Returns:
        - Tuple[bool, str]: A tuple indicating whether the student was removed successfully (True/False) and a message describing the result.
        """
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
        """
        Removes an assignment from a class.

        Parameters:
        - class_id (str): The ID of the class to remove the assignment from.
        - assignment_name (str): The name of the assignment to remove.

        Returns:
        - Tuple[bool, str]: A tuple indicating whether the assignment was removed successfully (True/False) and a message describing the result.
        """
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
        
    def determine_class_grade(self, class_id: str, student_name: str) -> Union[int, None]:
        """
        Determines the overall grade for a student in a class.

        Parameters:
        - class_id (str): The ID of the class.
        - student_name (str): The name of the student.

        Returns:
        - Union[int, None]: The overall grade for the student in the class, or None if the class or student does not exist.
        """
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            if class_id not in data or student_name not in data[class_id]:
                return None
            total_points = 0
            earned_points = 0
            for assignment in data[class_id][student_name].values():
                if assignment['score'] != "Not Graded":
                    total_points += assignment['max_points']
                    earned_points += assignment['score']
            return round((earned_points / total_points) * 100, 2)
        except Exception as e:
            print(f"Failed to determine class grade: {e}")
            return None
        
    def convert_to_letter_grade(self, grade: int) -> str:
        """
        Converts a numeric grade to a letter grade.

        Parameters:
        - grade (int): The numeric grade to convert.

        Returns:
        - str: The letter grade corresponding to the numeric grade.
        """
        if grade is None:
            return "Not Graded"
        if grade >= 90:
            return "A"
        elif grade >= 80:
            return "B"
        elif grade >= 70:
            return "C"
        elif grade >= 60:
            return "D"
        return "F"