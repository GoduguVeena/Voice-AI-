from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_array(path: Path, values: np.ndarray, title: str, ylabel: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 3))
    plt.plot(values, linewidth=1)
    plt.title(title)
    plt.xlabel("Frame")
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot FastSpeech 2 variance-adaptor predictions saved as .npy files.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--label", default="sample")
    args = parser.parse_args()
    for name, title, ylabel in (("duration", "Duration prediction", "Frames"), ("pitch", "Pitch prediction (F0)", "Hz"), ("energy", "Energy prediction", "Amplitude")):
        source = args.input / f"{name}.npy"
        if not source.exists():
            raise FileNotFoundError(source)
        plot_array(args.output / f"{name}.png", np.load(source), f"{args.label}: {title}", ylabel)


if __name__ == "__main__":
    main()