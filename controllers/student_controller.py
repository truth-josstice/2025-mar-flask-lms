from flask import Blueprint, jsonify, request
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
@students_bp.route('/<int:student_id>')
def get_student(student_id):
    stmt = db.select(Student).where(Student.id==student_id)
    student = db.session.scalar(stmt)
    
    if student:
        data = student_schema.dump(student)
        return jsonify(data)
    
    else:
        return jsonify({"message": f"Student with id {student_id} not found."}), 404
    
# POST /
@students_bp.route('/', methods=["POST"])
def create_student():
    body_data = request.get_json()

    new_student = Student(
        name=body_data.get("name"),
        email=body_data.get("email"),
        address=body_data.get("address")
    )

    db.session.add(new_student)
    db.session.commit()

    return jsonify(student_schema.dump(new_student)), 201


# PUT/PATCH /id
# @students_bp.route('/<int:student_id>', methods=["PUT", "PATCH"])
# def update_student(student_id):
#     body_date = request.get_json()

# DELETE /id