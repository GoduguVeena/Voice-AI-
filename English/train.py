import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


if __name__ == "__main__":
    from common.upstream import add_mode_parser, run_upstream

    parser = argparse.ArgumentParser(description="Train the English FastSpeech 2 model.")
    add_mode_parser(parser)
    run_upstream(parser.parse_args().config, "train")