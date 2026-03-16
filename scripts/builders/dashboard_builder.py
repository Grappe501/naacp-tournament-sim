from utils.file_utils import write_file

def build_dashboard():

    write_file(
        "apps/dashboard/README.md",
        "# Dashboard\nDisplays simulation results."
    )