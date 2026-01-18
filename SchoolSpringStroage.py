import json
import os

def load_seen_jobs(path):
    if not os.path.exists(path):
        return set()
    with open(path, "r") as f:
        return set(json.load(f))

def save_seen_jobs(path, seen_jobs):
    with open(path, "w") as f:
        json.dump(list(seen_jobs), f, indent=2)
