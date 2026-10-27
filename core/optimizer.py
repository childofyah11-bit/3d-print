from __future__ import annotations

import math
import os
from typing import Any, Dict, List

from core.profile_manager import ProfileManager


class OptimizationEngine:
    """Creates beginner-friendly print settings from printer, material, print type, and goal."""

    def __init__(self, profile_manager: ProfileManager | None = None):
        self.profile_manager = profile_manager or ProfileManager()
        self.printers = self.profile_manager.load_printers()
        self.filaments = self.profile_manager.load_filaments()

    def _get_printer(self, name: str) -> Dict[str, Any]:
        for printer in self.printers:
            if printer.get("name") == name:
                return printer
        return self.printers[0] if self.printers else {}

    def _get_filament(self, name: str) -> Dict[str, Any]:
        for filament in self.filaments:
            if filament.get("name") == name:
                return filament
        return self.filaments[0] if self.filaments else {}

    def _layer_height_for(self, print_type: str, goal: str) -> float:
        mapping = {
            "Miniature": 0.12,
            "Functional Part": 0.20,
            "Cosplay Prop": 0.16,
            "Toy": 0.18,
            "Container": 0.20,
            "Planter": 0.20,
            "Vase": 0.24,
            "Decorative Object": 0.16,
            "Mechanical Part": 0.20,
            "Art Piece": 0.12,
        }
        base = mapping.get(print_type, 0.20)
        if goal == "Fastest Print":
            return round(base + 0.04, 2)
        if goal in ["Best Quality", "Best Surface Finish"]:
            return round(base - 0.02, 2)
        return round(base, 2)

    def _wall_count_for(self, print_type: str, goal: str) -> int:
        if goal in ["Strongest Part", "Mechanical Part"]:
            return 4
        if goal in ["Best Quality", "Best Surface Finish"]:
            return 3
        if goal == "Fastest Print":
            return 2
        return 3

    def _infill_percent_for(self, print_type: str, goal: str) -> int:
        mapping = {
            "Miniature": {"Best Quality": 15, "Strongest Part": 20, "Fastest Print": 10, "Balanced": 15, "Lowest Cost": 10, "Best Surface Finish": 15},
            "Functional Part": {"Best Quality": 20, "Strongest Part": 35, "Fastest Print": 12, "Balanced": 22, "Lowest Cost": 15, "Best Surface Finish": 18},
            "Cosplay Prop": {"Best Quality": 15, "Strongest Part": 20, "Fastest Print": 10, "Balanced": 15, "Lowest Cost": 10, "Best Surface Finish": 15},
            "Toy": {"Best Quality": 18, "Strongest Part": 22, "Fastest Print": 12, "Balanced": 18, "Lowest Cost": 10, "Best Surface Finish": 15},
            "Container": {"Best Quality": 18, "Strongest Part": 28, "Fastest Print": 12, "Balanced": 20, "Lowest Cost": 12, "Best Surface Finish": 15},
            "Planter": {"Best Quality": 15, "Strongest Part": 25, "Fastest Print": 10, "Balanced": 18, "Lowest Cost": 10, "Best Surface Finish": 15},
            "Vase": {"Best Quality": 10, "Strongest Part": 15, "Fastest Print": 5, "Balanced": 10, "Lowest Cost": 5, "Best Surface Finish": 10},
            "Decorative Object": {"Best Quality": 12, "Strongest Part": 18, "Fastest Print": 8, "Balanced": 12, "Lowest Cost": 8, "Best Surface Finish": 12},
            "Mechanical Part": {"Best Quality": 20, "Strongest Part": 40, "Fastest Print": 15, "Balanced": 25, "Lowest Cost": 15, "Best Surface Finish": 18},
            "Art Piece": {"Best Quality": 15, "Strongest Part": 20, "Fastest Print": 10, "Balanced": 15, "Lowest Cost": 10, "Best Surface Finish": 15},
        }
        values = mapping.get(print_type, mapping.get("Functional Part", {}))
        return values.get(goal, 18)

    def _pattern_for(self, goal: str) -> str:
        if goal == "Strongest Part":
            return "Gyroid"
        if goal == "Fastest Print":
            return "Lines"
        if goal == "Best Surface Finish":
            return "Grid"
        return "Gyroid"

    def _print_speed_for(self, printer: Dict[str, Any], goal: str) -> int:
        base = int(printer.get("max_speed", 500) * 0.45)
        if goal == "Fastest Print":
            return int(base * 1.2)
        if goal == "Best Quality":
            return int(base * 0.75)
        if goal == "Strongest Part":
            return int(base * 0.8)
        return base

    def _travel_speed_for(self, printer: Dict[str, Any], goal: str) -> int:
        base = int(printer.get("max_speed", 500) * 0.65)
        if goal == "Fastest Print":
            return int(base * 1.1)
        if goal == "Best Quality":
            return int(base * 0.8)
        return base

    def _cooling_for(self, filament: Dict[str, Any], goal: str) -> int:
        material = filament.get("material", "PLA").upper()
        if material == "PLA":
            return 100 if goal not in ["Strongest Part", "Fastest Print"] else 80
        if material == "PETG":
            return 40
        if material == "TPU":
            return 20
        return 70

    def _supports_for(self, print_type: str, filament: Dict[str, Any]) -> str:
        material = filament.get("material", "PLA").upper()
        if print_type == "Vase":
            return "No supports; use vase mode or spiralize outer contour"
        if print_type == "Planter":
            return "Supports for overhangs > 45 degrees; use tree supports if needed"
        if material == "TPU":
            return "Support material or breakaway support for overhangs; reduce support density"
        return "Normal tree or grid supports on overhangs greater than 45°"

    def _adhesion_for(self, filament: Dict[str, Any], print_type: str) -> str:
        material = filament.get("material", "PLA").upper()
        if material == "PETG":
            return "Textured plate + light glue stick if needed"
        if material == "TPU":
            return "PEI plate with a small brim"
        if print_type in ["Miniature", "Art Piece", "Decorative Object"]:
            return "Clean plate + light brim for small details"
        return "Brim recommended for small parts and bowls"

    def _nozzle_temp(self, filament: Dict[str, Any], printer: Dict[str, Any], goal: str) -> int:
        base = int(filament.get("nozzle_temp", 210))
        if goal == "Fastest Print":
            return base + 5
        if goal == "Best Quality":
            return base - 3
        if goal == "Best Surface Finish":
            return base - 2
        return base

    def _bed_temp(self, filament: Dict[str, Any], printer: Dict[str, Any], goal: str) -> int:
        base = int(filament.get("bed_temp", 60))
        if goal == "Strongest Part":
            return base + 10
        return base

    def optimize(self, printer_name: str, filament_name: str, print_type: str, goal: str) -> Dict[str, Any]:
        printer = self._get_printer(printer_name)
        filament = self._get_filament(filament_name)
        layer_height = self._layer_height_for(print_type, goal)
        nozzle = self._nozzle_temp(filament, printer, goal)
        bed = self._bed_temp(filament, printer, goal)
        wall_count = self._wall_count_for(print_type, goal)
        top_layers = 5 if goal in ["Best Quality", "Best Surface Finish", "Strongest Part"] else 4
        bottom_layers = top_layers
        infill = self._infill_percent_for(print_type, goal)
        infill_pattern = self._pattern_for(goal)
        print_speed = self._print_speed_for(printer, goal)
        travel_speed = self._travel_speed_for(printer, goal)
        cooling = self._cooling_for(filament, goal)
        support_recommendation = self._supports_for(print_type, filament)
        adhesion_recommendation = self._adhesion_for(filament, print_type)

        settings = {
            "printer": printer_name,
            "filament": filament_name,
            "print_type": print_type,
            "goal": goal,
            "layer_height": round(layer_height, 2),
            "nozzle_temperature": nozzle,
            "bed_temperature": bed,
            "wall_count": wall_count,
            "top_layers": top_layers,
            "bottom_layers": bottom_layers,
            "infill_percent": infill,
            "infill_pattern": infill_pattern,
            "print_speed": print_speed,
            "travel_speed": travel_speed,
            "cooling_percent": cooling,
            "support_recommendation": support_recommendation,
            "build_plate_adhesion": adhesion_recommendation,
            "estimated_quality": 0,
            "estimated_strength": 0,
            "estimated_speed": 0,
            "difficulty_rating": 0,
            "suggested_improvements": []
        }

        analysis = {
            "quality": 88 if goal == "Best Quality" else 80,
            "strength": 84 if goal == "Strongest Part" else 76,
            "speed": 90 if goal == "Fastest Print" else 74,
            "difficulty": 5 if print_type in ["Miniature", "Art Piece", "Cosplay Prop"] else 4,
            "suggestions": []
        }

        if print_type == "Miniature":
            analysis["quality"] += 8
            analysis["difficulty"] += 1
            analysis["suggestions"].append("Use a smaller nozzle or slower outer wall speed for more detail.")
        if goal == "Strongest Part":
            analysis["strength"] += 10
            analysis["suggestions"].append("Increase wall count and use gyroid infill for stronger parts.")
        if goal == "Fastest Print":
            analysis["speed"] += 10
            analysis["suggestions"].append("Lower the infill and reduce print detail for quicker jobs.")
        if filament.get("material", "PLA").upper() == "TPU":
            analysis["suggestions"].append("Slow the print speed slightly and use a direct drive setup for cleaner TPU results.")
        if print_type == "Planter":
            analysis["suggestions"].append("Use a slightly larger wall count to improve rigidity and reduce cracking.")

        settings["estimated_quality"] = analysis["quality"]
        settings["estimated_strength"] = analysis["strength"]
        settings["estimated_speed"] = analysis["speed"]
        settings["difficulty_rating"] = analysis["difficulty"]
        settings["suggested_improvements"] = analysis["suggestions"]
        return settings

    def ai_recommendation(self, description: str) -> Dict[str, Any]:
        text = description.lower()
        printer = "Bambu X1C"
        filament = "Bambu PLA"
        print_type = "Functional Part"
        goal = "Balanced"

        if "x1c" in text or "x1" in text:
            printer = "Bambu X1C"
        elif "p1s" in text or "p1" in text:
            printer = "Bambu P1S"
        elif "a1 mini" in text or "mini" in text:
            printer = "Bambu A1 Mini"
        elif "a1" in text:
            printer = "Bambu A1"
        elif "mk4" in text or "prusa" in text:
            printer = "Prusa MK4"
        elif "ender 3 v3" in text:
            printer = "Ender 3 V3"
        elif "ender 3" in text:
            printer = "Ender 3"

        if "petg" in text:
            filament = "Bambu PETG"
        elif "tpu" in text:
            filament = "Bambu TPU"
        elif "pla+" in text or "pla plus" in text:
            filament = "eSUN PLA+"
        elif "sunlu" in text:
            filament = "Sunlu PLA"
        elif "elegoo" in text:
            filament = "Elegoo PLA"
        elif "pla" in text:
            filament = "Bambu PLA"

        if "miniature" in text or "dragon" in text or "small" in text:
            print_type = "Miniature"
        elif "planter" in text:
            print_type = "Planter"
        elif "container" in text or "box" in text or "holder" in text:
            print_type = "Container"
        elif "mechanical" in text or "gear" in text or "bracket" in text:
            print_type = "Mechanical Part"
        elif "vase" in text:
            print_type = "Vase"
        elif "toy" in text:
            print_type = "Toy"
        elif "prop" in text or "cosplay" in text:
            print_type = "Cosplay Prop"
        elif "art" in text or "sculpture" in text:
            print_type = "Art Piece"

        if "quality" in text or "detailed" in text or "detail" in text or "best" in text:
            goal = "Best Quality"
        elif "strong" in text or "structural" in text or "load" in text:
            goal = "Strongest Part"
        elif "fast" in text or "quick" in text or "speed" in text:
            goal = "Fastest Print"
        elif "finish" in text or "surface" in text:
            goal = "Best Surface Finish"
        elif "cheap" in text or "cost" in text:
            goal = "Lowest Cost"

        return self.optimize(printer, filament, print_type, goal)
