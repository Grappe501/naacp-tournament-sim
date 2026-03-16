from utils.file_utils import write_file

def build_governance():

    print("Building governance system...")

    write_file(
        "governance/protocols/build-protocol.md",
        "# Build Protocol\nDefines system construction rules."
    )

    write_file(
        "governance/protocols/ai-build-protocol.md",
        "# AI Build Protocol\nDefines AI participation rules."
    )

    write_file(
        "governance/drift/drift-taxonomy.md",
        "# Drift Taxonomy\nDefines architecture drift detection."
    )