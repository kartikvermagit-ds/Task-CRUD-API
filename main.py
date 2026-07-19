from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks.",
    version="1.0"
)

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


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


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }

    tasks.append(new_task)
    return new_task