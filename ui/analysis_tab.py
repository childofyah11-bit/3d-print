from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from core.analysis import AnalysisEngine


class AnalysisTab(tk.Frame):
    """Shows print quality, strength, speed, difficulty, cost, and timing estimates."""

    def __init__(self, parent):
        super().__init__(parent, bg="#111827")
        self.engine = AnalysisEngine()

        self.metrics_frame = ttk.Frame(self)
        self.metrics_frame.pack(fill="both", expand=True, padx=12, pady=12)

        self.label_map = {}
        self.bar_map = {}
        self.generate_metric_row("Estimated Print Quality", 0)
        self.generate_metric_row("Estimated Strength", 1)
        self.generate_metric_row("Estimated Speed", 2)
        self.generate_metric_row("Difficulty Rating", 3)

        self.summary_text = tk.Text(
            self,
            height=12,
            bg="#0f172a",
            fg="#e2e8f0",
            borderwidth=0,
            highlightthickness=0,
            wrap="word",
        )
        self.summary_text.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def generate_metric_row(self, title: str, row_index: int):
        ttk.Label(self.metrics_frame, text=title, width=20).grid(row=row_index, column=0, padx=(0, 12), pady=6, sticky="w")
        progress = ttk.Progressbar(self.metrics_frame, orient="horizontal", length=400, mode="determinate", maximum=100)
        progress.grid(row=row_index, column=1, padx=(0, 10), pady=6, sticky="ew")
        value_label = ttk.Label(self.metrics_frame, text="0%", width=6)
        value_label.grid(row=row_index, column=2, padx=(0, 10), sticky="w")
        self.label_map[title] = value_label
        self.bar_map[title] = progress

    def update_analysis(self, settings: dict):
        quality = self.engine.estimate_quality(settings)
        strength = self.engine.estimate_strength(settings)
        speed = self.engine.estimate_speed(settings)
        difficulty = self.engine.estimate_difficulty(settings)

        self._set_metric("Estimated Print Quality", quality)
        self._set_metric("Estimated Strength", strength)
        self._set_metric("Estimated Speed", speed)
        self._set_metric("Difficulty Rating", difficulty * 10)

        suggestions = self.engine.generate_suggestions(settings)
        self.summary_text.delete("1.0", tk.END)
        summary = [
            f"Estimated Print Quality: {quality}/100",
            f"Estimated Strength: {strength}/100",
            f"Estimated Speed: {speed}/100",
            f"Difficulty Rating: {difficulty}/10",
            "",
            "Suggested Improvements:",
        ]
        summary.extend(f"- {item}" for item in suggestions)
        self.summary_text.insert(tk.END, "\n".join(summary))

    def _set_metric(self, name: str, value: int):
        self.bar_map[name]["value"] = value
        self.label_map[name].configure(text=f"{value}%")
