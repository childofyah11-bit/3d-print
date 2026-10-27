from __future__ import annotations

import json
import os
from typing import Any, Dict, List


class ProfileManager:
    """Central manager for printers, filament data, profiles, and app settings."""

    def __init__(self, base_dir: str | None = None):
        self.base_dir = base_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.data_dir = os.path.join(self.base_dir, "data")
        self.printers_path = os.path.join(self.data_dir, "printers.json")
        self.filaments_path = os.path.join(self.data_dir, "filaments.json")
        self.profiles_path = os.path.join(self.data_dir, "profiles.json")

    def _read_json(self, path: str) -> Any:
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write_json(self, path: str, payload: Any) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

    def load_printers(self) -> List[Dict[str, Any]]:
        data = self._read_json(self.printers_path)
        return data.get("printers", [])

    def load_filaments(self) -> List[Dict[str, Any]]:
        data = self._read_json(self.filaments_path)
        return data.get("filaments", [])

    def load_profiles(self) -> Dict[str, Any]:
        data = self._read_json(self.profiles_path)
        if not data:
            default = {
                "app_settings": {
                    "theme": "dark",
                    "autosave": True,
                    "recent_projects": [],
                    "favorites": []
                },
                "profiles": []
            }
            self._write_json(self.profiles_path, default)
            return default
        data.setdefault("app_settings", {
            "theme": "dark",
            "autosave": True,
            "recent_projects": [],
            "favorites": []
        })
        data.setdefault("profiles", [])
        return data

    def save_profiles(self, profile_data: Dict[str, Any]) -> None:
        self._write_json(self.profiles_path, profile_data)

    def save_profile(self, name: str, profile: Dict[str, Any]) -> None:
        data = self.load_profiles()
        profiles = data.get("profiles", [])
        merged = False
        for index, item in enumerate(profiles):
            if item.get("name") == name:
                profiles[index] = profile
                merged = True
                break
        if not merged:
            profiles.append(profile)
        data["profiles"] = profiles
        self.save_profiles(data)

    def load_profile(self, name: str) -> Dict[str, Any] | None:
        for profile in self.load_profiles().get("profiles", []):
            if profile.get("name") == name:
                return profile
        return None

    def list_profile_names(self) -> List[str]:
        return [profile.get("name", "Unnamed") for profile in self.load_profiles().get("profiles", [])]

    def validate_profile(self, profile: Dict[str, Any]) -> bool:
        required = ["name", "printer", "filament", "print_type", "goal", "settings"]
        for field in required:
            if field not in profile:
                return False
        if not isinstance(profile.get("settings", {}), dict):
            return False
        return True

    def load_app_settings(self) -> Dict[str, Any]:
        data = self.load_profiles()
        return data.get("app_settings", {
            "theme": "dark",
            "autosave": True,
            "recent_projects": [],
            "favorites": []
        })

    def save_app_settings(self, settings: Dict[str, Any]) -> None:
        data = self.load_profiles()
        data["app_settings"] = settings
        self.save_profiles(data)

    def export_profile(self, profile_name: str, export_path: str) -> None:
        profile = self.load_profile(profile_name)
        if profile is None:
            raise FileNotFoundError(f"Profile '{profile_name}' was not found.")
        with open(export_path, "w", encoding="utf-8") as file:
            json.dump(profile, file, indent=2)

    def import_profile(self, import_path: str) -> Dict[str, Any]:
        with open(import_path, "r", encoding="utf-8") as file:
            profile = json.load(file)
        if not self.validate_profile(profile):
            raise ValueError("The imported profile is missing required fields.")
        self.save_profile(profile["name"], profile)
        return profile

    def add_recent_project(self, name: str) -> None:
        settings = self.load_app_settings()
        recent = settings.get("recent_projects", [])
        if name in recent:
            recent.remove(name)
        recent.insert(0, name)
        settings["recent_projects"] = recent[:8]
        self.save_app_settings(settings)

    def add_favorite(self, name: str) -> None:
        settings = self.load_app_settings()
        favorites = settings.get("favorites", [])
        if name not in favorites:
            favorites.append(name)
        settings["favorites"] = favorites
        self.save_app_settings(settings)


if __name__ == "__main__":
    manager = ProfileManager()
    print(manager.load_printers())
