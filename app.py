
import re

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from database import (
    create_database,
    add_student,
    get_students,
    get_student,
    update_student,
    delete_student,
    get_dashboard_stats,
    email_exists
)


app = Flask(__name__)

app.secret_key = "student-management-secret-key"

create_database()


# -------------------------
# Dashboard
# -------------------------

@app.route("/")
def home():

    total_students, total_courses, total_years = get_dashboard_stats()

    return render_template(
        "index.html",
        total_students=total_students,
        total_courses=total_courses,
        total_years=total_years
    )


# -------------------------
# View and Search Students
# -------------------------

@app.route("/students")
def students():

    search = request.args.get("search", "").strip()

    student_list = get_students(search)

    return render_template(
        "students.html",
        students=student_list
    )


# -------------------------
# Add Student
# -------------------------

@app.route("/add-student", methods=["GET", "POST"])
def add_student_page():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        course = request.form.get("course", "").strip()
        year = request.form.get("year", "").strip()
        address = request.form.get("address", "").strip()

        # Validate name
        if name == "":
            flash("Name cannot be empty!", "error")
            return redirect(url_for("add_student_page"))

        # Validate email
        if email == "":
            flash("Email cannot be empty!", "error")
            return redirect(url_for("add_student_page"))

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            flash("Please enter a valid email address!", "error")
            return redirect(url_for("add_student_page"))

        # Check duplicate email
        if email_exists(email):
            flash("A student with this email already exists!", "error")
            return redirect(url_for("add_student_page"))

        # Validate phone
        if phone != "" and not re.fullmatch(r"[0-9]{10}", phone):
            flash("Phone number must contain exactly 10 digits!", "error")
            return redirect(url_for("add_student_page"))

        # Validate course
        if course == "":
            flash("Course is required!", "error")
            return redirect(url_for("add_student_page"))

        # Validate year
        if year == "":
            flash("Year is required!", "error")
            return redirect(url_for("add_student_page"))

        try:
            year = int(year)

            if year < 1 or year > 4:
                flash("Year must be between 1 and 4!", "error")
                return redirect(url_for("add_student_page"))

        except ValueError:
            flash("Year must be a number!", "error")
            return redirect(url_for("add_student_page"))

        # Save student
        add_student(
            name,
            email,
            phone,
            course,
            year,
            address
        )

        flash("Student added successfully!", "success")

        return redirect(url_for("students"))

    return render_template("add_student.html")


# -------------------------
# Edit Student
# -------------------------

@app.route("/edit-student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    student = get_student(student_id)

    if student is None:
        return "Student not found!", 404

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        course = request.form.get("course", "").strip()
        year = request.form.get("year", "").strip()
        address = request.form.get("address", "").strip()

        # Validate name
        if name == "":
            flash("Name cannot be empty!", "error")
            return redirect(url_for("edit_student", student_id=student_id))

        # Validate email
        if email == "":
            flash("Email cannot be empty!", "error")
            return redirect(url_for("edit_student", student_id=student_id))

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            flash("Please enter a valid email address!", "error")
            return redirect(url_for("edit_student", student_id=student_id))

        # Validate phone
        if phone != "" and not re.fullmatch(r"[0-9]{10}", phone):
            flash("Phone number must contain exactly 10 digits!", "error")
            return redirect(url_for("edit_student", student_id=student_id))

        # Check duplicate email, excluding the current student
        if email_exists(email, student_id):
            flash(
                "This email is already registered to another student!",
                "error"
            )
            return redirect(url_for("edit_student", student_id=student_id))

        # Validate course
        if course == "":
            flash("Course is required!", "error")
            return redirect(url_for("edit_student", student_id=student_id))

        # Validate year
        if year == "":
            flash("Year is required!", "error")
            return redirect(url_for("edit_student", student_id=student_id))

        try:
            year = int(year)

            if year < 1 or year > 4:
                flash("Year must be between 1 and 4!", "error")
                return redirect(url_for("edit_student", student_id=student_id))

        except ValueError:
            flash("Year must be a number!", "error")
            return redirect(url_for("edit_student", student_id=student_id))

        # Update student
        update_student(
            student_id,
            name,
            email,
            phone,
            course,
            year,
            address
        )

        flash("Student updated successfully!", "success")

        return redirect(url_for("students"))

    return render_template(
        "edit_student.html",
        student=student
    )


# -------------------------
# Delete Student
# -------------------------

@app.route("/delete-student/<int:student_id>")
def delete_student_page(student_id):

    student = get_student(student_id)

    if student is None:
        return "Student not found!", 404

    delete_student(student_id)

    flash("Student deleted successfully!", "success")

    return redirect(url_for("students"))


# -------------------------
# Run Application
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
