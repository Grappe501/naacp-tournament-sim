from utils.file_utils import write_file


def build_environment():

    print("Building Python environment...")

    requirements = """
flask
requests
pandas
numpy
sqlalchemy
psycopg2-binary
python-dotenv
tqdm
"""

    write_file("requirements.txt", requirements)