# FastSpeech 2 for English and Telugu

This repository contains the assignment implementation for two independent FastSpeech 2 pipelines. The language folders intentionally share only the data and orchestration utilities; each language has its own preprocessing, training, inference, and configuration entry points.

## Layout

```text
English/                 English pipeline entry points
Telugu/                  Telugu pipeline entry points
common/                  dataset, manifest, and variance-analysis utilities
configs/                 language-specific experiment settings
Results/                 generated plots and audio (created by the scripts)
Report/Technical_Report.md
```

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

The model implementation is the upstream FastSpeech 2 reference implementation. Set `FASTSPEECH2_ROOT` to a local checkout of `ming024/FastSpeech2` before training. This keeps the assignment code reproducible and avoids copying a large third-party model into the submission.

## Data preparation

Prepare a CSV with columns `audio,text` (paths may be absolute or relative to the CSV) and run one command per language:

```bash
python English/preprocess.py --input data/svarah.csv --output data/English --seed 42
python Telugu/preprocess.py --input data/indictts_telugu.csv --output data/Telugu --seed 42
```

For the supplied Hugging Face datasets, accept the Svarah access conditions in your browser first, set `HF_TOKEN` in the local terminal, and stream only the assignment subset:

```bash
python English/download_prepare.py --dataset ai4bharat/Svarah --split test --output data/English
python Telugu/download_prepare.py --dataset SPRINGLab/IndicTTS_Telugu --split train --output data/Telugu
```

The downloader uses the token from the environment through the Hugging Face client; no token is written to a file or command argument.

The splitter uses a seeded, speaker-aware split when a `speaker` column is available and rejects duplicate audio paths across train and validation. `--train-hours 5 --validation-hours 1` are the assignment defaults; the script selects complete utterances up to those budgets.

## Training and synthesis

```bash
python English/train.py --config configs/english.yaml
python Telugu/train.py --config configs/telugu.yaml
python English/inference.py --config configs/english.yaml --text-file English/test_sentences.txt
python Telugu/inference.py --config configs/telugu.yaml --text-file Telugu/test_sentences.txt
```

The training wrapper delegates to the checked-out upstream implementation and records the exact command in the output directory. Inference writes one WAV per assignment sentence and the duration, pitch, and energy arrays required for the variance-adaptor plots.

## Reproducibility

The dataset archives and trained checkpoints are intentionally not committed. Place them in the paths declared in the YAML files, or provide an accessible download URL in the report. See [Report/Technical_Report.md](Report/Technical_Report.md) for the preprocessing decisions, experiment table, and result-analysis checklist.