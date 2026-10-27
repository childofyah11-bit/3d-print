from __future__ import annotations

from typing import Dict, List


class AnalysisEngine:
    """Creates quality, strength, and time estimates using print settings and material input."""

    @staticmethod
    def estimate_quality(settings: Dict[str, object]) -> int:
        base = int(settings.get("estimated_quality", 75))
        return max(0, min(100, base))

    @staticmethod
    def estimate_strength(settings: Dict[str, object]) -> int:
        base = int(settings.get("estimated_strength", 70))
        return max(0, min(100, base))

    @staticmethod
    def estimate_speed(settings: Dict[str, object]) -> int:
        base = int(settings.get("estimated_speed", 70))
        return max(0, min(100, base))

    @staticmethod
    def estimate_difficulty(settings: Dict[str, object]) -> int:
        difficulty = int(settings.get("difficulty_rating", 5))
        return max(1, min(10, difficulty))

    @staticmethod
    def calculate_print_time(print_type: str, layer_height: float, print_speed: int) -> int:
        type_factor = {
            "Miniature": 90,
            "Functional Part": 60,
            "Cosplay Prop": 80,
            "Toy": 55,
            "Container": 70,
            "Planter": 65,
            "Vase": 45,
            "Decorative Object": 60,
            "Mechanical Part": 75,
            "Art Piece": 100,
        }
        minutes = type_factor.get(print_type, 60)
        speed_factor = 100 / max(print_speed, 1)
        return max(20, int(minutes * speed_factor * (0.8 + (layer_height / 0.25))))

    @staticmethod
    def calculate_material_usage(print_type: str, infill_percent: int, layer_height: float) -> float:
        base = {
            "Miniature": 7,
            "Functional Part": 20,
            "Cosplay Prop": 15,
            "Toy": 18,
            "Container": 28,
            "Planter": 30,
            "Vase": 22,
            "Decorative Object": 16,
            "Mechanical Part": 34,
            "Art Piece": 12,
        }
        grams = base.get(print_type, 20)
        infill_factor = 1 + (infill_percent / 100)
        return round(grams * infill_factor * (0.9 + layer_height), 1)

    @staticmethod
    def estimate_material_cost(material_grams: float, filament_name: str) -> float:
        cost_per_kg = {
            "Bambu PLA": 28,
            "Bambu PETG": 32,
            "Bambu TPU": 35,
            "Sunlu PLA": 22,
            "Elegoo PLA": 24,
            "eSUN PLA+": 26,
            "Overture PLA": 23,
            "Generic PLA": 20,
            "Generic PETG": 22,
            "Generic TPU": 28,
        }
        price = cost_per_kg.get(filament_name, 24)
        return round((material_grams / 1000) * price, 2)

    @staticmethod
    def generate_suggestions(settings: Dict[str, object]) -> List[str]:
        suggestions = []
        if float(settings.get("layer_height", 0.2)) < 0.15:
            suggestions.append("Lower layer height for detailed features and smoother surfaces.")
        if int(settings.get("infill_percent", 20)) > 25:
            suggestions.append("Reduce infill slightly if the part does not need extra rigidity.")
        if int(settings.get("cooling_percent", 70)) < 50:
            suggestions.append("Increase fan cooling for a cleaner surface finish on PLA.")
        if settings.get("support_recommendation", "") and "Supports" in str(settings.get("support_recommendation", "")):
            suggestions.append("Add supports to overhangs to reduce failed edges and weak bridges.")
        if not suggestions:
            suggestions.append("Your settings are balanced. Consider making one small adjustment at a time.")
        return suggestions
