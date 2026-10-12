
import sqlite3


def create_database():

    connection = sqlite3.connect("student.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            course TEXT,
            year INTEGER,
            address TEXT
        )
    """)

    connection.commit()

    connection.close()


def add_student(name, email, phone, course, year, address):

    connection = sqlite3.connect("student.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, email, phone, course, year, address)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, phone, course, year, address))

    connection.commit()

    connection.close()



def email_exists(email, student_id=None):

    connection = sqlite3.connect("student.db")

    cursor = connection.cursor()

    if student_id is None:
        cursor.execute(
            "SELECT * FROM students WHERE email = ?",
            (email,)
        )
    else:
        cursor.execute(
            "SELECT * FROM students WHERE email = ? AND id != ?",
            (email, student_id)
        )

    student = cursor.fetchone()

    connection.close()

    return student is not None




def get_students(search=""):

    connection = sqlite3.connect("student.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ?
        OR email LIKE ?
        OR course LIKE ?
    """, (
        "%" + search + "%",
        "%" + search + "%",
        "%" + search + "%"
    ))

    students = cursor.fetchall()

    connection.close()

    return students


def get_student(student_id):

    connection = sqlite3.connect("student.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    connection.close()

    return student


def update_student(student_id, name, email, phone, course, year, address):

    connection = sqlite3.connect("student.db")

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?,
            email = ?,
            phone = ?,
            course = ?,
            year = ?,
            address = ?
        WHERE id = ?
    """, (
        name,
        email,
        phone,
        course,
        year,
        address,
        student_id
    ))

    connection.commit()

    connection.close()


def delete_student(student_id):

    connection = sqlite3.connect("student.db")

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()

    connection.close()



def get_dashboard_stats():

    connection = sqlite3.connect("student.db")

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT course) FROM students")
    total_courses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT year) FROM students")
    total_years = cursor.fetchone()[0]

    connection.close()

    return total_students, total_courses, total_years


create_database()