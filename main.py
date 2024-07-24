from gradebook import GradeBook
from auth import Auth
import os
import time
from colorama import init, Fore, Style

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + f"{title:^60}")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)

def print_menu(options):
    for i, option in enumerate(options, 1):
        print(Fore.GREEN + f"{i}. {option}")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)

def get_input(prompt):
    return input(Fore.YELLOW + f"{prompt}: " + Style.RESET_ALL)

def print_success(message):
    print(Fore.GREEN + Style.BRIGHT + message)

def print_error(message):
    print(Fore.RED + Style.BRIGHT + message)

def display_student_record(student):
    print(Fore.CYAN + f"Name: {student['names']}")
    print(Fore.CYAN + f"Email: {student['email']}")
    print(Fore.CYAN + f"GPA: {student['gpa']:.2f}")
    print(Fore.CYAN + "Courses:")
    for course in student['courses']:
        print(Fore.CYAN + f"  - {course['course_name']}: Grade {course['grade']}, Credits {course['credits']}")

def main():
    auth = Auth()
    
    while True:
        print_header("Welcome to the Grade Book Application")
        print_menu(["Login", "Exit"])
        choice = get_input("Choose an action")
        
        if choice == '1' and auth.login():
            break
        elif choice == '2':
            print_success("Exiting...")
            return
        else:
            print_error("Invalid choice. Please try again.")
        time.sleep(1)

    gradebook = GradeBook()

    while True:
        print_header("Grade Book Application")
        print_menu([
            "Add Student", "Update Student", "Delete Student", "View Student Records",
            "Add Course", "Register Student for Course",
            "Calculate GPA", "Student Ranking", "Search by Grade",
            "Generate Transcript", "Register New User", "Exit"
        ])
        choice = get_input("Choose an action")

        if choice == '1':
            email = get_input("Enter student email")
            names = get_input("Enter student names")
            gradebook.add_student(email, names)
            print_success("Student added successfully!")
        elif choice == '2':
            email = get_input("Enter student email to update")
            new_names = get_input("Enter new names for the student")
            if gradebook.update_student(email, new_names):
                print_success("Student updated successfully!")
            else:
                print_error("Student not found.")
        elif choice == '3':
            email = get_input("Enter student email to delete")
            if gradebook.delete_student(email):
                print_success("Student deleted successfully!")
            else:
                print_error("Student not found.")
        elif choice == '4':
            print_header("View Student Records")
            print_menu(["View All Students", "View Specific Student", "Back to Main Menu"])
            sub_choice = get_input("Choose an option")
            
            if sub_choice == '1':
                students = gradebook.view_student_records()
                print_header("All Students")
                for student in students:
                    print(Fore.CYAN + f"Name: {student['names']}, Email: {student['email']}, "
                          f"Courses: {student['courses_count']}, GPA: {student['gpa']:.2f}")
            elif sub_choice == '2':
                email = get_input("Enter student email")
                student = gradebook.view_student_records(email)
                if student:
                    print_header(f"Student Record: {student['names']}")
                    display_student_record(student)
                else:
                    print_error("Student not found.")
            elif sub_choice == '3':
                continue
            else:
                print_error("Invalid choice. Returning to main menu.")
        elif choice == '5':
            name = get_input("Enter course name")
            trimester = get_input("Enter trimester")
            credits = int(get_input("Enter course credits"))
            gradebook.add_course(name, trimester, credits)
            print_success("Course added successfully!")
        elif choice == '6':
            email = get_input("Enter student email")
            course_name = get_input("Enter course name")
            trimester = get_input("Enter trimester")
            credits = int(get_input("Enter course credits"))
            grade = float(get_input("Enter grade"))
            gradebook.register_student_for_course(email, course_name, trimester, credits, grade)
            print_success("Student registered for course successfully!")
        elif choice == '7':
            email = get_input("Enter student email")
            gpa = gradebook.calculate_GPA(email)
            if gpa is not None:
                print_success(f"Student GPA: {gpa:.2f}")
            else:
                print_error("Student not found.")
        elif choice == '8':
            ranking = gradebook.calculate_ranking()
            print_header("Student Ranking")
            for rank, (name, gpa) in enumerate(ranking, start=1):
                print(Fore.CYAN + f"{rank}. {name}: {gpa:.2f}")
        elif choice == '9':
            course_name = get_input("Enter course name")
            grade = float(get_input("Enter grade"))
            students = gradebook.search_by_grade(course_name, grade)
            print_header("Students with the specified grade")
            for student in students:
                print(Fore.CYAN + student.names)
        elif choice == '10':
            email = get_input("Enter student email")
            transcript = gradebook.generate_transcript(email)
            if transcript:
                print_header(f"Transcript for {transcript['name']}")
                for course in transcript['courses']:
                    print(Fore.CYAN + f"Course: {course['course_name']}, Grade: {course['grade']}, Credits: {course['credits']}")
                print_success(f"GPA: {transcript['gpa']:.2f}")
            else:
                print_error("Student not found.")
        elif choice == '11':
            if auth.register():
                print_success("New user registered successfully!")
            else:
                print_error("Registration failed. Please try again.")
        elif choice == '12':
            print_success("Exiting...")
            break
        else:
            print_error("Invalid choice. Please try again.")
        
        input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    main()