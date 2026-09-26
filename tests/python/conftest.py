# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Make the build scripts importable as modules.

The scripts under scripts/ are run as files, not installed as a package,
and several import their siblings by bare name, so the directory goes on
sys.path once for the whole suite.
"""

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
