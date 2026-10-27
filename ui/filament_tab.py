from __future__ import annotations

import json
import os
import tkinter as tk
from tkinter import filedialog, ttk

from core.optimizer import OptimizationEngine


class OptimizerTab(tk.Frame):
    """Main settings optimization wizard for beginners."""

    def __init__(self, parent, profile_manager):
        super().__init__(parent, bg="#111827")
        self.profile_manager = profile_manager
        self.engine = OptimizationEngine(profile_manager)

        self.printers = [printer.get("name") for printer in self.profile_manager.load_printers()]
        self.filaments = [filament.get("name") for filament in self.profile_manager.load_filaments()]
        self.print_types = [
            "Miniature",
            "Functional Part",
            "Cosplay Prop",
            "Toy",
            "Container",
            "Planter",
            "Vase",
            "Decorative Object",
            "Mechanical Part",
            "Art Piece",
        ]
        self.goals = [
            "Best Quality",
            "Strongest Part",
            "Fastest Print",
            "Balanced",
            "Lowest Cost",
            "Best Surface Finish",
        ]

        self._build_form()
        self._build_ai_mode()
        self._build_results_panel()

    def _build_form(self):
        form = ttk.Frame(self)
        form.pack(fill="x", padx=16, pady=16)

        self.printer_var = tk.StringVar(value=self.printers[0] if self.printers else "Custom")
        self.filament_var = tk.StringVar(value=self.filaments[0] if self.filaments else "Bambu PLA")
        self.print_type_var = tk.StringVar(value="Miniature")
        self.goal_var = tk.StringVar(value="Balanced")

        fields = [
            ("Printer", self.printer_var, self.printers),
            ("Filament", self.filament_var, self.filaments),
            ("Print Type", self.print_type_var, self.print_types),
            ("Priority", self.goal_var, self.goals),
        ]

        for index, (label_text, variable, options) in enumerate(fields):
            ttk.Label(form, text=label_text, width=14).grid(row=index, column=0, padx=(0, 12), pady=8, sticky="w")
            combo = ttk.Combobox(form, textvariable=variable, values=options, state="readonly", width=28)
            combo.grid(row=index, column=1, padx=(0, 18), pady=8, sticky="w")

        ttk.Button(form, text="OPTIMIZE", command=self.optimize_current).grid(row=4, column=0, columnspan=2, pady=(12, 0), sticky="w")

    def _build_ai_mode(self):
        ai_frame = ttk.Frame(self)
        ai_frame.pack(fill="x", padx=16, pady=(0, 12))
        ttk.Label(ai_frame, text="AI Mode", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        text_frame = ttk.Frame(ai_frame)
        text_frame.pack(fill="x", pady=(6, 8))

        self.ai_entry = tk.Text(text_frame, height=4, width=85, bg="#0f172a", fg="#e2e8f0", borderwidth=0, highlightthickness=0)
        self.ai_entry.pack(side="left", fill="x", expand=True)

        ttk.Button(text_frame, text="AI Recommend", command=self.apply_ai_recommendation).pack(side="left", padx=(10, 0))

    def _build_results_panel(self):
        panel = ttk.Frame(self)
        panel.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        ttk.Label(panel, text="Generated Settings", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))

        self.results_text = tk.Text(
            panel,
            height=18,
            width=105,
            bg="#0f172a",
            fg="#e2e8f0",
            borderwidth=0,
            highlightthickness=0,
            wrap="word",
        )
        self.results_text.pack(fill="both", expand=True)

    def optimize_current(self):
        settings = self.engine.optimize(
            self.printer_var.get(),
            self.filament_var.get(),
            self.print_type_var.get(),
            self.goal_var.get(),
        )
        self._render_settings(settings)
        return settings

    def apply_ai_recommendation(self):
        description = self.ai_entry.get("1.0", tk.END).strip()
        if not description:
            self.ai_entry.insert(tk.END, "I am printing a dragon miniature")
            description = self.ai_entry.get("1.0", tk.END).strip()
        settings = self.engine.ai_recommendation(description)
        self._render_settings(settings)
        self.printer_var.set(settings["printer"])
        self.filament_var.set(settings["filament"])
        self.print_type_var.set(settings["print_type"])
        self.goal_var.set(settings["goal"])

    def _render_settings(self, settings: dict):
        lines = [
            "PrintOptimizer Pro Recommendation",
            "=" * 36,
            f"Printer: {settings['printer']}",
            f"Filament: {settings['filament']}",
            f"Print Type: {settings['print_type']}",
            f"Priority: {settings['goal']}",
            "",
            "Generated Output",
            "-" * 36,
            f"Layer Height: {settings['layer_height']} mm",
            f"Nozzle Temperature: {settings['nozzle_temperature']}°C",
            f"Bed Temperature: {settings['bed_temperature']}°C",
            f"Wall Count: {settings['wall_count']}",
            f"Top Layers: {settings['top_layers']}",
            f"Bottom Layers: {settings['bottom_layers']}",
            f"Infill %: {settings['infill_percent']}%",
            f"Infill Pattern: {settings['infill_pattern']}",
            f"Print Speed: {settings['print_speed']} mm/s",
            f"Travel Speed: {settings['travel_speed']} mm/s",
            f"Cooling %: {settings['cooling_percent']}%",
            f"Support Recommendations: {settings['support_recommendation']}",
            f"Build Plate Adhesion: {settings['build_plate_adhesion']}",
            "",
            "Analysis",
            "-" * 36,
            f"Estimated Print Quality: {settings['estimated_quality']}/100",
            f"Estimated Strength: {settings['estimated_strength']}/100",
            f"Estimated Speed: {settings['estimated_speed']}/100",
            f"Difficulty Rating: {settings['difficulty_rating']}/10",
            "Suggested Improvements:",
        ]
        lines.extend(f"- {item}" for item in settings.get("suggested_improvements", []))
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, "\n".join(lines))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PrintOptimizer Pro")
    root.geometry("1100x760")
    OptimizerTab(root, None)
    root.mainloop()
