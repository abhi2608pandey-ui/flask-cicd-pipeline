from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import certifi
import os

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

mongo = PyMongo()

if app.config["MONGO_URI"]:
    mongo.init_app(app, tlsCAFile=certifi.where())


@app.route("/health")
def health():
    """Health endpoint used by CI/CD deployment verification."""
    return jsonify({
        "status": "healthy",
        "service": "student-registration"
    }), 200


@app.route("/")
def index():
    """Home page - list all students."""
    students = mongo.db.students.find()
    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    """Add a new student."""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]

        mongo.db.students.insert_one({
            "name": name,
            "email": email,
            "course": course
        })

        return redirect(url_for("index"))

    return render_template("add_student.html")


@app.route("/update/<student_id>", methods=["GET", "POST"])
def update_student(student_id):
    """Update an existing student."""
    try:
        object_id = ObjectId(student_id)
    except Exception:
        return "Invalid student ID", 404

    student = mongo.db.students.find_one({"_id": object_id})

    if student is None:
        return "Student not found", 404

    if request.method == "POST":
        new_name = request.form["name"]
        new_email = request.form["email"]
        new_course = request.form["course"]

        mongo.db.students.update_one(
            {"_id": object_id},
            {
                "$set": {
                    "name": new_name,
                    "email": new_email,
                    "course": new_course
                }
            }
        )

        return redirect(url_for("index"))

    return render_template("update_student.html", student=student)


@app.route("/delete/<student_id>")
def delete_student(student_id):
    """Delete a student."""
    try:
        object_id = ObjectId(student_id)
    except Exception:
        return "Invalid student ID", 404

    result = mongo.db.students.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        return "Student not found", 404

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=False,
        port=5000
    )