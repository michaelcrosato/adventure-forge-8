from __future__ import annotations

import sys
import unittest
from io import StringIO

from adventure_forge.paths import repo_root


def run_units() -> str:
    root = repo_root()
    src = str(root / "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    loader = unittest.TestLoader()
    suite = loader.discover(str(root / "tests"), pattern="test_*.py")
    buf = StringIO()
    result = unittest.TextTestRunner(stream=buf, verbosity=2).run(suite)
    output = buf.getvalue()
    if not result.wasSuccessful():
        raise AssertionError("unit tests failed\n" + output)
    return output
