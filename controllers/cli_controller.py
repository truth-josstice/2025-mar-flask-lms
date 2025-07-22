from flask import Blueprint
from init import db
from models.students import Student
from models.teachers import Teacher

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_table():
    db.create_all()
    print("tables created...")


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("tables dropped...")

@db_commands.cli.command("seed")
def seed_tables():
    student = [
        Student(
            name="Alice",
            email="alice@email.com",
            address="Sydney"
        ),

        Student(
            name="Bob",
            email="bob@email.com",
            address="Melbourne"
        )
    ]
    db.session.add_all(student)

    teachers = [
        Teacher(
            name="Teacher A",
            department="Science",
            address="Sydney"
        ), 
        Teacher(
            name="Teacher B",
            department="Management",
            address="Perth"
        )
    ]
    db.session.add_all(teachers)

    db.session.commit()
    print("tables seeded...")