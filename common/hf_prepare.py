from __future__ import annotations

import argparse
import csv
import hashlib
import io
import sys
from pathlib import Path


def _speaker(record: dict) -> str:
    for key in ("speaker", "speaker_id", "client_id", "speaker_name"):
        value = record.get(key)
        if value is not None:
            return str(value)
    return "unknown"


def _text(record: dict) -> str:
    for key in ("text", "transcription", "transcript", "sentence"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return " ".join(value.split())
    raise ValueError(f"Could not find a transcript field in columns: {sorted(record)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream a bounded train/validation subset from a Hugging Face audio dataset.")
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--split", default="train")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--train-hours", type=float, default=5)
    parser.add_argument("--validation-hours", type=float, default=1)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    try:
        from datasets import Audio, load_dataset
    except ImportError as exc:
        raise SystemExit(
            f"Missing package 'datasets' for interpreter {sys.executable}. "
            "Install with: python -m pip install datasets soundfile"
        ) from exc

    dataset = load_dataset(args.dataset, split=args.split, streaming=True, token=True)
    dataset = dataset.cast_column("audio", Audio(decode=False))
    train_seconds = args.train_hours * 3600
    validation_seconds = args.validation_hours * 3600
    durations = {"train": 0.0, "validation": 0.0}
    rows = {"train": [], "validation": []}
    output_audio = args.output / "wavs"
    output_audio.mkdir(parents=True, exist_ok=True)

    try:
        import soundfile as sf
    except ImportError as exc:
        raise SystemExit(
            f"Missing package 'soundfile' for interpreter {sys.executable}. "
            "Install with: python -m pip install datasets soundfile"
        ) from exc

    for index, record in enumerate(dataset):
        audio = record.get("audio")
        if not isinstance(audio, dict):
            raise ValueError("The dataset must contain an audio column")
        source = io.BytesIO(audio["bytes"]) if audio.get("bytes") else audio.get("path")
        if source is None:
            raise ValueError("The audio record contains neither embedded bytes nor a path")
        import soundfile as sf

        samples, sample_rate = sf.read(source, dtype="float32")
        sample_rate = int(sample_rate)
        duration = len(samples) / sample_rate
        digest = hashlib.sha1(f"{args.seed}:{index}".encode()).hexdigest()[:16]
        split = "validation" if int(digest, 16) % 6 == 0 else "train"
        if durations[split] + duration > (validation_seconds if split == "validation" else train_seconds):
            alternate = "train" if split == "validation" else "validation"
            if durations[alternate] + duration <= (validation_seconds if alternate == "validation" else train_seconds):
                split = alternate
            else:
                if all(durations[name] >= limit for name, limit in (("train", train_seconds), ("validation", validation_seconds))):
                    break
                continue
        filename = f"{split}_{len(rows[split]):06d}.wav"
        path = output_audio / filename
        sf.write(path, samples, sample_rate)
        rows[split].append((Path("wavs") / filename, _text(record), _speaker(record), duration))
        durations[split] += duration
        if (index + 1) % 25 == 0:
            print(
                f"Processed {index + 1} records | "
                f"train={durations['train'] / 3600:.2f}h | "
                f"validation={durations['validation'] / 3600:.2f}h",
                flush=True,
            )

    if not rows["train"] or not rows["validation"]:
        raise RuntimeError(f"Could not create both splits: {durations}")
    args.output.mkdir(parents=True, exist_ok=True)
    for split, split_rows in rows.items():
        with (args.output / f"{split}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["audio", "text", "speaker", "duration"])
            writer.writerows(split_rows)
    print(f"Prepared {args.dataset}: train={durations['train'] / 3600:.2f}h, validation={durations['validation'] / 3600:.2f}h")


if __name__ == "__main__":
    main()