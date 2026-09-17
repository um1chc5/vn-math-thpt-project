"""Put script packages on sys.path for every test under src/tests/."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
_GENERATE = _SCRIPTS / "generate"

for p in (_SCRIPTS, _GENERATE):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)
