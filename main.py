# import dependencies
from fastapi import FastAPI, status, HTTPException
from uuid import UUID

# initiate fastapi
app = FastAPI()


# local DB is an empty dict
students: dict = {}

# dummy dict to store a new student record
student_schema = {"id": "", "name": "", "age": 0, "sex": "", "height": 0.0}


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return "Welcome to Mikael API"


# retrieve all students resource
@app.get("/students", status_code=status.HTTP_200_OK)
def get_students():
    return students


# retrieve a single student resource
@app.get("/students/{id}", status_code=status.HTTP_200_OK)
def get_student_by_id(id: str):
    student = find_student(id, students)
    return student


# create student resource
@app.post("/students", status_code=status.HTTP_200_OK)
def create_student(
    name: str, age: int, sex: str, height: float
):
    new_record = student_schema.copy()
    new_record["id"] = str(UUID(int=len(students) + 1))
    new_record["name"] = name
    new_record["age"] = age
    new_record["sex"] = sex
    new_record["height"] = height

    students[new_record["id"]] = new_record

    return {"message": "Student created successfully", "data": new_record}



#update student record resource
@app.put("/students/{id}", status_code=status.HTTP_200_OK)
def update_student(
    id: str, name: str, age: int, sex: str, height: float
):
    student = find_student(id, students)
    student["name"] = name
    student["age"] = age
    student["sex"] = sex
    student["height"] = height

    return {"message": "Student updated successfully", "data": student}



# delete a student resource
@app.delete("/students/{id}")
def delete_student(id: str):
    student = find_student(id, students)
    del students[id]
    return {"message": "Student deleted successfully"}


# utility function to get student and throw error if not found
def find_student(id: str, students: dict):
    student = students.get(id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )

    return student