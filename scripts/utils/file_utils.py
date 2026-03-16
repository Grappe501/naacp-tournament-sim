from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def write_file(path: str, content: str) -> None:
    file_path = ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content.strip() + "\n", encoding="utf-8")

def ensure_dir(path: str) -> None:
    dir_path = ROOT / path
    dir_path.mkdir(parents=True, exist_ok=True)

def append_file(path: str, content: str) -> None:
    file_path = ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(content)

def file_exists(path: str) -> bool:
    return (ROOT / path).exists()