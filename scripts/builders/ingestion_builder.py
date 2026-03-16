from utils.file_utils import write_file

def build_ingestion():

    print("Building ingestion pipeline...")

    code = """

def run_ingestion():

    print("Starting data ingestion")

"""

    write_file("services/ingestion-worker/ingest.py", code)