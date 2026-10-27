from __future__ import annotations

import os
import tkinter as tk
from tkinter import filedialog, ttk

from core.analysis import AnalysisEngine
from core.queue_manager import QueueManager


class QueueTab(tk.Frame):
    """Queue management for GCODE and print job sequencing."""

    def __init__(self, parent, queue_manager: QueueManager | None = None):
        super().__init__(parent, bg="#111827")
        self.queue_manager = queue_manager or QueueManager()

        self.left = ttk.Frame(self)
        self.left.pack(side="left", fill="y", padx=12, pady=12)

        self.actions = ttk.Frame(self.left)
        self.actions.pack(fill="x", pady=(0, 10))

        ttk.Button(self.actions, text="Add GCODE", command=self.add_files).pack(side="left", padx=(0, 6))
        ttk.Button(self.actions, text="Remove", command=self.remove_selected).pack(side="left", padx=(0, 6))
        ttk.Button(self.actions, text="Move Up", command=lambda: self.move_selected(-1)).pack(side="left", padx=(0, 6))
        ttk.Button(self.actions, text="Move Down", command=lambda: self.move_selected(1)).pack(side="left")

        self.queue_listbox = tk.Listbox(
            self.left,
            width=54,
            height=18,
            bg="#0f172a",
            fg="#e2e8f0",
            selectbackground="#2563eb",
            selectforeground="#f8fafc",
            borderwidth=0,
            highlightthickness=0,
        )
        self.queue_listbox.pack(fill="both", expand=True)

        stats = ttk.Frame(self.left)
        stats.pack(fill="x", pady=(10, 0))
        ttk.Label(stats, text="Total Jobs:").pack(side="left")
        self.total_jobs_var = tk.StringVar(value="0")
        ttk.Label(stats, textvariable=self.total_jobs_var, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(8, 20))
        ttk.Label(stats, text="Total Time:").pack(side="left")
        self.total_time_var = tk.StringVar(value="0m")
        ttk.Label(stats, textvariable=self.total_time_var, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(8, 0))

        self.right = ttk.Frame(self)
        self.right.pack(side="left", fill="both", expand=True, padx=(0, 12), pady=12)

        ttk.Label(self.right, text="Queue Plan", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))
        self.plan_text = tk.Text(
            self.right,
            height=18,
            width=45,
            bg="#0f172a",
            fg="#e2e8f0",
            borderwidth=0,
            highlightthickness=0,
            wrap="word",
        )
        self.plan_text.pack(fill="both", expand=True)

        ttk.Button(self.right, text="Generate Queue", command=self.generate_queue_plan).pack(pady=(12, 0), anchor="e")
        self.refresh_queue()

    def add_files(self):
        accepted = ("STL files", "*.stl"), ("3MF files", "*.3mf"), ("GCODE files", "*.gcode")
        files = filedialog.askopenfilenames(filetypes=accepted)
        if not files:
            return
        for file_path in files:
            self.queue_manager.add_job(file_path)
        self.refresh_queue()

    def remove_selected(self):
        selection = self.queue_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        self.queue_manager.remove_job(index)
        self.refresh_queue()

    def move_selected(self, direction: int):
        selection = self.queue_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        self.queue_manager.move_job(index, direction)
        self.refresh_queue()

    def refresh_queue(self):
        self.queue_listbox.delete(0, tk.END)
        for job in self.queue_manager.jobs:
            self.queue_listbox.insert(tk.END, job.file_name)
        self.total_jobs_var.set(str(self.queue_manager.total_jobs()))
        self.total_time_var.set(self.queue_manager.formatted_total_time())

    def generate_queue_plan(self):
        plan = self.queue_manager.generate_queue_plan()
        self.plan_text.delete("1.0", tk.END)
        self.plan_text.insert(tk.END, "\n".join(plan))


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Queue Demo")
    QueueTab(window)
    window.mainloop()
