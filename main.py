processes = [
    {"id": "P1", "arrival": 0, "burst": 8},
    {"id": "P2", "arrival": 0, "burst": 4},
    {"id": "P3", "arrival": 0, "burst": 2}
]


def fcfs(processes):
    processes = [p.copy() for p in processes]   # ADD THIS LINE

    time = 0
    result = []
    gantt = []

    for p in processes:
        if time < p["arrival"]:
            time = p["arrival"]

        start = time
        completion = start + p["burst"]

        turnaround = completion - p["arrival"]
        waiting = turnaround - p["burst"]

        result.append({
            "id": p["id"],
            "waiting": waiting,
            "turnaround": turnaround
        })

        gantt.append((p["id"], start, completion))
        time = completion

    return result, gantt

print("\n---FCFS---")


res, gantt = fcfs(processes)

print("\nProcess\tWT\tTAT")
for r in res:
    print(f"{r['id']}\t{r['waiting']}\t{r['turnaround']}")

print("\nGantt Chart:")
for g in gantt:
    print(f"| {g[0]} ", end="")
print("|")

print("0", end="")
for g in gantt:
    print(f"   {g[2]}", end="")


def sjf(processes):
    processes = [p.copy() for p in processes]  # avoid modifying original

    time = 0
    completed = []
    result = []
    gantt = []

    while processes:
        # get processes that have arrived
        available = [p for p in processes if p["arrival"] <= time]

        if not available:
            time += 1
            continue

        # pick shortest job
        shortest = min(available, key=lambda x: x["burst"])
        processes.remove(shortest)

        start = time
        completion = start + shortest["burst"]

        turnaround = completion - shortest["arrival"]
        waiting = turnaround - shortest["burst"]

        result.append({
            "id": shortest["id"],
            "waiting": waiting,
            "turnaround": turnaround
        })

        gantt.append((shortest["id"], start, completion))
        time = completion

    return result, gantt

print("\n--- SJF ---")

res, gantt = sjf(processes)

print("Process\tWT\tTAT")
for r in res:
    print(f"{r['id']}\t{r['waiting']}\t{r['turnaround']}")

print("\nGantt Chart:")
for g in gantt:
    print(f"| {g[0]} ", end="")
print("|")

print("0", end="")
for g in gantt:
    print(f"   {g[2]}", end="")


def round_robin(processes, quantum):
    processes = [p.copy() for p in processes]

    time = 0
    queue = []
    result = []
    gantt = []

    remaining = {p["id"]: p["burst"] for p in processes}
    arrival = {p["id"]: p["arrival"] for p in processes}

    processes.sort(key=lambda x: x["arrival"])
    i = 0

    while queue or i < len(processes):
        while i < len(processes) and processes[i]["arrival"] <= time:
            queue.append(processes[i]["id"])
            i += 1

        if not queue:
            time += 1
            continue

        current = queue.pop(0)
        exec_time = min(quantum, remaining[current])

        start = time
        time += exec_time
        remaining[current] -= exec_time

        gantt.append((current, start, time))

        while i < len(processes) and processes[i]["arrival"] <= time:
            queue.append(processes[i]["id"])
            i += 1

        if remaining[current] > 0:
            queue.append(current)
        else:
            completion = time
            tat = completion - arrival[current]
            wt = tat - next(p["burst"] for p in processes if p["id"] == current)

            result.append({
                "id": current,
                "waiting": wt,
                "turnaround": tat
            })

    return result, gantt

print("\n--- Round Robin ---")

quantum = 2

res, gantt = round_robin(processes, quantum)

print("Process\tWT\tTAT")
for r in res:
    print(f"{r['id']}\t{r['waiting']}\t{r['turnaround']}")

print("\nGantt Chart:")
for g in gantt:
    print(f"| {g[0]} ", end="")
print("|")

print("0", end="")
for g in gantt:
    print(f"   {g[2]}", end="")