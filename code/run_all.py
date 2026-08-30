"""Run all extracted listing scripts in lexical order.

Stops on first failure and prints the failing script path and exit code.
This script runs many scripts and may take time, but should complete within
reasonable bounds. Individual scripts have shorter timeouts.
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def main() -> None:
    """Run all listing scripts in order.

    Raises:
        SystemExit: With a non-zero code if any script fails or times out.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    root = Path(__file__).resolve().parent
    scripts = sorted(p for p in root.glob("**/listing-*.py") if p.is_file())

    env = dict(os.environ)
    env["CODE_RUN_ALL"] = "1"
    # Avoid interactive windows blocking execution.
    env.setdefault("MPLBACKEND", "Agg")
    project_root = root.parent
    existing_pythonpath = env.get("PYTHONPATH", "")
    extra_paths = os.pathsep.join(
        [str(project_root / "src"), str(project_root / "chapters")]
    )
    env["PYTHONPATH"] = (
        extra_paths + (os.pathsep + existing_pythonpath if existing_pythonpath else "")
    )
    # Per-script timeout (default 20s as per audit harness)
    timeout_s = float(env.get("CODE_RUN_ALL_TIMEOUT", "20"))
    max_scripts_env = env.get("CODE_RUN_ALL_MAX_SCRIPTS")
    if max_scripts_env:
        try:
            max_scripts = int(max_scripts_env)
        except ValueError:
            max_scripts = None
        else:
            if max_scripts <= 0:
                max_scripts = None
        if max_scripts is not None:
            scripts = scripts[:max_scripts]
            logger.info("Limiting run to first %d scripts (CODE_RUN_ALL_MAX_SCRIPTS)", max_scripts)

    logger.info(f"Running {len(scripts)} scripts with {timeout_s}s timeout per script")

    for script in scripts:
        logger.info(f"RUNNING: {script.relative_to(root)}")
        try:
            proc = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(script.parent),
                env=env,
                timeout=timeout_s,
                capture_output=True,
                text=True,
            )
        except subprocess.TimeoutExpired:
            logger.error(f"TIMEOUT: {script} (>{timeout_s:.0f}s)")
            raise SystemExit(124)
        if proc.returncode != 0:
            logger.error(f"FAILED: {script} (exit {proc.returncode})")
            if proc.stderr:
                logger.error(f"Error output: {proc.stderr}")
            raise SystemExit(proc.returncode)

    logger.info("All scripts completed successfully")
    return None


if __name__ == "__main__":
    main()
