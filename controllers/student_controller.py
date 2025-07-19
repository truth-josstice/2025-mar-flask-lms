from flask import Blueprint, jsonify
from init import db
from models.students import Student, student_schema, students_schema

students_bp = Blueprint("student", __name__, url_prefix="/students")

# Routes
# GET /
@students_bp.route('/')
def get_students():
    stmt = db.select(Student)
    students_list = db.session.scalars(stmt) # Python object
    data = students_schema.dump(students_list) # JavaScript JSON object
    
    if data:
        return jsonify(data)
    else:
        return jsonify({"message": "No student records found."}), 404
        

# GET /id
# POST /
# PUT/PATCH /id
# DELETE /id