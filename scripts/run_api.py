import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
app_file = ROOT / "services" / "api" / "app.py"

subprocess.run([sys.executable, str(app_file)], check=True)
