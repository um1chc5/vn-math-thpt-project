# Tests

Mirror whatever layout `src/scripts/` currently uses (flat or by role).

```bash
python3 -m pytest src/tests -q
```

`conftest.py` (if present) may put script dirs on `sys.path` so tests import the CLI modules without packaging.
