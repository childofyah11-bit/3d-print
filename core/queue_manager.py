from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class QueueJob:
    file_path: str
    eject_action: str = "Manual eject: configure before unloading"
    estimated_minutes: int = 25

    @property
    def file_name(self) -> str:
        return os.path.basename(self.file_path)


class QueueManager:
    """Manages the print queue and automatic combined print flow plan."""

    def __init__(self):
        self.jobs: List[QueueJob] = []

    def add_job(self, file_path: str, eject_action: str | None = None) -> QueueJob:
        if not file_path:
            raise ValueError("A file path is required.")
        job = QueueJob(file_path=file_path, eject_action=eject_action or "Manual eject: configure before unloading")
        self.jobs.append(job)
        return job

    def remove_job(self, index: int) -> QueueJob | None:
        if 0 <= index < len(self.jobs):
            return self.jobs.pop(index)
        return None

    def move_job(self, index: int, direction: int) -> bool:
        new_index = index + direction
        if not (0 <= index < len(self.jobs) and 0 <= new_index < len(self.jobs)):
            return False
        self.jobs[index], self.jobs[new_index] = self.jobs[new_index], self.jobs[index]
        return True

    def adjust_eject_action(self, index: int, action: str) -> None:
        if 0 <= index < len(self.jobs):
            self.jobs[index].eject_action = action

    def total_jobs(self) -> int:
        return len(self.jobs)

    def total_estimated_time(self) -> int:
        return sum(job.estimated_minutes for job in self.jobs)

    def formatted_total_time(self) -> str:
        total = self.total_estimated_time()
        hours, minutes = divmod(total, 60)
        if hours and minutes:
            return f"{hours}h {minutes}m"
        if hours:
            return f"{hours}h"
        return f"{minutes}m"

    def generate_queue_plan(self) -> List[str]:
        if not self.jobs:
            return ["No jobs in the queue."]

        plan: List[str] = []
        for index, job in enumerate(self.jobs, start=1):
            plan.append(f"JOB {index}: PRINT -> {job.file_name}")
            plan.append("WAIT -> stabilize nozzle and bed temperature")
            plan.append(f"EJECT ROUTINE -> {job.eject_action}")
            if index < len(self.jobs):
                plan.append("NEXT JOB")
        return plan

    def clear(self) -> None:
        self.jobs.clear()
