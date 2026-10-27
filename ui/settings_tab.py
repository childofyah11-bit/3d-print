from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class FilamentTab(tk.Frame):
    """Material database, brand recommendations, and temperature guidance."""

    def __init__(self, parent):
        super().__init__(parent, bg="#111827")

        self.materials = [
            ("Bambu PLA", "PLA", "210-225°C", "50-65°C", "Easy beginner option"),
            ("Bambu PETG", "PETG", "230-250°C", "70-80°C", "Strong and slightly harder to tune"),
            ("Bambu TPU", "TPU", "220-240°C", "35-60°C", "Flexible and slow printing"),
            ("Sunlu PLA", "PLA", "205-220°C", "50-60°C", "Great value and easy to use"),
            ("Elegoo PLA", "PLA", "200-220°C", "50-60°C", "Consistent results for many hobbyists"),
            ("eSUN PLA+", "PLA+", "210-235°C", "55-65°C", "Stronger than standard PLA"),
            ("Overture PLA", "PLA", "205-220°C", "50-60°C", "Reliable everyday material"),
            ("Generic PLA", "PLA", "200-220°C", "50-60°C", "General purpose starter"),
            ("Generic PETG", "PETG", "230-245°C", "70-80°C", "Good impact strength"),
            ("Generic TPU", "TPU", "220-240°C", "35-60°C", "Flexible and shock absorbing"),
        ]

        self.brand_notes = [
            ("Bambu Lab", "Reliable, premium print profiles and excellent color quality"),
            ("Sunlu", "Affordable, consistent, and beginner-friendly"),
            ("Elegoo", "Easy setup and strong PLA performance"),
            ("eSUN", "Popular PLA+ option that improves toughness"),
            ("Overture", "Widely available with strong community support"),
            ("Generic", "Works well when profile settings are tuned correctly"),
        ]

        self.build_material_table()
        self.build_brand_table()

    def build_material_table(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=12, pady=(12, 8))
        ttk.Label(frame, text="Material Database", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 6))

        tree = ttk.Treeview(frame, columns=("Name", "Type", "Nozzle", "Bed", "Notes"), show="headings")
        tree.heading("Name", text="Name")
        tree.heading("Type", text="Type")
        tree.heading("Nozzle", text="Nozzle")
        tree.heading("Bed", text="Bed")
        tree.heading("Notes", text="Notes")
        tree.column("Name", width=180)
        tree.column("Type", width=100)
        tree.column("Nozzle", width=120)
        tree.column("Bed", width=120)
        tree.column("Notes", width=300)

        for item in self.materials:
            tree.insert("", tk.END, values=item)

        tree.pack(fill="both", expand=True)

    def build_brand_table(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        ttk.Label(frame, text="Brand Database", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 6))

        tree = ttk.Treeview(frame, columns=("Brand", "Recommendation"), show="headings")
        tree.heading("Brand", text="Brand")
        tree.heading("Recommendation", text="Recommendation")
        tree.column("Brand", width=180)
        tree.column("Recommendation", width=500)

        for item in self.brand_notes:
            tree.insert("", tk.END, values=item)

        tree.pack(fill="both", expand=True)
