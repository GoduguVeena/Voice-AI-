from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.upstream import add_mode_parser, run_upstream
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train the Telugu FastSpeech 2 model.")
    add_mode_parser(parser)
    run_upstream(parser.parse_args().config, "train")