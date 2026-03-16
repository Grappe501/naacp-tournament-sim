from utils.file_utils import write_file

def build_boxscore_ingestion():
    print("Building boxscore ingestion...")

    placeholder = """
def run_boxscore_pipeline(game_external_id: str):
    print(f"TODO: fetch and load boxscore for game {game_external_id}")
"""

    write_file("services/ingestion-worker/pipelines/boxscores_pipeline.py", placeholder)