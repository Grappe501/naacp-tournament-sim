from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def write_file(path, content):

    file_path = ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def ensure_dir(path):

    dir_path = ROOT / path
    dir_path.mkdir(parents=True, exist_ok=True)