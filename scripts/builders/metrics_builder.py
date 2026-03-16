from utils.file_utils import write_file

def build_metrics_ingestion():
    print("Building metrics ingestion...")

    placeholder = """
def run_metrics_pipeline(season: int):
    print(f"TODO: fetch and load advanced metrics for season {season}")
"""

    write_file("services/ingestion-worker/pipelines/metrics_pipeline.py", placeholder)