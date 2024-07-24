from student import Student
from course import Course
import utils

class GradeBook:
    def __init__(self):
        self.student_file = 'data/students.csv'
        self.course_file = 'data/courses.csv'
        self.grades_file = 'data/grades.csv'
        self.students = {}
        self.courses = {}
        self._load_students()
        self._load_courses()
        self._load_grades()

    def _load_students(self):
        for s in utils.read_csv(self.student_file):
            student = Student(s['email'], s['names'])
            self.students[s['email']] = student

    def _load_courses(self):
        for c in utils.read_csv(self.course_file):
            self.courses[c['name']] = Course(c['name'], c['trimester'], int(c['credits']))

    def _load_grades(self):
        for g in utils.read_csv(self.grades_file):
            student = self.students.get(g['email'])
            if student:
                student.gpa = float(g.get('gpa', 0.0))
                if g.get('courses'):
                    for course_data in g['courses'].split(';'):
                        course_name, trimester, credits, grade = course_data.split(':')
                        student.register_for_course(course_name, trimester, int(credits), float(grade))

    def add_student(self, email, names):
        student = Student(email, names)
        self.students[email] = student
        self._write_students()
        self._write_grades()

    def add_course(self, name, trimester, credits):
        course = Course(name, trimester, credits)
        self.courses[name] = course
        self._write_courses()

    def register_student_for_course(self, email, course_name, trimester, credits, grade):
        student = self.students.get(email)
        if student:
            student.register_for_course(course_name, trimester, credits, grade)
            self._write_grades()

    def calculate_GPA(self, email):
        student = self.students.get(email)
        if student:
            gpa = student.calculate_GPA()
            self._write_grades()
            return gpa
        return None

    def calculate_ranking(self):
        for student in self.students.values():
            student.calculate_GPA()
        sorted_students = sorted(self.students.values(), key=lambda s: s.gpa, reverse=True)
        self._write_grades()
        return [(student.names, student.gpa) for student in sorted_students]

    def search_by_grade(self, course_name, grade):
        result = []
        for student in self.students.values():
            for course in student.courses_registered:
                if course['course_name'] == course_name and course['grade'] == grade:
                    result.append(student)
        return result

    def generate_transcript(self, email):
        student = self.students.get(email)
        if student:
            return {
                'name': student.names,
                'courses': student.courses_registered,
                'gpa': student.gpa
            }
        return None

    def _write_students(self):
        fieldnames = ['email', 'names']
        data = [{'email': s.email, 'names': s.names} for s in self.students.values()]
        utils.write_csv(self.student_file, data, fieldnames)

    def _write_courses(self):
        fieldnames = ['name', 'trimester', 'credits']
        data = [{'name': c.name, 'trimester': c.trimester, 'credits': c.credits} for c in self.courses.values()]
        utils.write_csv(self.course_file, data, fieldnames)

    def _write_grades(self):
        fieldnames = ['email', 'gpa', 'courses']
        data = []
        for student in self.students.values():
            student_data = {
                'email': student.email,
                'gpa': student.gpa,
                'courses': ';'.join([f"{c['course_name']}:{c['trimester']}:{c['credits']}:{c['grade']}" for c in student.courses_registered])
            }
            data.append(student_data)
        utils.write_csv(self.grades_file, data, fieldnames)

    def delete_student(self, email):
        if email in self.students:
            del self.students[email]
            self._write_students()
            self._write_grades()
            return True
        return False

    def update_student(self, email, new_names):
        if email in self.students:
            self.students[email].names = new_names
            self._write_students()
            return True
        return False

    def view_student_records(self, email=None):
        if email:
            student = self.students.get(email)
            if student:
                return {
                    'email': student.email,
                    'names': student.names,
                    'courses': student.courses_registered,
                    'gpa': student.gpa
                }
            return None
        else:
            return [
                {
                    'email': student.email,
                    'names': student.names,
                    'courses_count': len(student.courses_registered),
                    'gpa': student.gpa
                }
                for student in self.students.values()
            ]