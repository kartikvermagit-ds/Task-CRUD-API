from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks.",
    version="1.0"
)


# -------------------------
# Pydantic Models
# -------------------------

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False


class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


# -------------------------
# In-Memory Database
# -------------------------

tasks = [
    {
        "id": 1,
        "title": "Study FastAPI",
        "description": "Complete FastAPI tutorial",
        "completed": False
    },
    {
        "id": 2,
        "title": "Learn Git",
        "description": "Practice Git commands",
        "completed": False
    },
    {
        "id": 3,
        "title": "Complete Assignment",
        "description": "Finish FlyRank Week 2",
        "completed": True
    }
]


# -------------------------
# Root Endpoint
# -------------------------

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/health",
            "/tasks"
        ]
    }


# -------------------------
# Health Check
# -------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -------------------------
# Get All Tasks
# -------------------------

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return tasks


# -------------------------
# Get Task By ID
# -------------------------

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# -------------------------
# Create Task
# -------------------------

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }

    tasks.append(new_task)

    return new_task


# -------------------------
# Update Task
# -------------------------

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: TaskCreate):

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["description"] = updated_task.description
            task["completed"] = updated_task.completed

            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# -------------------------
# Delete Task
# -------------------------

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)

            return {
                "message": "Task deleted successfully",
                "task": deleted_task
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )