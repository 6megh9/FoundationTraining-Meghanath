import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Custom exception for database connection error
class DatabaseConnectionError(Exception):
    pass

# Custom exception for query execution error
class QueryExecutionError(Exception):
    pass

# Class representing the Student
class Student:
    def __init__(self, student_id, first_name, last_name, dob, email, phone_number):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.email = email
        self.phone_number = phone_number

# Class representing the Course
class Course:
    def __init__(self, course_id, course_name, course_code):
        self.course_id = course_id
        self.course_name = course_name
        self.course_code = course_code
        self.teacher = None

    def assign_teacher(self, teacher):
        self.teacher = teacher

    def update_course_info(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        if self.teacher:
            self.teacher.update_teacher_info(instructor, "", "")

    def display_course_info(self):
        print(f"Course ID: {self.course_id}")
        print(f"Course Name: {self.course_name}")
        print(f"Course Code: {self.course_code}")
        if self.teacher:
            print("Assigned Teacher:")
            self.teacher.display_teacher_info()

    def get_enrollments(self):
        # Implement logic to retrieve enrollments for the course from the database
        pass

    def get_teacher(self):
        return self.teacher

# Class representing the Enrollment
class Enrollment:
    def __init__(self, enrollment_id, student, course, enrollment_date):
        self.enrollment_id = enrollment_id
        self.student = student
        self.course = course
        self.enrollment_date = enrollment_date

    def get_student(self):
        return self.student

    def get_course(self):
        return self.course

# Class representing the Teacher
class Teacher:
    def __init__(self, teacher_id, name, email, expertise):
        self.teacher_id = teacher_id
        self.name = name
        self.email = email
        self.expertise = expertise

    def update_teacher_info(self, name, email, expertise):
        self.name = name
        self.email = email
        self.expertise = expertise

    def display_teacher_info(self):
        print(f"Teacher ID: {self.teacher_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Expertise: {self.expertise}")

    def get_assigned_courses(self):
        # Implement logic to retrieve assigned courses for the teacher from the database
        pass

# Class representing the Payment
class Payment:
    def __init__(self, payment_id, student, amount, payment_date):
        self.payment_id = payment_id
        self.student = student
        self.amount = amount
        self.payment_date = payment_date

    def get_student(self):
        return self.student

    def get_payment_amount(self):
        return self.amount

    def get_payment_date(self):
        return self.payment_date

# Class representing the SIS (Student Information System)
class SIS:
    def __init__(self, connection):
        self.connection = connection

    def enroll_student_in_course(self, student, course):
        # Implement logic to enroll a student in a course (add an enrollment record to the database)
        pass

    def assign_teacher_to_course(self, teacher, course):
        course.assign_teacher(teacher)

    def record_payment(self, student, amount):
        # Implement logic to record a payment made by a student (add a payment record to the database)
        pass

    def generate_enrollment_report(self, course):
        # Implement logic to generate an enrollment report for a specific course
        pass

    def generate_payment_report(self, student):
        # Implement logic to generate a payment report for a specific student
        pass

    def calculate_course_statistics(self, course):
        # Implement logic to calculate statistics for a specific course
        pass

# Database connection
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root",
        database="day"
    )

    if connection.is_connected():
        print("Connected to the database")
    else:
        print("Unable to connect to the database")
except Error as e:
    print(f"Database Connection Error: {e}")

# Example usage
try:
    sis = SIS(connection)

    # Example student, course, and teacher data
    john_doe = Student(student_id=101, first_name="John", last_name="Doe", dob="1995-08-15",
                       email="john.doe@example.com", phone_number="123-456-7890")

    intro_to_programming = Course(course_id=1, course_name="Introduction to Programming", course_code="CS101")
    python_expert = Teacher(teacher_id=201, name="Python Expert", email="python.expert@example.com", expertise="Python")

    # Enroll the student in the course
    sis.enroll_student_in_course(john_doe, intro_to_programming)

    # Assign the teacher to the course
    sis.assign_teacher_to_course(python_expert, intro_to_programming)

    # Record a payment made by the student
    sis.record_payment(john_doe, amount=500.00)

    # Display course information
    intro_to_programming.display_course_info()

    # Example reports and statistics
    sis.generate_enrollment_report(intro_to_programming)
    sis.generate_payment_report(john_doe)
    sis.calculate_course_statistics(intro_to_programming)

except DatabaseConnectionError:
    print("Unable to connect to the database. Check your connection parameters.")
except QueryExecutionError:
    print("Error executing the query.")
finally:
    # Close the connection in the finally block to ensure it's closed even if an exception occurs
    if connection.is_connected():
        connection.close()
        print("Connection closed")
