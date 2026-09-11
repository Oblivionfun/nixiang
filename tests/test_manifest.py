import json
from pathlib import Path

from tools.inventory import collect, verify


def test_repository_manifest_is_relative_and_sanitized():
    manifest = json.loads(Path("simulator/artifact-manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 1
    assert manifest["source_label"] == "user-obtained-local-sample"
    assert manifest["scope"] == "program-and-runtime"
    paths = [row["path"] for row in manifest["files"]]
    assert paths
    assert all(not Path(path).is_absolute() and ".." not in Path(path).parts for path in paths)
    assert all(not path.startswith("JammersSimulatorData/") for path in paths)
    assert all(len(row["sha256"]) == 64 for row in manifest["files"])

    complete = json.loads(Path("simulator/full-artifact-manifest.json").read_text(encoding="utf-8"))
    assert complete["scope"] == "complete-local-sample"
    assert len(complete["files"]) == 272
    assert any("JammersSimulatorData" in row["path"] for row in complete["files"])


def test_verify_accepts_fixture(tmp_path):
    (tmp_path / "app" / "WebView2Runtime").mkdir(parents=True)
    (tmp_path / "app" / "main.exe").write_bytes(b"fixture")
    (tmp_path / "JammersSimulatorData").mkdir()
    (tmp_path / "JammersSimulatorData" / "state.sqlite3").write_bytes(b"mutable")
    rows = collect(tmp_path)
    manifest = {"schema_version": 1, "source_label": "fixture", "files": rows}
    assert verify(tmp_path, manifest) == ([], [])
