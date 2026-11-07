from __future__ import annotations

import argparse
import os
import shlex
import subprocess
from pathlib import Path

import yaml


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def require_upstream() -> Path:
    root = os.environ.get("FASTSPEECH2_ROOT")
    if not root:
        raise SystemExit("Set FASTSPEECH2_ROOT to a local checkout of ming024/FastSpeech2 before running this command.")
    path = Path(root).resolve()
    if not (path / "preprocess.py").exists() or not (path / "train.py").exists():
        raise SystemExit(f"FASTSPEECH2_ROOT does not look like the reference implementation: {path}")
    return path


def run_upstream(config_path: Path, mode: str, text_file: Path | None = None) -> None:
    config = load_config(config_path)
    root = require_upstream()
    command = config["upstream"][mode]
    values = dict(config["paths"])
    if text_file is not None:
        values["text_file"] = str(text_file.resolve())
    rendered = [str(part).format(**values) for part in command]
    print("Running:", shlex.join(rendered))
    subprocess.run(rendered, cwd=root, check=True)


def add_mode_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", type=Path, required=True)