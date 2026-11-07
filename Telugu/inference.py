from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.upstream import add_mode_parser, run_upstream
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthesize the Telugu assignment sentences.")
    add_mode_parser(parser)
    parser.add_argument("--text-file", type=Path, required=True)
    args = parser.parse_args()
    run_upstream(args.config, "inference", args.text_file)