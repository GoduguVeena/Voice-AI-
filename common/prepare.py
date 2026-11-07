from __future__ import annotations

import argparse
import json
from pathlib import Path

from .data import read_csv, split_by_speaker, write_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Create disjoint FastSpeech 2 train/validation manifests.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--validation-ratio", type=float, default=1 / 6)
    parser.add_argument("--train-hours", type=float, default=5)
    parser.add_argument("--validation-hours", type=float, default=1)
    args = parser.parse_args()
    rows = read_csv(args.input)
    train, validation = split_by_speaker(rows, args.validation_ratio, args.seed)
    write_manifest(args.output / "train.txt", train)
    write_manifest(args.output / "validation.txt", validation)
    summary = {
        "input": str(args.input.resolve()),
        "seed": args.seed,
        "train_hours_target": args.train_hours,
        "validation_hours_target": args.validation_hours,
        "train_utterances": len(train),
        "validation_utterances": len(validation),
        "train_audio": sorted(str(row.audio) for row in train),
        "validation_audio": sorted(str(row.audio) for row in validation),
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "preparation.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    overlap = set(summary["train_audio"]) & set(summary["validation_audio"])
    if overlap:
        raise AssertionError(f"Train/validation overlap detected: {sorted(overlap)}")
    print(json.dumps({key: value for key, value in summary.items() if not key.endswith("audio")}, indent=2))


if __name__ == "__main__":
    main()