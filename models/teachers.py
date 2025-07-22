from init import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Teacher(db.Model):
    # __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(150))

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)