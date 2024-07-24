class Student:
    def __init__(self, email, names):
        self.email = email
        self.names = names
        self.courses_registered = []
        self.gpa = 0.0

    def calculate_GPA(self):
        if not self.courses_registered:
            self.gpa = 0.0
            return self.gpa
        total_points = sum(course['grade'] * course['credits'] for course in self.courses_registered)
        total_credits = sum(course['credits'] for course in self.courses_registered)
        self.gpa = total_points / total_credits
        return self.gpa

    def register_for_course(self, course_name, trimester, credits, grade):
        self.courses_registered.append({
            'course_name': course_name,
            'trimester': trimester,
            'credits': credits,
            'grade': grade
        })
        self.calculate_GPA()