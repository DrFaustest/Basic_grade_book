
import json
from typing import List, Dict, Tuple, Union

class GradebookController:
    def __init__(self):
        """
        Initialize the GradebookController class.
        """
        self.classes: List[str] = []
        self.students: Dict[str, List[str]] = {}
        self.assignments: Dict[str, List[str]] = {}
        self.grades: Dict[str, Dict[str, Union[int, str]]] = {}
        self.change_history: List[Tuple[List[str], Dict[str, List[str]], Dict[str, List[str]], Dict[str, Dict[str, Union[int, str]]]]] = []
        self.load_data()
        
    def load_classes(self) -> List[str]:
        """
        Load the list of classes.
        
        Returns:
            list: A list of class names.
        """
        return self.classes
    
    def load_students(self, class_id: str) -> List[str]:
        """
        Load the list of students for a given class.
        
        Args:
            class_id (str): The ID of the class.
        
        Returns:
            list: A list of student names.
        """
        return self.students.get(class_id, [])
    
    def load_assignments(self, class_id: str) -> List[str]:
        """
        Load the list of assignments for a given class.
        
        Args:
            class_id (str): The ID of the class.
        
        Returns:
            list: A list of assignment names.
        """
        with open('data.json', 'r') as file:
            data = json.load(file)
        class_data = data.get(class_id, {})
        assignments = set()
        for grades in class_data.values():
            assignments.update(grades.keys())
        return list(assignments)

    
    def load_grades(self, class_id: str) -> Dict[str, Union[int, str]]:
        """
        Load the grades for a given class.
        
        Args:
            class_id (str): The ID of the class.
        
        Returns:
            dict: A dictionary of student names and their corresponding grades.
        """
        return self.grades.get(class_id, {})

    def load_data(self) -> None:
        """
        Load the data from the JSON file.
        """
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            self.classes = list(data.keys())
            self.students = {class_name: list(data[class_name].keys()) for class_name in data}
            self.assignments = {class_name: list(data[class_name].values()) for class_name in data}
            self.grades = {class_name: {student: data[class_name][student] for student in data[class_name]} for class_name in data}
        except Exception as e:
            print(f"Failed to load data: {e}")
            

    def add_class(self, class_name: str) -> Tuple[bool, str]:
        """
        Add a new class to the system.
        
        Args:
            class_name (str): The name of the class.
        
        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            if class_name in data:
                return False, "Class already exists."
            data[class_name] = {}
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            self.load_data()
            return True, "Class added successfully."
        except Exception as e:
            print(f"Failed to add class: {e}")
            return False, "Failed to add class."

    def add_student(self, class_id: str, student_name: str) -> Tuple[bool, str]:
        """
        Add a new student to the specified class and initialize their grades for all assignments.
        
        Args:
            class_id (str): The ID of the class.
            student_name (str): The name of the student.
        
        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            if class_id not in data:
                data[class_id] = {}
            if student_name not in data[class_id]:
                data[class_id][student_name] = {}
                assignments = self.load_assignments(class_id)
                for assignment in assignments:
                    data[class_id][student_name][assignment] = "Not Graded"
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            self.load_data()
            return True, "Student added successfully."
        except Exception as e:
            print(f"Failed to add student: {e}")
            return False, "Failed to add student."


    def add_assignment(self, class_id: str, assignment_name: str, initial_grade: Union[int, None] = None) -> Tuple[bool, str]:
        """
        Adds an assignment to all students in a class with an initial grade.
        
        Args:
            class_id (str): The ID of the class.
            assignment_name (str): The name of the assignment.
            initial_grade (int, optional): The initial grade for the assignment. Defaults to None.
        
        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            if class_id not in data:
                return False, "Class does not exist."
            for student in data[class_id]:
                data[class_id][student][assignment_name] = initial_grade if initial_grade is not None else "Not Graded"
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            self.load_data()
            return True, "Assignment added successfully."
        except Exception as e:
            print(f"Failed to add assignment: {e}")
            return False, "Failed to add assignment."


    
    def update_grade(self, class_id: str, student_name: str, assignment_name: str, grade: int) -> bool:
        """
        Update or add a grade for a specific student and assignment in a class.
        
        Args:
            class_id (str): The ID of the class.
            student_name (str): The name of the student.
            assignment_name (str): The name of the assignment.
            grade (int): The grade for the assignment.
        
        Returns:
            bool: True if the grade was updated successfully, False otherwise.
        """
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)

            if class_id not in data:
                data[class_id] = {}
            if student_name not in data[class_id]:
                data[class_id][student_name] = {}

            data[class_id][student_name][assignment_name] = grade

            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
            self.load_data()
            return True
        except Exception as e:
            print(f"Failed to update grade: {e}")
            return False
  
    def save_changes(self) -> bool:
        """
        Save the current state of the gradebook to a file.
        
        Returns:
            bool: True if the changes were saved successfully, False otherwise.
        """
        try:
            with open('data.json', 'w') as file:
                json.dump(self.grades, file, indent=4)
            return True
        except Exception as e:
            print(f"Failed to save changes: {e}")
            return False
    
    def undo_last_change(self) -> Tuple[bool, str]:
        """
        Undo the last change made to the gradebook.
        
        Returns:
            bool: True if the change was undone successfully, False otherwise.
            str: A message indicating the result of the undo operation.
        """
        if self.change_history:
            self.classes, self.students, self.assignments, self.grades = self.change_history.pop()
            return True
        return False, "No changes to undo."

    
    def validate_input(self, input_data: str) -> Tuple[bool, str]:
        """
        Validate the input data.
        
        Args:
            input_data (str): The input data to validate.
        
        Returns:
            tuple: A tuple containing a boolean indicating whether the input is valid and a message.
        """
        # Expand based on specific needs
        if not input_data or not isinstance(input_data, str) or len(input_data.strip()) == 0:
            return False, "Invalid input."
        return True, ""
    