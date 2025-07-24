# Creating an LMS app with entities

- Student
- Teacher
- Courses
- Enrollments: Junction table

## Setup

To run server successfully, here are the steps you need to perform:

- Create a .env file with the variables included in .env.example
  - DATABASE_URI with a connection string to your chosen database eg. postgres

- ensure that a local database exists by making one in the postgres shell
  - enter the postgres shell
    - MacOS: run the `psql` command
    - Linux & WSL: run the `sudo -u postgres psql` command
  - list all existing databases by running `\l`
  - if the database you want to use does not currently exist, create it by running `CREATE DATABASE lms_db;`
  - check that it exists by running `\l` again
  - connect to the database you want to use with `\c lms_db`
- ensure that a postgres shell user that has permissions to work with your database
  - in the postgres shell, run `CREATE USER lms_dev WITH PASSWORD '123456';`
  - grant the user the permissions needed to work with the database, run `GRANT ALL PRIVILEGES ON DATABASE lms_db TO lms_dev;`
  - grant db schema permissions to the user as well, run `GRANT ALL ON SCHEMA public TO lms_dev;`
- exit the postgres shell with `\q`

- Set up a virtual environment by following the below:
  - run `python3 -m venv .venv` to make the venv
    - MacOS, Linux & WSL: `source .venv/bin/activate`
    - Windows: `.venv/Scripts/activate`
  - set the VSCode Python interpreter to the venv Python library:
    - CTRL+SHIFT+P to open the command palette
    - choose the interpreter with the path that matches ".venv" path
- Install depenencies from the project within the activated venv:
  - Run `pip install -r ./requirements.txt`

- ensure that the flask app database exists and has any seed data required
  - check the source code for any cli commands, e.g. `./controllers/cli_controller.py`
  - run the following commands in order to drop tables, create tables and seed created tables

- Create a .flaskenv file with the variables included in .flaskenv.example
- flask run to run the server

## API Endpoints

|Endpoint                 |  Methods  |   Rule |
|------------------------- | ---------- | --------------------------|
|student.create_student     |POST |       /students/                |
|student.delete_student     |DELETE|      /students/<int:student_id>|
|student.get_student_by_id  |GET    |     /students/<int:student_id>|
|student.get_students       |GET     |    /students/                |
|student.update_student     |PATCH, PUT|  /students/<int:student_id>|