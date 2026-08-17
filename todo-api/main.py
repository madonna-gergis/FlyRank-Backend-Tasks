import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Task Manager API with SQLite")

DB_FILE = "tasks.db"

# --- Database Helper Function ---
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enables dict-like access for rows
    return conn

# --- Stage 0: Create Database, Table & Seed Data ---
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()

    # Seed 3 example tasks ONLY if table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Learn FastAPI", 1))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Connect SQLite Database", 0))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("Build AI Portfolio", 0))
        conn.commit()
    conn.close()

# Initialize DB on server start
init_db()

# --- Pydantic Models for API Validation ---
class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

# --- Stage 1: Read Endpoints ---
@app.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [dict(task) for task in tasks]

@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if task is None:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    return dict(task)

# --- Stage 2: Insert Endpoint ---
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(status_code=400, detail={"error": "Title is required"})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task_data.title.strip(), 0))
    conn.commit()
    new_id = cursor.lastrowid
    
    new_task = conn.execute("SELECT * FROM tasks WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return dict(new_task)

# --- Stage 3: Update & Delete Endpoints ---
@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_data: TaskUpdate):
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task is None:
        conn.close()
        raise HTTPException(status_code=404, detail={"error": "Task not found"})

    current_title = task["title"]
    current_done = task["done"]

    new_title = task_data.title.strip() if task_data.title is not None else current_title
    new_done = task_data.done if task_data.done is not None else current_current_done if 'current_current_done' in locals() else current_done

    if task_data.title is not None and not task_data.title.strip():
        conn.close()
        raise HTTPException(status_code=400, detail={"error": "Title cannot be empty"})

    conn.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (new_title, int(new_done), task_id))
    conn.commit()
    
    updated_task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return dict(updated_task)

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task is None:
        conn.close()
        raise HTTPException(status_code=404, detail={"error": "Task not found"})

    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return None