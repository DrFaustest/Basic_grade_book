
from typing import Dict, List
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from controller import GradebookController

class GradebookApp:
    """
    A GUI application for managing grades in a gradebook system.

    Attributes:
        master (tk.Tk): The root Tkinter window.
        controller (GradebookController): The controller object for managing gradebook data.
        label_welcome (tk.Label): The label widget for displaying a welcome message.
        label_instructions (tk.Label): The label widget for displaying instructions.
        class_selection (ttk.Combobox): The combobox widget for selecting a class.
        button_frame (tk.Frame): The frame widget for holding buttons.
        button_add_class (tk.Button): The button widget for adding a class.
        button_add_student (tk.Button): The button widget for adding a student.
        button_add_assignment (tk.Button): The button widget for adding an assignment.
        tree_frame (tk.Frame): The frame widget for holding the treeview.
        tree_scroll (tk.Scrollbar): The scrollbar widget for the treeview.
        grades_view (ttk.Treeview): The treeview widget for displaying grades.
    """

    def __init__(self, master: tk.Tk) -> None:
        """
        Initializes the GradebookApp.

        Args:
            master (tk.Tk): The root Tkinter window.
        """
        self.master = master
        master.title("Gradebook Application")
        self.controller = GradebookController()
        self.geometry = "800x600"
        master.geometry(self.geometry)
        
        self.label_welcome = tk.Label(master, text="Welcome to the Gradebook System", font=("Arial", 14))
        self.label_welcome.pack(pady=10)
        
        self.label_instructions = tk.Label(master, text="Select a or add a class and manage grades\nAdd students or assignments to the class\nDouble click on a grade to edit it\n", font=("Arial", 12))
        self.label_instructions.pack(pady=10)
        
        self.class_selection = ttk.Combobox(master, width=15, state='readonly')
        self.class_selection['values'] = self.controller.load_classes()
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
        
        self.tree_frame = tk.Frame(master)
        self.tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_treeview()

    def on_class_selected(self, event: tk.Event = None) -> None:
        """
        Event handler for when a class is selected from the combobox.

        Args:
            event (tk.Event, optional): The event object. Defaults to None.
        """
        class_id = self.class_selection.get()
        assignments = self.controller.load_assignments(class_id)
        self.update_treeview_columns(assignments)
        
        grades = self.controller.load_grades(class_id)
        self.grades_view.delete(*self.grades_view.get_children())
        
        for student, student_grades in grades.items():
            row_values = [student] + [student_grades.get(assignment, "") for assignment in assignments]
            self.grades_view.insert('', 'end', values=row_values)

    def setup_treeview(self) -> None:
        """
        Sets up the treeview widget for displaying grades.
        """
        self.tree_frame = tk.Frame(self.master)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree_scroll = tk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.grades_view = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, columns=[], show="headings")
        self.grades_view.pack(fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.grades_view.yview)

        self.grades_view.bind("<Double-1>", self.edit_grade)

    def edit_grade(self, event: tk.Event) -> None:
        """
        Event handler for editing a grade when a cell is double-clicked.

        Args:
            event (tk.Event): The event object.
        """
        region = self.grades_view.identify("region", event.x, event.y)
        if region == "cell":
            col_id = int(self.grades_view.identify_column(event.x).replace('#', '')) - 1
            row_id = self.grades_view.identify_row(event.y)
            if col_id > 0:
                current_value = self.grades_view.item(row_id, 'values')[col_id]
                new_grade = simpledialog.askinteger("Update Grade", "Enter new grade:", parent=self.master, initialvalue=current_value)
                if new_grade is not None:
                    student_name = self.grades_view.item(row_id, 'values')[0]
                    assignment_name = self.grades_view.column("#{}".format(col_id + 1), option="id")
                    self.controller.update_grade(self.class_selection.get(), student_name, assignment_name, new_grade)
                    values = list(self.grades_view.item(row_id, 'values'))
                    values[col_id] = new_grade
                    self.grades_view.item(row_id, values=values)

    def on_cell_click(self, event: tk.Event) -> None:
        """
        Event handler for when a cell in the treeview is clicked.

        Args:
            event (tk.Event): The event object.
        """
        row_id = self.grades_view.identify_row(event.y)
        column_id = self.grades_view.identify_column(event.x)
    
        cell_value = self.grades_view.item(row_id)['values'][int(column_id[1:]) - 1]
    
        print(f'You clicked on cell with value: {cell_value}')
    
    def update_treeview_columns(self, assignments: List[str]) -> None:
        """
        Updates the columns of the treeview based on the assignments.

        Args:
            assignments (List[str]): The list of assignment names.
        """
        self.grades_view["columns"] = ["Student Name"] + assignments
        self.grades_view.heading('#1', text='Student Name', anchor='w')
        for idx, assignment in enumerate(assignments, start=2):
            self.grades_view.column(f'#{idx}', anchor='center', width=100)
            self.grades_view.heading(f'#{idx}', text=assignment)
    
        self.grades_view.bind('<ButtonRelease-1>', self.on_cell_click)

    def add_class(self) -> None:
        """
        Event handler for adding a class.
        """
        class_name = simpledialog.askstring("Add Class", "Enter class name:")
        if class_name:
            success, message = self.controller.add_class(class_name)
            if success:
                self.class_selection['values'] = self.controller.load_classes()
                messagebox.showinfo("Success", "Class added successfully")
                self.on_class_selected()
            else:
                messagebox.showerror("Error", message)

    def add_student(self) -> None:
        """
        Event handler for adding a student.
        """
        class_id = self.class_selection.get()
        student_name = simpledialog.askstring("Add Student", "Enter student name:")
        if student_name:
            success, message = self.controller.add_student(class_id, student_name)
            if success:
                messagebox.showinfo("Success", message)
                self.on_class_selected()
            else:
                messagebox.showerror("Error", message)


    def add_assignment(self) -> None:
        """
        Event handler for adding an assignment.
        """
        class_id = self.class_selection.get()
        assignment_details = simpledialog.askstring("Add Assignment", "Enter assignment details:")
        if assignment_details:
            success, message = self.controller.add_assignment(class_id, assignment_details)
            messagebox.showinfo("Success", message if success else "Failed to add assignment")
            self.on_class_selected()

    def change_grade(self, row_id: str, column_id: str) -> None:
        """
        Changes the grade of a student for a specific assignment.

        Args:
            row_id (str): The ID of the row in the treeview.
            column_id (str): The ID of the column in the treeview.
        """
        selected_item = self.grades_view.focus()  
        if column_id == '#2':
            new_grade = simpledialog.askinteger("Update Grade", "Enter new grade:", parent=self.master)
            if new_grade is not None:
                values = self.grades_view.item(selected_item, 'values')
                student, assignment = values[0], values[int(column_id[1:]) - 1] 
                success = self.controller.update_grade(self.class_selection.get(), student, assignment, new_grade)
                if success:
                    self.grades_view.item(selected_item, values=(student, new_grade))

if __name__ == "__main__":
    root = tk.Tk()
    app = GradebookApp(root)
    root.mainloop()