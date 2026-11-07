from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Utterance:
    audio: Path
    text: str
    speaker: str = "unknown"
    duration: float = 0.0


def read_csv(path: Path) -> list[Utterance]:
    rows: list[Utterance] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"audio", "text"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} is missing columns: {', '.join(sorted(missing))}")
        for row in reader:
            audio = Path(row["audio"])
            if not audio.is_absolute():
                audio = path.parent / audio
            text = " ".join((row["text"] or "").split())
            if not text:
                continue
            rows.append(Utterance(audio.resolve(), text, row.get("speaker") or "unknown", float(row.get("duration") or 0)))
    if not rows:
        raise ValueError(f"No usable utterances found in {path}")
    return rows


def split_by_speaker(rows: Iterable[Utterance], validation_ratio: float, seed: int) -> tuple[list[Utterance], list[Utterance]]:
    rows = list(rows)
    if len({row.speaker for row in rows}) == 1:
        shuffled = rows[:]
        random.Random(seed).shuffle(shuffled)
        target = max(1, round(len(shuffled) * validation_ratio))
        return shuffled[target:], shuffled[:target]
    grouped: dict[str, list[Utterance]] = {}
    for row in rows:
        grouped.setdefault(row.speaker, []).append(row)
    speakers = list(grouped)
    random.Random(seed).shuffle(speakers)
    target = max(1, round(len(rows) * validation_ratio))
    validation: list[Utterance] = []
    for speaker in speakers:
        if len(validation) >= target:
            break
        validation.extend(grouped[speaker])
    validation_ids = {row.audio for row in validation}
    train = [row for row in rows if row.audio not in validation_ids]
    if not train or not validation:
        raise ValueError("The dataset is too small for a non-empty train/validation split")
    return train, validation


def write_manifest(path: Path, rows: Iterable[Utterance]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="|")
        for row in rows:
            writer.writerow([row.audio, row.text, row.speaker, f"{row.duration:.3f}"])