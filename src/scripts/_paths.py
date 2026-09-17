"""Shared path helpers for scripts (any nesting under src/scripts/)."""

from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "requirements.txt").is_file() and (parent / "src" / "configs").is_dir():
            return parent
    raise RuntimeError("project root not found from " + str(here))


def src_dir(root: Path | None = None) -> Path:
    return (root or project_root()) / "src"
