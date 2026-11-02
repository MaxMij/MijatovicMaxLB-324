import hashlib
import json
from zipfile import ZipFile

from scripts.package_app import build_package


def test_azure_package_contains_only_runtime_files(tmp_path):
    output = build_package(tmp_path / "app.zip", "test-revision")
    with ZipFile(output) as archive:
        assert set(archive.namelist()) == {
            "app.py",
            "requirements.txt",
            "templates/index.html",
            "templates/login.html",
            "build-info.json",
        }
        assert json.loads(archive.read("build-info.json")) == {
            "revision": "test-revision"
        }
    assert output.with_suffix(".zip.sha256").read_text() == (
        f"{hashlib.sha256(output.read_bytes()).hexdigest()}  app.zip\n"
    )
