# School Management System

## Overview
This School Management System is an educational management application designed to facilitate the management of grades within a school environment. It is built using Python with a Tkinter graphical user interface. The system allows for the management of classes, students, and their assignments and grades.

## Features
- **Dynamic Grade Management**: Manage grades dynamically across various classes with options to add classes, students, and assignments.
- **Data Persistence**: Utilizes JSON files for data storage, handling complex data structures that maintain class, student, and assignment information.
- **Interactive GUI**: The application features a responsive GUI for interaction with the grade data. Users can add, update, and query grade information through a structured interface.

## Installation
To run the School Management System, you need Python and Tkinter installed on your machine.

```bash
# Clone the repository
git clone https://github.com/DrFaustest/Basic_grade_book.git
# Navigate to the directory
cd school-management-system
# Install dependencies (if any)
pip install -r requirements.txt
# Execute the program
python view.py
```

## Usage
The application supports various functionalities through its GUI:

- **Adding Classes, Students, and Assignments** 
Through simple dialog inputs, you can add new classes, students, and assignments.
- **Grade Modifications** 
Directly click on a cell within the grade table to modify student grades for specific assignments.
- **Data Management** 
All data changes are saved in a local JSON file, ensuring that all information persists between sessions.


- **Data Structure**
The system uses a JSON file (data.json) to store the class, student, and assignment data in a structured format. This allows for easy manipulation and retrieval of data necessary for operation .