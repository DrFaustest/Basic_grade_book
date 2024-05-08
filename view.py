
from typing import Dict, List
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from controller import GradebookController

class GradebookApp:

    def __init__(self, master: tk.Tk) -> None:
        '''
        Initialize the GradebookApp class
        
        Parameters:
            master (tk.Tk): The root window
            
            Returns:
                None
        '''
        self.master = master
        master.title("Gradebook Application")
        self.controller = GradebookController()
        self.geometry = "800x600"
        master.geometry(self.geometry)
        self.last_clicked = None
        
        self.label_welcome = tk.Label(master, text="Welcome to the Gradebook System", font=("Arial", 14))
        self.label_welcome.pack(pady=10)
        
        self.label_instructions = tk.Label(master, text="Select a or add a class and manage grades\nAdd students or assignments to the class\nDouble click on a grade to edit it\n", font=("Arial", 12))
        self.label_instructions.pack(pady=10)
        
        self.class_selection = ttk.Combobox(master, width=15, state='readonly')
        self.class_selection['values'] = self.controller.classes
        self.class_selection.bind("<<ComboboxSelected>>", self.on_class_selected)
        self.class_selection.pack(pady=5)
        
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.LEFT, padx=20)
        
        self.button_add_class = tk.Button(self.button_frame, text="Add Class", command=self.add_class)
        self.button_add_student = tk.Button(self.button_frame, text="Add Student", command=self.add_student)
        self.button_add_assignment = tk.Button(self.button_frame, text="Add Assignment", command=self.add_assignment)
        self.button_add_class.pack(fill=tk.X, padx=10, pady=10)
        self.button_add_student.pack(fill=tk.X, padx=10, pady=10)
        self.button_add_assignment.pack(fill=tk.X, padx=10, pady=10)
        
        # Black line separator
        self.separator1 = ttk.Separator(self.button_frame, orient='horizontal')
        self.separator1.pack(fill=tk.X, pady=10)
        
        self.button_total_grade = tk.Button(self.button_frame, text="Total Grade", command=self.calculate_total_grade)
        self.button_total_grade.pack(fill=tk.X, padx=10, pady=10)

        # Black line separator
        self.separator3 = ttk.Separator(self.button_frame, orient='horizontal')
        self.separator3.pack(fill=tk.X, pady=10)
        
        # Wide gap
        self.separator2 = tk.Frame(self.button_frame, height=50, bg=None)
        self.separator2.pack(fill=tk.X)
        
        self.button_remove_student = tk.Button(self.button_frame, text="Remove Student", command=self.remove_student, bg='red', fg='white')
        self.button_remove_student.pack(fill=tk.X, padx=10, pady=10)

        self.button_remove_assignment = tk.Button(self.button_frame, text="Remove Assignment", command=self.remove_assignment, bg='red', fg='white')
        self.button_remove_assignment.pack(fill=tk.X, padx=10, pady=10)
        

        
        self.tree_frame = tk.Frame(master)
        self.tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_treeview()

    def calculate_total_grade(self) -> None:
        '''
        
        Calculate the total grade for each student in the class
        
        Parameters:
            None
            
            Returns:
                None
        '''
        class_id = self.class_selection.get()
        students = self.controller.get_students()
        grade_list = []
        for student in students:
            percentage = self.controller.determine_class_grade(class_id, student)
            letter_grade = self.controller.convert_to_letter_grade(percentage)
            grade_list.append(f"{student}: {letter_grade} ({percentage}%)")
        
        grade_popup = tk.Toplevel(self.master)
        grade_popup.title("Class Grades")
        grade_popup.geometry("300x300")
        
        grade_label = tk.Label(grade_popup, text="\n".join(grade_list), font=("Arial", 12))
        grade_label.pack(pady=10)
        grade_scroll = tk.Scrollbar(grade_popup)
        grade_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        grade_label.config(yscrollcommand=grade_scroll.set)
        grade_scroll.config(command=grade_label.yview)
        
        grade_popup.mainloop()

    def on_class_selected(self, event) -> None:
        '''
        
        Handle the event when a class is selected
        
        Parameters:
            event (tk.Event): The event that triggered the function
            
            Returns:
                None
        '''
        class_id = self.class_selection.get()
        self.controller.load_data(class_id)
        assignments = self.controller.get_assignments()
        student_names = self.controller.get_students()
        self.update_treeview_columns(assignments)

        self.grades_view.delete(*self.grades_view.get_children())

        for student in student_names:
            student_grades = self.controller.get_grades_for_student(student)
            row_values = [student] + [grade for grade in student_grades]
            self.grades_view.insert('', 'end', values=row_values)

    def remove_student(self) -> None:
        '''
        
        Remove a student from the class
        
        Parameters:
            None
            
            Returns:
                None
        '''
        selected_item = self.grades_view.focus()
        if selected_item:
            student_name = self.grades_view.item(selected_item, 'values')[0]
            success, message = self.controller.remove_student(self.class_selection.get(), student_name)
            if success:
                self.grades_view.delete(selected_item)
                messagebox.showinfo("Success", message, parent=self.master)
                self.on_class_selected(event=None)
            else:
                messagebox.showerror("Error", message, parent=self.master)


    def remove_assignment(self,) -> None:
        '''
        
        Remove an assignment from the class
        
        Parameters:
            None
            
            Returns:
                None
        '''
        selected_item = self.grades_view.focus()
        if selected_item:
            student_name, assignment_name = self.last_clicked
            selected_class = self.class_selection.get()
            success, message = self.controller.remove_assignment(selected_class, assignment_name)
            if success:
                self.grades_view.delete(selected_item)
                messagebox.showinfo("Success", message, parent=self.master)
                self.class_selection.set(selected_class)
                self.on_class_selected(event=None)
            else:
                messagebox.showerror("Error", message, parent=self.master)

    def setup_treeview(self) -> None:
        '''
        
        Setup the treeview for the application
        
        Parameters:
            None
            
            Returns:
                None
        '''
        self.tree_frame = tk.Frame(self.master)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree_scroll = tk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.grades_view = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, columns=[], show="headings")
        self.grades_view.pack(fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.grades_view.yview)

        self.grades_view.bind("<Double-1>", self.edit_grade)

    def on_cell_click(self, event: tk.Event) -> None:
        '''
        
        Handle the event when a cell is clicked
        
        Parameters:
            event (tk.Event): The event that triggered the function
            
            Returns:
                None
        '''
        row_id = self.grades_view.identify_row(event.y)
        column_id = self.grades_view.identify_column(event.x)
        student_name = self.grades_view.item(row_id, 'values')[0]
        assignment_name = self.grades_view.heading(column_id)["text"]

        cell_value = self.grades_view.item(row_id)['values'][int(column_id[1:]) - 1]

        self.grades_view.selection_set(row_id)
        self.grades_view.focus_set()
        self.grades_view.focus(row_id)

        self.last_clicked = (student_name,assignment_name)
        print(self.last_clicked)

        print(f'You clicked on cell with value: {cell_value}')
    
    def update_treeview_columns(self, assignments: List[str]) -> None:
        '''
        
        Update the columns in the treeview
        
        Parameters:
            assignments (List[str]): The list of assignments
            
            Returns:
                None
        '''
        self.grades_view["columns"] = ["Student Name"] + self.controller.get_assignments()
        self.grades_view.heading('#1', text='Student Name', anchor='w')
        for idx, assignment in enumerate(assignments, start=2):
            self.grades_view.column(f'#{idx}', anchor='center', width=100)
            self.grades_view.heading(f'#{idx}', text=assignment)

        self.grades_view.bind('<ButtonRelease-1>', self.on_cell_click)

    def add_class(self) -> None:
        '''
        Add a class to the controller

        Parameters:
            None

        Returns:
            None
        '''
        class_name = simpledialog.askstring("Add Class", "Enter class name:", parent=self.master)
        if class_name:
            if class_name in self.controller.classes:
                messagebox.showerror("Error", "Class already exists.", parent=self.master)
            else:
                success, message = self.controller.add_class(class_name)
                if success:
                    self.controller.load_data()
                    self.class_selection['values'] = self.controller.classes
                    messagebox.showinfo("Success", "Class added successfully", parent=self.master)
                    self.on_class_selected(event=None)
                else:
                    messagebox.showerror("Error", message, parent=self.master)

    def add_student(self) -> None:
        '''
        Add a student to the class
        
        Parameters:
            None
            
            Returns:
                None
        '''
        class_id = self.class_selection.get()
        student_name = simpledialog.askstring("Add Student", "Enter student name:", parent=self.master)
        if student_name:
            if student_name in self.controller.get_students():
                messagebox.showerror("Error", "Student already exists in this class.", parent=self.master)
            else:
                student_name = " ".join([word.capitalize() for word in student_name.split()])
                success, message = self.controller.add_student(class_id, student_name)
                if success:
                    messagebox.showinfo("Success", message, parent=self.master)
                    self.on_class_selected(event=None)
                else:
                    messagebox.showerror("Error", message, parent=self.master)

    def add_assignment(self) -> None:
        '''
        Add an assignment to the class
        
        Parameters:
            None
            
            Returns:
                None
        '''
        class_id = self.class_selection.get()
        assignment_details = simpledialog.askstring("Add Assignment", "Enter assignment details:", parent=self.master)
        if assignment_details:
            if assignment_details in self.controller.get_assignments():
                messagebox.showerror("Error", "Assignment already exists.", parent=self.master)
            else:
                max_points = simpledialog.askinteger("Add Assignment", "Enter maximum points:", parent=self.master)
                self.master.focus_set()
                if max_points is not None and max_points >= 0:
                    success, message = self.controller.add_assignment(class_id, assignment_details, max_points)
                    messagebox.showinfo("Success", message if success else "Failed to add assignment")
                    self.on_class_selected(event=None)

    def edit_grade(self, event: tk.Event) -> None:
        '''
        Edit the grade of a student in the treeview
        
        Parameters:
            event (tk.Event): The event that triggered the function
            
            Returns:
                None
        '''
        region = self.grades_view.identify("region", event.x, event.y)
        if region == "cell":
            col_id = int(self.grades_view.identify_column(event.x).replace('#', '')) - 1
            row_id = self.grades_view.identify_row(event.y)
            if col_id > 0:
                self.update_grade(col_id, row_id)
    
    def update_grade(self, col_id: int, row_id: str) -> None:
        '''
        Update the grade of a student in the treeview
        
        Parameters:
            col_id (int): The id of the column in the treeview
            row_id (str): The id of the row in the treeview
            
            Returns:
                None
        '''
        current_value = self.grades_view.item(row_id, 'values')[col_id]
        new_grade = simpledialog.askinteger("Update Grade", "Enter new grade:", parent=self.master, initialvalue=current_value)
        if new_grade is not None and new_grade >= 0:
            student_name = self.grades_view.item(row_id, 'values')[0]
            assignment_name = self.grades_view.column("#{}".format(col_id + 1), option="id")
            self.check_and_update_grade(student_name, assignment_name, new_grade, row_id, col_id)
    
    def check_and_update_grade(self, student_name: str, assignment_name: str, new_grade: int, row_id: str, col_id: int) -> None:
        '''
        Check if the new grade is higher than the maximum points and ask for confirmation
        
        Parameters:
            student_name (str): The name of the student
            assignment_name (str): The name of the assignment
            new_grade (int): The new grade
            row_id (str): The id of the row in the treeview
            col_id (int): The id of the column in the treeview
            
            Returns:
                None
        '''
        max_points = self.controller.get_max_points(assignment_name)
        if new_grade > max_points:
            confirmation = messagebox.askyesno("Confirmation", "The new grade is higher than the maximum points. Do you want to proceed?", parent=self.master)
            if confirmation:
                self.update_grade_in_controller_and_view(student_name, assignment_name, new_grade, row_id, col_id)
        else:
            self.update_grade_in_controller_and_view(student_name, assignment_name, new_grade, row_id, col_id)
    
    def update_grade_in_controller_and_view(self, student_name: str, assignment_name: str, new_grade: int, row_id: str, col_id: int) -> None:
        '''
        Update the grade in the controller and the treeview

        Parameters:
            student_name (str): The name of the student
            assignment_name (str): The name of the assignment
            new_grade (int): The new grade
            row_id (str): The id of the row in the treeview
            col_id (int): The id of the column in the treeview

        Returns:
            None
        '''
        success = self.controller.update_grade(self.class_selection.get(), student_name, assignment_name, new_grade)
        if success:
            values = list(self.grades_view.item(row_id, 'values'))
            values[col_id] = new_grade
            self.grades_view.item(row_id, values=values)
            self.on_class_selected(event=None)
        else:
            messagebox.showinfo("Info", "Grade not updated.", parent=self.master)



if __name__ == "__main__":
    root = tk.Tk()
    app = GradebookApp(root)
    root.mainloop()