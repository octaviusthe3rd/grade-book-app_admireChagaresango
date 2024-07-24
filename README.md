# Grade Book Application

### Description
Grade Book Application is a menu driven app that manages student records, including courses and grade for an educational institution.

### Features
1. Add, update and delete student records
2. Add course information
3. Register students for any course and record student grades
4. Calculate each student's GPA
5. Student rankings based on GPA
6. Search for students by course taken and by grade
7. Generate student transcripts
8. View individual or all student records


### Setup
1. Clone this repository.
2. Navigate to the project directory.
3. Install required dependencies (if any) using:

pip install -r requirements.txt


### Executing the application
Run the application by executing:

python main.py


### Dependencies
- Python3
- CSV module (built-in)


### Prerequisites
- Colorama


### File Structure
- "main.py": Main entry point of the application
- "gradebook.py": Contains the GradeBook class, along with the majority of functions driving the application
- "student.py": Defines the Student class
- "course.py": Defines the Course class
- "auth.py": Handles user authentication
- "utils.py": Contains utility functions for file operations in this case CSV utilities