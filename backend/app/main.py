from uuid import uuid4
from fastapi import FastAPI, HTTPException
from time import time
from app.schemas import WorkerRegisterRequest, TaskCreateRequest, WorkerHeartbeatRequest
from app.state import workers, tasks, task_logs
from app.scheduler import pick_best_worker, assign_task_to_worker
import asyncio
import subprocess
from asyncio.subprocess import PIPE
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mini Scheduler")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Mini Scheduler backend is running"}


@app.get("/api/dashboard")
def get_dashboard():
    return {
        "workers": list(workers.values()),
        "tasks": list(tasks.values()),
        "summary": {
            "total_workers": len(workers),
            "online_workers": sum(1 for w in workers.values() if w["status"] == "ONLINE"),
            "offline_workers": sum(1 for w in workers.values() if w["status"] == "OFFLINE"),
            "pending_tasks": sum(1 for t in tasks.values() if t["status"] == "PENDING"),
            "running_tasks": sum(1 for t in tasks.values() if t["status"] == "RUNNING"),
            "success_tasks": sum(1 for t in tasks.values() if t["status"] == "SUCCESS"),
            "failed_tasks": sum(1 for t in tasks.values() if t["status"] == "FAILED"),
        },
    }


@app.post("/api/workers/register")
def register_worker(payload: WorkerRegisterRequest):
    if payload.worker_id in workers:
        raise HTTPException(status_code=400, detail="Worker already exists")

    worker = {
        "worker_id": payload.worker_id,
        "host": payload.host,
        "total_cpu": payload.total_cpu,
        "total_mem": payload.total_mem,
        "used_cpu": 0,
        "used_mem": 0,
        "status": "ONLINE",
        "running_tasks": [],
        "last_heartbeat": time(),
    }

    workers[payload.worker_id] = worker
    return {"message": "Worker registered successfully", "worker": worker}


@app.get("/api/workers")
def list_workers():
    return {"workers": list(workers.values())}


@app.post("/api/tasks")
async def create_task(payload: TaskCreateRequest):
    task_id = str(uuid4())

    task = {
    "task_id": task_id,
    "command": payload.command,
    "cpu_required": payload.cpu_required,
    "mem_required": payload.mem_required,
    "status": "PENDING",
    "assigned_worker_id": None,
    "started_at": None,
    "finished_at": None,
    "exit_code": None,
    }

    task_logs[task_id] = []

    # Try to schedule immediately
    worker = pick_best_worker(task, workers)
    if worker is not None:
        assign_task_to_worker(task, worker)
        asyncio.create_task(execute_task(task, worker))

    tasks[task_id] = task
    return {
        "message": "Task created successfully",
        "task": task,
    }


@app.get("/api/tasks")
def list_tasks():
    return {"tasks": list(tasks.values())}


@app.get("/api/tasks/{task_id}")
def get_task(task_id: str):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": task}


@app.get("/api/tasks/{task_id}/logs")
def get_task_logs(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "task_id": task_id,
        "logs": task_logs.get(task_id, [])
    }


@app.post("/api/workers/heartbeat")
async def worker_heartbeat(payload: WorkerHeartbeatRequest):
    worker = workers.get(payload.worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker["used_cpu"] = payload.used_cpu
    worker["used_mem"] = payload.used_mem
    worker["running_tasks"] = payload.running_tasks
    worker["last_heartbeat"] = time()
    worker["status"] = "ONLINE"

    return {"message": "Heartbeat received", "worker": worker}


async def monitor_workers():
    while True:
        now = time()
        for worker in workers.values():
            last_heartbeat = worker.get("last_heartbeat")
            if last_heartbeat is None:
                continue

            if now - last_heartbeat > 15:
                worker["status"] = "OFFLINE"
            else:
                worker["status"] = "ONLINE"
        await asyncio.sleep(2)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_workers())
    asyncio.create_task(reschedule_pending_tasks())



async def reschedule_pending_tasks():
    while True:
        for task in tasks.values():
            if task["status"] != "PENDING":
                continue

            worker = pick_best_worker(task, workers)
            if worker is not None:
                assign_task_to_worker(task, worker)
                asyncio.create_task(execute_task(task, worker))

        await asyncio.sleep(2)



async def execute_task(task: dict, worker: dict):
    await asyncio.to_thread(run_task_blocking, task, worker)


def run_task_blocking(task: dict, worker: dict):
    task_id = task["task_id"]
    command = task["command"]

    task["started_at"] = time()
    task_logs[task_id].append(f"Starting task: {command}")

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    
        if process.stdout:
            for line in process.stdout:
                task_logs[task_id].append(f"[stdout] {line.rstrip()}")

        if process.stderr:
            for line in process.stderr:
                task_logs[task_id].append(f"[stderr] {line.rstrip()}")

        return_code = process.wait()
        task["exit_code"] = return_code
        task["finished_at"] = time()

        if return_code == 0:
            task["status"] = "SUCCESS"
            task_logs[task_id].append("Task finished successfully")
        else:
            task["status"] = "FAILED"
            task_logs[task_id].append(f"Task failed with exit code {return_code}")

    except Exception as e:
        task["status"] = "FAILED"
        task["finished_at"] = time()
        task["exit_code"] = -1
        task_logs[task_id].append(f"Execution error: {repr(e)}")

    finally:
        worker["used_cpu"] -= task["cpu_required"]
        worker["used_mem"] -= task["mem_required"]

        if task_id in worker["running_tasks"]:
            worker["running_tasks"].remove(task_id)