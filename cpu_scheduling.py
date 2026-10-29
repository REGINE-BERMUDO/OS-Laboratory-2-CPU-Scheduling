# Operating Systems Laboratory Activity 2
# CPU Scheduling Simulator - Python 3

from collections import deque
from copy import deepcopy

PROCESSES = [
    {"pid": "P1", "at": 0, "bt": 8, "priority": 2},
    {"pid": "P2", "at": 0, "bt": 4, "priority": 1},
    {"pid": "P3", "at": 0, "bt": 2, "priority": 4},
    {"pid": "P4", "at": 0, "bt": 6, "priority": 3},
]

SRTF_PROCESSES = [
    {"pid": "P1", "at": 0, "bt": 8, "priority": 2},
    {"pid": "P2", "at": 1, "bt": 4, "priority": 1},
    {"pid": "P3", "at": 2, "bt": 2, "priority": 4},
    {"pid": "P4", "at": 3, "bt": 1, "priority": 3},
]