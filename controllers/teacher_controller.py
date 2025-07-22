from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from init import db
from models.teachers import Teacher, teacher_schema, teachers_schema

teachers_bp = Blueprint("teacher", __name__, url_prefix="/teachers")

# Routes
# GET /
@teachers_bp.route('/')
def get_teachers():
    stmt = db.select(Teacher)
    teachers_list = db.session.scalars(stmt) # Python object
    data = teachers_schema.dump(teachers_list) # JavaScript JSON object
    
    if data:
        return jsonify(data)
    else:
        return jsonify({"message": "No teacher records found."}), 404
        

# GET /id
@teachers_bp.route('/<int:teacher_id>')
def get_teacher_by_id(teacher_id):
    stmt = db.select(Teacher).where(Teacher.id==teacher_id)
    teacher = db.session.scalar(stmt)
    
    if teacher:
        data = teacher_schema.dump(teacher)
        return jsonify(data)
    
    else:
        return jsonify({"message": f"Teacher with id {teacher_id} not found."}), 404
    
# POST /
@teachers_bp.route('/', methods=["POST"])
def create_teacher():
    try:
        body_data = request.get_json()

        new_teacher = Teacher(
            name=body_data.get("name"),
            department=body_data.get("department"),
            address=body_data.get("address")
        )

        db.session.add(new_teacher)
        db.session.commit()

        return jsonify(teacher_schema.dump(new_teacher)), 201
    
    except IntegrityError as err:
        match err.orig.pgcode:
            case errorcodes.NOT_NULL_VIOLATION:
                return jsonify({"message": f"Required field {err.orig.diag.column_name} cannot be null."}), 400
    except:
        return {"message": "An unknown error occured."}, 400


# PUT/PATCH /id
@teachers_bp.route('/<int:teacher_id>', methods=["PUT", "PATCH"])
def update_Teacher(teacher_id):
    stmt = db.select(Teacher).where(Teacher.id==teacher_id)
    teacher=db.session.scalar(stmt)

    if teacher:
        body_data = request.get_json()

        teacher.name = body_data.get("name", teacher.name)
        teacher.address = body_data.get("address", teacher.address)
        teacher.department = body_data.get("department", teacher.department)

        db.session.commit()
        return jsonify(teacher_schema.dump(teacher))
    
    else: 
        return jsonify({"message": f"Teacher with id {teacher_id} does not exist."}), 404

# DELETE /id
@teachers_bp.route('/<int:Teacher_id>', methods=["DELETE"])
def delete_Teacher(teacher_id):
    stmt = db.select(Teacher).where(Teacher.id==teacher_id)
    teacher = db.session.scalar(stmt)

    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return jsonify({"message": f"Teacher '{teacher.name}' was removed successfully."}),201
    else:
        return jsonify({"message": f"Teacher with id '{teacher_id}' does not exist."}), 404