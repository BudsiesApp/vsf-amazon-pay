#!/usr/bin/env python3
"""Publish a source-selected immutable Amazon Pay preview."""
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = "BudsiesApp/vsf-amazon-pay"


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], stderr=subprocess.PIPE).decode().strip()


def resolve(ref):
    if not re.fullmatch(r"[0-9a-f]{40}", ref):
        if ref.startswith('-') or not re.fullmatch(r"[A-Za-z0-9_./-]+", ref):
            raise ValueError("invalid source ref")
        check = ref if ref.startswith('refs/') else 'refs/heads/' + ref
        git("check-ref-format", check)
        ref = check
    git("fetch", "--no-tags", "origin", ref)
    return git("rev-parse", "--verify", "FETCH_HEAD^{commit}")


def identity(packaging, sources, toolchain):
    return {"formatVersion": 1, "repository": REPOSITORY, "packagingRevision": packaging,
            "sources": sources, "toolchain": toolchain}


def tag_for(value):
    canonical = json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    return 'package-preview-' + hashlib.sha256(canonical).hexdigest()


def main():
    parser = argparse.ArgumentParser(description='Publish an immutable Amazon Pay preview')
    parser.add_argument('--source-ref', required=True, help='Amazon Pay source branch, full ref or commit')
    args = parser.parse_args()
    if git('status', '--porcelain', '--', 'scripts/package-release.py', 'scripts/package-release.json',
           'scripts/publish-release.py', 'scripts/preview-packages.py', 'scripts/preview-cleanup.py'):
        raise ValueError('publishing inputs must be committed')
    packaging = git('rev-parse', 'HEAD^{commit}')
    cleaner = load('preview-cleanup')
    tracking = cleaner.GitHub()
    repository = tracking.repository()
    if repository.get('full_name', '').lower() != REPOSITORY.lower():
        raise ValueError('repository could not be verified')
    with tracking.lock(packaging):
        branches, pinned = cleaner.associations((args.source_ref,), (False,), repository['default_branch'])
        pinned = pinned or any(tracking.protected(branch) for branch in branches)
        sources = {'amazonPay': resolve(args.source_ref)}
        value = identity(packaging, sources, {'python': sys.version.split()[0], 'zlib': zlib.ZLIB_RUNTIME_VERSION})
        tag = tag_for(value)
        registry, parent = tracking.read_registry()
        existed = tracking.release(tag) is not None
        unknown_tag = not existed and tag not in registry['previews'] and tracking.ref(tag) is not None
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            load('package-release').prepare(path, tag, sources['amazonPay'], value)
            publisher = load('publish-release')
            publisher.publish(publisher.GitHub(), tag, path, preview=True)
            manifest = json.loads((path / 'release-manifest.json').read_text())
        release = tracking.release(tag)
        if cleaner.register(registry, tag, release, packaging, branches, pinned, existed or unknown_tag):
            tracking.write_registry(registry, parent, packaging)
    base = f'https://github.com/{REPOSITORY}/releases/download/{tag}/'
    print(json.dumps({'releaseTag': tag, 'identity': value,
                      'packages': [{**package, 'url': base + package['asset']} for package in manifest['packages']],
                      'manifestUrl': base + 'release-manifest.json', 'checksumsUrl': base + 'SHA256SUMS'}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, subprocess.CalledProcessError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
