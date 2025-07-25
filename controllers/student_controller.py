from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
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
def get_student_by_id(student_id):
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
    try:
        body_data = request.get_json()

        new_student = Student(
            name=body_data.get("name"),
            email=body_data.get("email"),
            address=body_data.get("address")
        )

        db.session.add(new_student)
        db.session.commit()

        return jsonify(student_schema.dump(new_student)), 201
    
    except IntegrityError as err:
        match err.orig.pgcode:
            case errorcodes.NOT_NULL_VIOLATION:
                return jsonify({"message": f"Required field {err.orig.diag.column_name} cannot be null."}), 400
            case errorcodes.UNIQUE_VIOLATION:
                return jsonify({"message": f"Email must be unique."}), 400


# PUT/PATCH /id
@students_bp.route('/<int:student_id>', methods=["PUT", "PATCH"])
def update_student(student_id):
    stmt = db.select(Student).where(Student.id==student_id)
    student=db.session.scalar(stmt)

    if student:
        body_data = request.get_json()

        student.name = body_data.get("name", student.name)
        student.address = body_data.get("address", student.address)
        student.email = body_data.get("email", student.email)

        db.session.commit()
        return jsonify(student_schema.dump(student))
    
    else: 
        return jsonify({"message": f"Student with id {student_id} does not exist."}), 404

# DELETE /id
@students_bp.route('/<int:student_id>', methods=["DELETE"])
def delete_student(student_id):
    stmt = db.select(Student).where(Student.id==student_id)
    student = db.session.scalar(stmt)

    # data = student_schema.dump(student)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": f"Student '{student.name}' was removed successfully."}),201
    else:
        return jsonify({"message": f"Student with id '{student_id}' does not exist."}), 404