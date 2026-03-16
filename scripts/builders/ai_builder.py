from utils.file_utils import write_file

def build_ai():
    print("Building AI registry...")

    write_file(
        "packages/prompt-registry/prompts.md",
        "# Prompt Registry\n\nAll AI prompts used by the system are registered here."
    )