"""Create or verify a sanitized manifest for a locally obtained simulator folder."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXCLUDED_NAMES = {".DS_Store"}
EXCLUDED_TOP_LEVEL = {"JammersSimulatorData"}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_relative(path: Path, root: Path) -> str:
    relative = path.relative_to(root)
    if any(part in {"..", ""} for part in relative.parts):
        raise ValueError(f"unsafe relative path: {relative}")
    return relative.as_posix()


def included(path: Path, root: Path, include_all: bool = False) -> bool:
    relative = path.relative_to(root)
    if include_all:
        return True
    return path.name not in EXCLUDED_NAMES and not any(
        part in EXCLUDED_TOP_LEVEL for part in relative.parts
    )


def collect(root: Path, include_all: bool = False) -> list[dict]:
    root = root.resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and included(path, root, include_all):
            rows.append({"path": safe_relative(path, root), "bytes": path.stat().st_size, "sha256": digest(path)})
    return rows


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("files"), list):
        raise TypeError("manifest must contain a files list")
    return data


def verify(root: Path, manifest: dict) -> tuple[list[str], list[str]]:
    mismatches = []
    for row in manifest["files"]:
        relative = row.get("path")
        if not isinstance(relative, str) or Path(relative).is_absolute() or ".." in Path(relative).parts:
            mismatches.append(f"unsafe manifest path: {relative!r}")
            continue
        path = root / relative
        if not path.is_file():
            mismatches.append(f"missing: {relative}")
            continue
        if path.stat().st_size != row.get("bytes") or digest(path) != row.get("sha256"):
            mismatches.append(f"changed: {relative}")
    expected = {row["path"] for row in manifest["files"]}
    actual = {row["path"] for row in collect(root, manifest.get("scope") == "complete-local-sample")}
    extras = sorted(actual - expected)
    return mismatches, extras


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--write", action="store_true", help="write a new manifest from the local folder")
    parser.add_argument("--include-all", action="store_true", help="include .DS_Store and mutable runtime state")
    args = parser.parse_args()
    if args.write and args.verify:
        parser.error("choose --write or --verify")
    if args.write:
        rows = collect(args.root, args.include_all)
        output = {
            "schema_version": 1,
            "source_label": "user-obtained-local-sample",
            "scope": "complete-local-sample" if args.include_all else "program-and-runtime",
            "files": rows,
        }
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {len(rows)} file records to {args.manifest}")
        return 0
    manifest = load_manifest(args.manifest)
    mismatches, extras = verify(args.root, manifest)
    for item in mismatches:
        print(item)
    if extras:
        print(f"notice: {len(extras)} unlisted files (not deleted)")
    if mismatches:
        return 1
    print(f"verified {len(manifest['files'])} manifest records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
