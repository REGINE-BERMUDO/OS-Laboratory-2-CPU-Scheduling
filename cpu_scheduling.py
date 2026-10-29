# Operating Systems Laboratory Activity 2
# CPU Scheduling Simulator - Python 3

from collections import deque
from copy import deepcopy

PROCESSES = [
    {"pid": "P1", "at": 0, "bt": 5, "priority": 3},
    {"pid": "P2", "at": 0, "bt": 9, "priority": 1},
    {"pid": "P3", "at": 0, "bt": 3, "priority": 4},
    {"pid": "P4", "at": 0, "bt": 7, "priority": 2},
]

SRTF_PROCESSES = [
    {"pid": "P1", "at": 0, "bt": 8, "priority": 2},
    {"pid": "P2", "at": 1, "bt": 4, "priority": 1},
    {"pid": "P3", "at": 2, "bt": 2, "priority": 4},
    {"pid": "P4", "at": 3, "bt": 1, "priority": 3},
]

def prepare(processes):
    result = deepcopy(processes)
    for p in result:
        p["remaining"] = p["bt"]
        p["first_start"] = None
    return result

def record_run(p, start, end, gantt):
    if start == end:
        return
    if gantt and gantt[-1][2] == p["pid"] and gantt[-1][1] == start:
        gantt[-1] = (gantt[-1][0], end, p["pid"])
    else:
        gantt.append((start, end, p["pid"]))
    if p["first_start"] is None:
        p["first_start"] = start
    p["remaining"] -= end - start
    if p["remaining"] == 0:
        p["ct"] = end

def finish_results(processes):
    for p in processes:
        p["tat"] = p["ct"] - p["at"]
        p["wt"] = p["tat"] - p["bt"]
        p["rt"] = p["first_start"] - p["at"]

def fcfs(data):
    ps = prepare(data)
    time, gantt = 0, []
    for p in sorted(ps, key=lambda x: (x["at"], x["pid"])):
        if time < p["at"]:
            time = p["at"]
        start = time
        time += p["bt"]
        record_run(p, start, time, gantt)
    finish_results(ps)
    return ps, gantt

def non_preemptive(data, mode):
    ps = prepare(data)
    time, done, gantt = 0, set(), []
    while len(done) < len(ps):
        ready = [p for p in ps if p["pid"] not in done and p["at"] <= time]
        if not ready:
            time = min(p["at"] for p in ps if p["pid"] not in done)
            continue
        if mode == "sjf":
            chosen = min(ready, key=lambda p: (p["bt"], p["at"], p["pid"]))
        else:
            chosen = min(ready, key=lambda p: (p["priority"], p["at"], p["pid"]))
        start = time
        time += chosen["bt"]
        record_run(chosen, start, time, gantt)
        done.add(chosen["pid"])
    finish_results(ps)
    return ps, gantt

def round_robin(data, quantum=2):
    if quantum <= 0:
        raise ValueError("Time quantum must be greater than zero.")
    ps = prepare(data)
    by_arrival = sorted(ps, key=lambda p: (p["at"], p["pid"]))
    ready, gantt = deque(), []
    time, i = 0, 0
    while i < len(by_arrival) or ready:
        if not ready:
            time = max(time, by_arrival[i]["at"])
        while i < len(by_arrival) and by_arrival[i]["at"] <= time:
            ready.append(by_arrival[i])
            i += 1
        p = ready.popleft()
        start = time
        end = time + min(quantum, p["remaining"])
        record_run(p, start, end, gantt)
        time = end
        while i < len(by_arrival) and by_arrival[i]["at"] <= time:
            ready.append(by_arrival[i])
            i += 1
        if p["remaining"] > 0:
            ready.append(p)
    finish_results(ps)
    return ps, gantt

def srtf(data):
    ps = prepare(data)
    time = min(p["at"] for p in ps)
    completed, gantt = set(), []
    while len(completed) < len(ps):
        ready = [
            p for p in ps
            if p["at"] <= time and p["pid"] not in completed and p["remaining"] > 0
        ]
        if not ready:
            time = min(p["at"] for p in ps if p["pid"] not in completed and p["at"] > time)
            continue
        p = min(ready, key=lambda x: (x["remaining"], x["at"], x["pid"]))
        start, end = time, time + 1
        record_run(p, start, end, gantt)
        time = end
        if p["remaining"] == 0:
            completed.add(p["pid"])
    finish_results(ps)
    return ps, gantt

def display(title, processes, gantt):
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)
    print("\nGANTT CHART")
    print(" | ".join(f"{pid} [{start}-{end}]" for start, end, pid in gantt))
    print("\nPROCESS METRICS")
    print(f"{'PID':<6}{'AT':>5}{'BT':>5}{'PR':>5}{'CT':>6}{'TAT':>6}{'WT':>6}{'RT':>6}")
    for p in sorted(processes, key=lambda x: x["pid"]):
        print(f"{p['pid']:<6}{p['at']:>5}{p['bt']:>5}{p['priority']:>5}{p['ct']:>6}{p['tat']:>6}{p['wt']:>6}{p['rt']:>6}")
    n = len(processes)
    print(f"\nAverage Waiting Time: {sum(p['wt'] for p in processes) / n:.2f} ms")
    print(f"Average Turnaround Time: {sum(p['tat'] for p in processes) / n:.2f} ms")
    print(f"Average Response Time: {sum(p['rt'] for p in processes) / n:.2f} ms")

if __name__ == "__main__":
    ps, g = fcfs(PROCESSES)
    display("1. FCFS", ps, g)
    ps, g = non_preemptive(PROCESSES, "sjf")
    display("2. NON-PREEMPTIVE SJF", ps, g)
    ps, g = non_preemptive(PROCESSES, "priority")
    display("3. NON-PREEMPTIVE PRIORITY", ps, g)
    ps, g = round_robin(PROCESSES, quantum=2)
    display("4. ROUND ROBIN (QUANTUM = 2)", ps, g)
    ps, g = srtf(SRTF_PROCESSES)
    display("5. SRTF (SEPARATE ARRIVAL-TIME DATASET)", ps, g)