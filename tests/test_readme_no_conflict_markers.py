"""Repo hygiene: README must not ship unresolved git conflict markers (MRB #10)."""
from __future__ import annotations

from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_MARKERS = ("<<<<<<<", ">>>>>>>", "=======")


def test_readme_has_no_git_conflict_markers():
    text = (_ROOT / "README.md").read_text(encoding="utf-8")
    for m in _MARKERS:
        assert m not in text, f"README.md still contains conflict marker {m!r}"


def test_tracked_markdown_has_no_conflict_markers():
    bad: list[str] = []
    for path in _ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if any(m in text for m in ("<<<<<<<", ">>>>>>>")):
            bad.append(str(path.relative_to(_ROOT)))
    assert bad == [], f"conflict markers in: {bad}"
