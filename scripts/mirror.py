"""Pin every heki release on PyPI newer than the one this repository pins: for each, set the
version in pyproject.toml and README.md, commit, and tag `v<version>`. Prereleases are skipped.

usage: python3 scripts/mirror.py   (from the repository root; pushing is left to the caller)
"""

import json
import re
import subprocess
import urllib.request
from pathlib import Path


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def current() -> str:
    text = Path("pyproject.toml").read_text()
    return re.search(r'"heki==([0-9.]+)"', text).group(1)


def releases() -> list[str]:
    with urllib.request.urlopen("https://pypi.org/pypi/heki/json", timeout=30) as response:
        data = json.load(response)
    final = [v for v, files in data["releases"].items() if files and re.fullmatch(r"[0-9]+(\.[0-9]+)*", v)]
    return sorted(final, key=version_key)


def pin(version: str) -> None:
    pyproject = Path("pyproject.toml")
    text = pyproject.read_text()
    text = re.sub(r'^version = "[0-9.]+"', f'version = "{version}"', text, flags=re.M)
    text = re.sub(r'"heki==[0-9.]+"', f'"heki=={version}"', text)
    pyproject.write_text(text)
    readme = Path("README.md")
    readme.write_text(re.sub(r"rev: v[0-9.]+", f"rev: v{version}", readme.read_text()))
    subprocess.run(["git", "add", "pyproject.toml", "README.md"], check=True)
    subprocess.run(["git", "commit", "-m", f"heki {version}"], check=True)
    # An annotated tag: `git push --follow-tags` pushes only annotated tags.
    subprocess.run(["git", "tag", "-a", f"v{version}", "-m", f"heki {version}"], check=True)


def main() -> None:
    pinned = version_key(current())
    for version in releases():
        if version_key(version) > pinned:
            pin(version)
            print(f"pinned heki {version}")


if __name__ == "__main__":
    main()
