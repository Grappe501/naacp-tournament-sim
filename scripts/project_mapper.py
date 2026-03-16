import os
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPORT = {
    "builders": [],
    "services": [],
    "missing_imports": [],
    "pipelines": [],
    "simulation_modules": [],
    "database_modules": [],
    "problems": []
}


def list_python_files():
    files = []

    for root, dirs, filenames in os.walk(ROOT):

        if ".git" in root:
            continue

        for f in filenames:
            if f.endswith(".py"):
                files.append(Path(root) / f)

    return files


def analyze_imports(file_path):

    try:
        tree = ast.parse(file_path.read_text())
    except Exception as e:
        REPORT["problems"].append(
            f"Parse error in {file_path}: {e}"
        )
        return

    for node in ast.walk(tree):

        if isinstance(node, ast.ImportFrom):

            module = node.module

            if not module:
                continue

            module_path = module.replace(".", "/")

            found = False

            for py in list_python_files():
                if module_path in str(py):
                    found = True
                    break

            if not found:
                REPORT["missing_imports"].append(
                    f"{file_path} -> {module}"
                )


def detect_builders(file_path):

    if "builders" in str(file_path):
        REPORT["builders"].append(str(file_path))


def detect_services(file_path):

    if "services" in str(file_path):
        REPORT["services"].append(str(file_path))


def detect_pipelines(file_path):

    if "pipeline" in str(file_path).lower():
        REPORT["pipelines"].append(str(file_path))


def detect_simulation_modules(file_path):

    if "simulation_worker" in str(file_path):
        REPORT["simulation_modules"].append(str(file_path))


def detect_database_modules(file_path):

    if "packages/db" in str(file_path):
        REPORT["database_modules"].append(str(file_path))


def analyze_repo():

    print("Scanning repository...")

    files = list_python_files()

    for f in files:

        detect_builders(f)
        detect_services(f)
        detect_pipelines(f)
        detect_simulation_modules(f)
        detect_database_modules(f)

        analyze_imports(f)

    print_report()


def print_section(title, data):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    if not data:
        print("None")

    for d in data:
        print(d)


def print_report():

    print("\n\nPROJECT STRUCTURE REPORT")

    print_section("BUILDERS", REPORT["builders"])

    print_section("SERVICES", REPORT["services"])

    print_section("PIPELINES", REPORT["pipelines"])

    print_section("SIMULATION MODULES", REPORT["simulation_modules"])

    print_section("DATABASE MODULES", REPORT["database_modules"])

    print_section("MISSING IMPORTS", REPORT["missing_imports"])

    print_section("PROBLEMS", REPORT["problems"])

    print("\n\nPROJECT COMPLETION ANALYSIS")

    readiness = 100

    if REPORT["missing_imports"]:
        readiness -= 20

    if len(REPORT["pipelines"]) < 3:
        readiness -= 20

    if len(REPORT["simulation_modules"]) < 5:
        readiness -= 20

    if len(REPORT["database_modules"]) < 3:
        readiness -= 10

    print(f"\nEstimated System Readiness: {readiness}%")

    if readiness < 60:
        print("Project NOT ready to run.")

    elif readiness < 80:
        print("Project partially ready. Missing components.")

    else:
        print("Project structurally ready.")


if __name__ == "__main__":
    analyze_repo()