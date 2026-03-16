from utils.file_utils import write_file

def build_simulation():

    code = """

def run_simulation():

    print("Running tournament simulation")

"""

    write_file("services/simulation-worker/simulate.py", code)