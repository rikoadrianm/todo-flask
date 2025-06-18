# app.py (Flask Version dari todo_app.py)

from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
todo_list = []

def load_tasks():
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    task_name, is_done, deadline = parts
                else:
                    task_name, is_done = parts
                    deadline = "-"
                todo_list.append({
                    "task": task_name,
                    "done": is_done == "True",
                    "deadline": deadline
                })

def save_tasks():
    with open("tasks.txt", "w") as f:
        for task in todo_list:
            f.write(f"{task['task']}|{task['done']}|{task['deadline']}\n")

@app.route("/")
def index():
    filter_status = request.args.get('filter')
    if filter_status == 'done':
        tasks = [t for t in todo_list if t["done"]]
    elif filter_status == 'undone':
        tasks = [t for t in todo_list if not t["done"]]
    else:
        tasks = todo_list
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("task")
    deadline = request.form.get("deadline") or "-"
    todo_list.append({"task": name, "done": False, "deadline": deadline})
    save_tasks()
    return redirect(url_for("index"))

@app.route("/done/<int:index>")
def done(index):
    if 0 <= index < len(todo_list):
        todo_list[index]["done"] = True
        save_tasks()
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(todo_list):
        todo_list.pop(index)
        save_tasks()
    return redirect(url_for("index"))

@app.route("/edit/<int:index>", methods=["POST"])
def edit(index):
    if 0 <= index < len(todo_list):
        new_name = request.form.get("task")
        new_deadline = request.form.get("deadline")
        if new_name:
            todo_list[index]["task"] = new_name
        if new_deadline:
            todo_list[index]["deadline"] = new_deadline
        save_tasks()
    return redirect(url_for("index"))

if __name__ == "__main__":
    load_tasks()
    app.run(debug=True)
