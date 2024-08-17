import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from models.task import Task

app = FastAPI()


@app.get("/")
async def get_version():
    return {"version": "0.1.0"}


@app.post("/task")
async def create_task(task: Task):
    print(task)
    return task


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
