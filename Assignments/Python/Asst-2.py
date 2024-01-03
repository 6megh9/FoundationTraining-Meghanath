import mysql.connector
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

    def update_course_info(self, course_code, course_name, instructor):
        self.course_code = course_code
        self.course_name = course_name
        if self.teacher:
            self.teacher.name = instructor

    def display_course_info(self):
        print(f"Course ID: {self.course_id}")
        print(f"Course Code: {self.course_code}")
        print(f"Course Name: {self.course_name}")
        if self.teacher:
            print(f"Instructor: {self.teacher.name}")

    def get_enrollments(self, connection):
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM enrollments WHERE course_id = {self.course_id}"
            cursor.execute(query)
            enrollments = cursor.fetchall()
            return enrollments
        except mysql.connector.Error as e:
            print(f"Query Execution Error: {e}")
            raise QueryExecutionError(e)
        finally:
            if cursor:
                cursor.close()

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

    def get_assigned_courses(self, connection):
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM courses WHERE teacher_id = {self.teacher_id}"
            cursor.execute(query)
            assigned_courses = cursor.fetchall()
            return assigned_courses
        except mysql.connector.Error as e:
            print(f"Query Execution Error: {e}")
            raise QueryExecutionError(e)
        finally:
            if cursor:
                cursor.close()

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
    def __init__(self):
        self.students = []
        self.courses = []
        self.teachers = []
        self.payments = []

    def enroll_student_in_course(self, student, course, enrollment_date, connection):
        try:
            cursor = connection.cursor()

            # Check if the student and course exist
            check_student_query = f"SELECT * FROM students WHERE student_id = {student.student_id}"
            cursor.execute(check_student_query)
            existing_student = cursor.fetchone()

            check_course_query = f"SELECT * FROM courses WHERE course_id = {course.course_id}"
            cursor.execute(check_course_query)
            existing_course = cursor.fetchone()

            if existing_student and existing_course:
                # Insert enrollment record
                insert_enrollment_query = f"INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES " \
                                          f"({student.student_id}, {course.course_id}, '{enrollment_date}')"
                cursor.execute(insert_enrollment_query)

                connection.commit()
                print(f"Student {student.first_name} {student.last_name} enrolled in {course.course_name}")
            else:
                print("Student or course does not exist.")

        except QueryExecutionError:
            print("Error executing the query.")
        finally:
            if cursor:
                cursor.close()

    def assign_teacher_to_course(self, teacher, course, connection):
        try:
            cursor = connection.cursor()

            # Check if the teacher and course exist
            check_teacher_query = f"SELECT * FROM teachers WHERE teacher_id = {teacher.teacher_id}"
            cursor.execute(check_teacher_query)
            existing_teacher = cursor.fetchone()

            check_course_query = f"SELECT * FROM courses WHERE course_id = {course.course_id}"
            cursor.execute(check_course_query)
            existing_course = cursor.fetchone()

            if existing_teacher and existing_course:
                # Update course record with teacher information
                update_course_query = f"UPDATE courses SET teacher_id = {teacher.teacher_id} WHERE course_id = {course.course_id}"
                cursor.execute(update_course_query)

                connection.commit()
                print(f"Teacher {teacher.name} assigned to {course.course_name}")
            else:
                print("Teacher or course does not exist.")

        except QueryExecutionError:
            print("Error executing the query.")
        finally:
            if cursor:
                cursor.close()

    def record_payment(self, student, amount, payment_date, connection):
        try:
            cursor = connection.cursor()

            # Check if the student exists
            check_student_query = f"SELECT * FROM students WHERE student_id = {student.student_id}"
            cursor.execute(check_student_query)
            existing_student = cursor.fetchone()

            if existing_student:
                # Insert payment record
                insert_payment_query = f"INSERT INTO payments (student_id, amount, payment_date) VALUES " \
                                       f"({student.student_id}, {amount}, '{payment_date}')"
                cursor.execute(insert_payment_query)

                connection.commit()
                print(f"Payment recorded for {student.first_name} {student.last_name}")
            else:
                print("Student does not exist.")

        except QueryExecutionError:
            print("Error executing the query.")
        finally:
            if cursor:
                cursor.close()

    def generate_enrollment_report(self, course, connection):
        enrollments = course.get_enrollments(connection)
        if enrollments:
            print(f"Enrollment Report for {course.course_name}:")
            for enrollment in enrollments:
                student_id = enrollment[1]
                enrollment_date = enrollment[3]
                student = next((s for s in self.students if s.student_id == student_id), None)
                if student:
                    print(f"Student: {student.first_name} {student.last_name}, Enrollment Date: {enrollment_date}")
        else:
            print(f"No enrollments found for {course.course_name}")

    def generate_payment_report(self, student, connection):
        payments = [p for p in self.payments if p.get_student().student_id == student.student_id]
        if payments:
            print(f"Payment Report for {student.first_name} {student.last_name}:")
            for payment in payments:
                amount = payment.get_payment_amount()
                payment_date = payment.get_payment_date()
                print(f"Amount: {amount}, Payment Date: {payment_date}")
        else:
            print(f"No payments found for {student.first_name} {student.last_name}")

    def calculate_course_statistics(self, course, connection):
        enrollments = course.get_enrollments(connection)
        total_enrollments = len(enrollments)
        total_payments = sum([p.get_payment_amount() for p in self.payments if p.get_student().student_id in [e[1] for e in enrollments]])

        print(f"Statistics for {course.course_name}:")
        print(f"Total Enrollments: {total_enrollments}")
        print(f"Total Payments: {total_payments}")

# Example usage
try:
    # Connect to the database
    connection = create_connection()

    # Example student, course, teacher, and payment data
    john_doe = Student(student_id=101, first_name="John", last_name="Doe", dob="1995-08-15",
                       email="john.doe@example.com", phone_number="123-456-7890")

    intro_to_programming = Course(course_id=1, course_name="Introduction to Programming", course_code="CS101")

    math_teacher = Teacher(teacher_id=201, name="Math Teacher", email="math.teacher@example.com", expertise="Mathematics")

    january_payment = Payment(payment_id=301, student=john_doe, amount=500.00, payment_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Example SIS (Student Information System) instance
    sis = SIS()
    sis.students.append(john_doe)
    sis.courses.append(intro_to_programming)
    sis.teachers.append(math_teacher)
    sis.payments.append(january_payment)

    # Enroll the student in the course
    enrollment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sis.enroll_student_in_course(john_doe, intro_to_programming, enrollment_date, connection)

    # Assign the teacher to the course
    intro_to_programming.assign_teacher(math_teacher)

    # Record a payment
    sis.record_payment(john_doe, 300.00, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), connection)

    # Generate reports
    sis.generate_enrollment_report(intro_to_programming, connection)
    sis.generate_payment_report(john_doe, connection)

    # Calculate course statistics
    sis.calculate_course_statistics(intro_to_programming, connection)

except DatabaseConnectionError:
    print("Unable to connect to the database. Check your connection parameters.")
except QueryExecutionError:
    print("Error executing the query.")
finally:
    # Close the connection in a finally block to ensure it's closed even if an exception occurs
    if connection:
        connection.close()
