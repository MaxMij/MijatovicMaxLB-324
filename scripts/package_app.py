"""Build the exact source ZIP sent to Azure, without local secrets or tooling."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]


def build_package(output, revision):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    files = [ROOT / "app.py", ROOT / "requirements.txt"]
    files.extend(sorted((ROOT / "templates").rglob("*.html")))
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, file.relative_to(ROOT).as_posix())
        archive.writestr("build-info.json", json.dumps({"revision": revision}) + "\n")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(".zip.sha256").write_text(
        f"{digest}  {output.name}\n", encoding="utf-8"
    )
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="dist/app.zip")
    parser.add_argument("--revision")
    args = parser.parse_args()
    revision = (
        args.revision
        or subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    )
    print(build_package(args.output, revision))
