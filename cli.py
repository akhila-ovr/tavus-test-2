import argparse, json
from pathlib import Path

# base config folders
BASE = Path(__file__).resolve().parent / "config"
FOLDERS = {
    "persona": BASE / "personas",
    "conversation": BASE / "conversations",
    "document": BASE / "documents",
}


def load_json(folder, name):
    """Load a JSON file (e.g., personas/alice.json)."""
    path = folder / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"{name}.json not found in {folder}")
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--persona")
    parser.add_argument("--conversation")
    parser.add_argument("--document")
    args = parser.parse_args()

    persona = load_json(FOLDERS["persona"], args.persona) if args.persona else None
    convo = (
        load_json(FOLDERS["conversation"], args.conversation)
        if args.conversation
        else None
    )
    doc = load_json(FOLDERS["document"], args.document) if args.document else None

    return persona, convo, doc


if __name__ == "__main__":
    main()
