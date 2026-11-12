#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVISION = "d9f6fcd224938bbcb7472306946d2a947c3ae5e6"
spec = importlib.util.spec_from_file_location("publisher", ROOT / "scripts/publish-release.py")
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)


class PackageReleaseTest(unittest.TestCase):
    def test_archive_provenance_and_repeatability(self):
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / "first", Path(tmp) / "second"
            for output in (first, second):
                subprocess.run(["python3", str(ROOT / "scripts/package-release.py"),
                                "--output", str(output), "--tag", "packages-37220-v1"], check=True)
            for name in ("amazon-pay.tgz", "release-manifest.json", "SHA256SUMS"):
                self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())
            metadata = json.loads((first / "release-manifest.json").read_text())
            package = metadata["packages"][0]
            self.assertEqual(package["sourceRevision"], REVISION)
            self.assertEqual(package["sourcePath"], "API/amazon-pay")
            self.assertEqual(package["name"], "@vue-storefront-api/amazon-pay")
            self.assertEqual(package["version"], "0.1.0")
            self.assertEqual(metadata["releaseTag"], "packages-37220-v1")
            self.assertEqual(metadata["packagingRevision"], subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip())
            digest = hashlib.sha256((first / "amazon-pay.tgz").read_bytes()).hexdigest()
            self.assertEqual(package["sha256"], digest)
            self.assertEqual((first / "SHA256SUMS").read_text(), digest + "  amazon-pay.tgz\n")
            source = subprocess.check_output(["git", "archive", REVISION, "API/amazon-pay"], cwd=ROOT)
            import io
            with tarfile.open(fileobj=io.BytesIO(source)) as original, tarfile.open(first / "amazon-pay.tgz") as archive:
                expected = {m.name.removeprefix("API/amazon-pay/"): original.extractfile(m).read()
                            for m in original if m.isfile()}
                actual = {m.name.removeprefix("package/"): archive.extractfile(m).read()
                          for m in archive if m.isfile()}
            self.assertEqual(actual, expected)
            self.assertIn("index.js", actual)
            self.assertNotIn(b"gitpkg.vercel.app", actual["package.json"])

    def test_publication_preflight_and_partial_recovery(self):
        class FakeGitHub:
            def __init__(self, assets=None, exists=True, sha="a" * 40):
                self.assets = dict(assets or {})
                self.exists = exists
                self.sha = sha
                self.writes = []

            def commit(self, tag):
                return self.sha

            def release(self, tag):
                return {"assets": [{"name": k, "id": k} for k in self.assets]} if self.exists else None

            def download(self, asset):
                return self.assets[asset["id"]]

            def create(self, tag):
                self.writes.append("create")
                self.exists = True

            def upload(self, tag, path):
                self.writes.append(path.name)
                self.assets[path.name] = path.read_bytes()

        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "amazon-pay.tgz").write_bytes(b"archive")
            (directory / "SHA256SUMS").write_bytes(b"checksum")
            (directory / "release-manifest.json").write_text(json.dumps(
                {"releaseTag": "packages-test", "packagingRevision": "a" * 40}))
            expected = {name: (directory / name).read_bytes() for name in publisher.ASSETS}
            for initial, exists, count in (({}, False, 4), (expected, True, 0),
                                           ({"amazon-pay.tgz": expected["amazon-pay.tgz"]}, True, 2)):
                fake = FakeGitHub(initial, exists)
                publisher.publish(fake, "packages-test", directory)
                self.assertEqual(fake.assets, expected)
                self.assertEqual(len(fake.writes), count)
            for initial, sha in (({"SHA256SUMS": b"conflict"}, "a" * 40), ({}, "b" * 40)):
                fake = FakeGitHub(initial, sha=sha)
                with self.assertRaises(ValueError):
                    publisher.publish(fake, "packages-test", directory)
                self.assertEqual(fake.assets, initial)
                self.assertEqual(fake.writes, [])


if __name__ == "__main__":
    unittest.main()
