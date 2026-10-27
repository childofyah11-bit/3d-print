from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk

from core.profile_manager import ProfileManager
from ui.analysis_tab import AnalysisTab
from ui.filament_tab import FilamentTab
from ui.optimizer_tab import OptimizerTab
from ui.queue_tab import QueueTab
from ui.settings_tab import SettingsTab
from core.queue_manager import QueueManager


class PrintOptimizerPro(tk.Tk):
    """Main application shell for the PrintOptimizer Pro desktop workflow."""

    def __init__(self):
        super().__init__()
        self.title("PrintOptimizer Pro")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        self.configure(bg="#111827")

        self.profile_manager = ProfileManager()
        self.queue_manager = QueueManager()

        self._configure_style()
        self._build_header()
        self._build_notebook()

    def _configure_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TFrame", background="#111827")
        style.configure("TNotebook", background="#111827")
        style.configure("TNotebook.Tab", background="#1f2937", foreground="#e2e8f0", padding=(18, 8))
        style.map("TNotebook.Tab", background=[("selected", "#0f172a")], foreground=[("selected", "#f8fafc")])
        style.configure("TButton", background="#2563eb", foreground="#f8fafc", padding=(12, 8))
        style.map("TButton", background=[("active", "#1d4ed8")], foreground=[("active", "#f8fafc")])
        style.configure("TLabel", background="#111827", foreground="#e2e8f0")
        style.configure("TCombobox", fieldbackground="#0f172a", background="#0f172a", foreground="#e2e8f0")

    def _build_header(self):
        header = tk.Frame(self, bg="#111827", height=72)
        header.pack(fill="x")

        title = tk.Label(header, text="PrintOptimizer Pro", bg="#111827", fg="#f8fafc", font=("Segoe UI", 20, "bold"))
        title.pack(anchor="w", padx=18, pady=(18, 8))

        search = tk.Entry(header, width=40, bg="#0f172a", fg="#e2e8f0", insertbackground="#e2e8f0")
        search.insert(0, "Search prints, tips, or profiles")
        search.pack(anchor="e", padx=18, pady=(0, 14))

    def _build_notebook(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        optimizer_tab = OptimizerTab(notebook, self.profile_manager)
        queue_tab = QueueTab(notebook, self.queue_manager)
        filament_tab = FilamentTab(notebook)
        analysis_tab = AnalysisTab(notebook)
        settings_tab = SettingsTab(notebook, self.profile_manager)

        notebook.add(optimizer_tab, text="Optimizer")
        notebook.add(queue_tab, text="Queue")
        notebook.add(filament_tab, text="Filaments")
        notebook.add(analysis_tab, text="Analysis")
        notebook.add(settings_tab, text="Settings")

        self.optimizer_tab = optimizer_tab
        self.analysis_tab = analysis_tab

        # Hook the analysis tab to optimization results for a neat workflow.
        optimizer_tab.optimize_current()
        analysis_tab.update_analysis({
            "estimated_quality": 82,
            "estimated_strength": 78,
            "estimated_speed": 80,
            "difficulty_rating": 5,
            "layer_height": 0.2,
            "infill_percent": 18,
            "cooling_percent": 80,
        })


if __name__ == "__main__":
    app = PrintOptimizerPro()
    app.mainloop()
