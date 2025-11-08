import json
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"

def load_config(category: str = "personas", name: str = "fashionAdvisor"):
    """
    Load a JSON file from a given category inside the config folder.
    Example: load_config("personas", "alice") → loads config/personas/alice.json
    """
    file_path = CONFIG_DIR / category / f"{name}.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Config '{name}' not found in '{category}' folder.")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

