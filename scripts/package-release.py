#!/usr/bin/env python3
"""Create deterministic Amazon Pay release assets without installing dependencies."""
import argparse
import gzip
import hashlib
import io
import json
import re
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = "API/amazon-pay"
ASSET = "amazon-pay.tgz"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def prepare(output, tag):
    revision = json.loads((ROOT / "scripts/package-release.json").read_text())["amazonPayRevision"]
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("amazonPayRevision must be a full commit SHA")
    resolved = git("rev-parse", "--verify", revision + "^{commit}").decode().strip()
    if resolved != revision:
        raise ValueError("source revision does not resolve to the selected commit")
    packaging = git("rev-parse", "HEAD^{commit}").decode().strip()
    source = git("archive", revision, SOURCE_PATH)
    output.mkdir(parents=True, exist_ok=True)
    target = output / ASSET
    with tarfile.open(fileobj=io.BytesIO(source), mode="r:") as original:
        members = [m for m in original.getmembers() if m.isfile() and m.name.startswith(SOURCE_PATH + "/")]
        files = {m.name[len(SOURCE_PATH) + 1:]: original.extractfile(m).read() for m in members}
        modes = {m.name[len(SOURCE_PATH) + 1:]: m.mode for m in members}
    manifest = json.loads(files["package.json"])
    if b"gitpkg.vercel.app" in files["package.json"]:
        raise ValueError("package manifest contains GitPkg")
    with target.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT) as archive:
            for name in sorted(files):
                info = tarfile.TarInfo("package/" + name)
                info.size = len(files[name])
                info.mode = modes[name]
                info.mtime = 0
                archive.addfile(info, io.BytesIO(files[name]))
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    metadata = {"repository": "BudsiesApp/vsf-amazon-pay", "releaseTag": tag,
                "packagingRevision": packaging, "packages": [{"name": manifest["name"],
                "version": manifest["version"], "sourceRevision": resolved,
                "sourcePath": SOURCE_PATH, "asset": ASSET, "sha256": digest}]}
    (output / "release-manifest.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (output / "SHA256SUMS").write_text(f"{digest}  {ASSET}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tag", required=True)
    args = parser.parse_args()
    prepare(args.output, args.tag)
