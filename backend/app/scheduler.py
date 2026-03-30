def pick_best_worker(task: dict, workers: dict):
    candidates = []

    for worker in workers.values():
        if worker["status"] != "ONLINE":
            continue

        available_cpu = worker["total_cpu"] - worker["used_cpu"]
        available_mem = worker["total_mem"] - worker["used_mem"]

        if available_cpu >= task["cpu_required"] and available_mem >= task["mem_required"]:
            remain_cpu = available_cpu - task["cpu_required"]
            remain_mem = available_mem - task["mem_required"]
            score = remain_cpu * 1000 + remain_mem
            candidates.append((score, worker))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]


def assign_task_to_worker(task: dict, worker: dict):
    worker["used_cpu"] += task["cpu_required"]
    worker["used_mem"] += task["mem_required"]
    worker["running_tasks"].append(task["task_id"])

    task["assigned_worker_id"] = worker["worker_id"]
    task["status"] = "RUNNING"