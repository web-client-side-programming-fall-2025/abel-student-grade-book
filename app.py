from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

students = set()
grades_by_student = {}

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/students", methods=["GET", "POST"])
def students_page():
    if request.method == "POST":
        name = request.form.get("student_name", "").strip()
        grade_str = request.form.get("grade", "").strip()

        if not name or not grade_str:
            return redirect(url_for("students_page"))

        try:
            grade = float(grade_str)
        except ValueError:
            return redirect(url_for("students_page"))

        students.add(name)
        grades_by_student.setdefault(name, []).append(grade)
        return redirect(url_for("students_page"))

    table_rows = []
    for name in sorted(students):
        grades = grades_by_student.get(name, [])
        table_rows.append({"name": name, "grades": grades})

    return render_template("students.html", rows=table_rows)

@app.route("/averages")
def averages_page():
    averages = []
    for name in sorted(students):
        grades = grades_by_student.get(name, [])
        avg = sum(grades) / len(grades) if grades else None
        averages.append({"name": name, "average": avg})

    return render_template("averages.html", averages=averages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
 
