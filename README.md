# OS Laboratory 2: CPU Scheduling Algorithms

## Overview

This project is a **CPU Scheduling Simulator** written in Python 3 and developed in GitHub Codespaces. It implements five scheduling algorithms, draws a Gantt chart for each one, and computes the completion time, turnaround time, waiting time, and response time of every process.

## Algorithms Implemented

| # | Algorithm | Type |
|---|---|---|
| 1 | First-Come, First-Served (FCFS) | Non-preemptive |
| 2 | Shortest Job First (SJF) | Non-preemptive |
| 3 | Priority Scheduling | Non-preemptive |
| 4 | Round Robin (RR), quantum = 2 ms | Preemptive |
| 5 | Shortest Remaining Time First (SRTF) | Preemptive |

## Datasets

**Main dataset** (used for FCFS, SJF, Priority, and Round Robin)

| Process | Arrival Time (AT) | Burst Time (BT) | Priority |
|---|---|---|---|
| P1 | 0 | 8 | 2 |
| P2 | 0 | 4 | 1 |
| P3 | 0 | 2 | 4 |
| P4 | 0 | 6 | 3 |

**Separate SRTF dataset** (different arrival times to show preemption)

| Process | Arrival Time (AT) | Burst Time (BT) | Priority |
|---|---|---|---|
| P1 | 0 | 8 | 2 |
| P2 | 1 | 4 | 1 |
| P3 | 2 | 2 | 4 |
| P4 | 3 | 1 | 3 |

**Assumptions**
- A smaller priority number means a higher priority.
- Round Robin uses a time quantum of 2 ms.
- SJF and Priority Scheduling are non-preemptive.
- FCFS uses arrival order, and the process ID breaks ties.

## Formulas

| Metric | Formula |
|---|---|
| Turnaround Time (TAT) | TAT = CT − AT |
| Waiting Time (WT) | WT = TAT − BT |
| Response Time (RT) | RT = First CPU Start − AT |
| Average metric | Sum of metric values ÷ number of processes |

## How the Code Works

| Function | What it does |
|---|---|
| `prepare()` | Copies the process list and adds `remaining` and `first_start` |
| `record_run()` | Adds a run to the Gantt chart and updates the process |
| `finish_results()` | Computes TAT, WT, and RT for each process |
| `fcfs()` | First-Come, First-Served scheduling |
| `non_preemptive()` | SJF and Priority scheduling (chosen by `mode`) |
| `round_robin()` | Round Robin scheduling with a given quantum |
| `srtf()` | Preemptive SJF, checked every 1 ms |
| `display()` | Prints the Gantt chart, metrics table, and averages |

## Results

### Average Metrics

| Algorithm | Average WT | Average TAT | Average RT |
|---|---|---|---|
| FCFS | 8.50 ms | 13.50 ms | 8.50 ms |
| Non-preemptive SJF | 5.00 ms | 10.00 ms | 5.00 ms |
| Non-preemptive Priority | 8.50 ms | 13.50 ms | 8.50 ms |
| Round Robin (q = 2) | 9.00 ms | 14.00 ms | 3.00 ms |
| SRTF (separate dataset) | 2.75 ms | 6.50 ms | 0.25 ms |


## Manual Verification

At least two processes per algorithm were calculated by hand and compared with the program output. All results matched.

| Algorithm | Process | CT / TAT / WT / RT | Match |
|---|---|---|---|
| FCFS | P2 | 12 / 12 / 8 / 8 | ✅ |
| FCFS | P3 | 14 / 14 / 12 / 12 | ✅ |
| SJF | P2 | 6 / 6 / 2 / 2 | ✅ |
| SJF | P1 | 20 / 20 / 12 / 12 | ✅ |
| Priority | P1 | 12 / 12 / 4 / 4 | ✅ |
| Priority | P3 | 20 / 20 / 18 / 18 | ✅ |
| Round Robin | P1 | 20 / 20 / 12 / 0 | ✅ |
| Round Robin | P3 | 6 / 6 / 4 / 4 | ✅ |
| SRTF | P1 | 15 / 15 / 7 / 0 | ✅ |
| SRTF | P4 | 5 / 2 / 1 / 1 | ✅ |

## Experiment: Round Robin Time Quantum

To test another quantum, change this line in the `main` block:

```python
ps, g = round_robin(PROCESSES, quantum=2)
```

| Quantum | CPU Allocations | Avg WT | Avg TAT | Avg RT |
|---|---|---|---|---|
| 1 | 19 | 9.50 ms | 14.50 ms | 1.50 ms |
| 2 | 10 | 9.00 ms | 14.00 ms | 3.00 ms |
| 4 | 6 | 9.00 ms | 14.00 ms | 5.50 ms |

**Findings**
- A smaller quantum gives more CPU allocations and a faster response time.
- A larger quantum gives fewer allocations and a slower response time.
- A very large quantum makes Round Robin behave like FCFS.
- A very small quantum causes many context switches, which wastes CPU time in a real operating system.
- q = 2 and q = 4 tied for the lowest average waiting time (9.00 ms).

## Experiment: Modified Dataset

The burst times and priorities were changed to test how the data affects the results (all arrival times stay at 0):

| Process | AT | BT | Priority |
|---|---|---|---|
| P1 | 0 | 5 | 3 |
| P2 | 0 | 9 | 1 |
| P3 | 0 | 3 | 4 |
| P4 | 0 | 7 | 2 |

| Algorithm | Average WT | Average TAT | Average RT |
|---|---|---|---|
| FCFS | 9.00 ms | 15.00 ms | 9.00 ms |
| SJF | 6.50 ms | 12.50 ms | 6.50 ms |
| Priority | 11.50 ms | 17.50 ms | 11.50 ms |
| Round Robin (q = 2) | 13.00 ms | 19.00 ms | 3.00 ms |
| SRTF* | 2.75 ms | 6.50 ms | 0.25 ms |

\*SRTF uses its own separate dataset, so it is not changed.

After this experiment, the code was changed back to the original dataset.

## Key Findings

- **SJF** had the lowest average waiting time among the first four algorithms (5.00 ms), but it can starve long jobs.
- **Round Robin** had the best response time (3.00 ms) but a higher waiting time (9.00 ms).
- **SRTF** performed best on its own dataset (2.75 ms) because it preempts longer processes.
- **Priority** became worse than FCFS with the modified dataset, because the highest-priority process also had the longest burst time.
- The results depend on the data as well as the algorithm.

## Conclusion

In this laboratory, I built a CPU scheduling simulator in Python and tested FCFS, SJF, Priority, Round Robin, and SRTF. My manual calculations matched the program output, which confirmed that the simulator works correctly. No single algorithm is best for every situation. The right choice depends on what the system needs most.

