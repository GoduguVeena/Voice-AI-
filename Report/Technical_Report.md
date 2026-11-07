# FastSpeech 2 Technical Report

## 1. Objective

This project trains independent FastSpeech 2 models for English (Svarah) and Telugu (IndicTTS Telugu). The upstream reference implementation is used for the acoustic model, while this repository supplies reproducible dataset preparation, language entry points, experiment configuration, synthesis inputs, and variance-adaptor analysis.

## 2. Dataset and preprocessing

| Language | Dataset | Training audio | Validation audio | Seed |
|---|---|---:|---:|---:|
| English | Svarah | 5 h target | 1 h target | 42 |
| Telugu | IndicTTS Telugu | 5 h target | 1 h target | 42 |

The input CSV contains `audio`, `text`, and optionally `speaker`. Relative audio paths are resolved relative to the CSV. Speaker-disjoint splitting is used when speaker labels exist; otherwise a seeded utterance split is used. Empty transcripts are removed, whitespace is normalized, and the generated manifests are checked for train/validation overlap.

## 3. Model and language changes

FastSpeech 2 consists of the phoneme/text encoder, variance adaptor for duration, pitch, and energy, length regulator, decoder, and mel-spectrogram-to-waveform vocoder. English uses the reference tokenizer and phoneme inventory. Telugu requires a Telugu-capable text frontend and a Unicode vocabulary; the same acoustic architecture and separate checkpoint are retained so the two languages do not share incompatible embeddings.

## 4. Training and validation analysis

Record the final configuration, hardware, step count, best checkpoint, and the training/validation curves in the table below after the runs complete.

| Language | Best step | Train loss | Validation loss | Overfitting / instability |
|---|---:|---:|---:|---|
| English | TODO | TODO | TODO | TODO |
| Telugu | TODO | TODO | TODO | TODO |

## 5. Test-sentence observations

For every English and Telugu sentence, include the generated WAV and duration, pitch (F0), and energy plots. Discuss pronunciation of long words, punctuation and numbers, rhythm, pauses, and any Telugu grapheme or phoneme errors. Do not claim subjective quality or convergence until the corresponding files have been inspected.

## 6. Reproduction

```bash
pip install -r requirements.txt
python English/preprocess.py --input data/svarah.csv --output data/English --seed 42
python Telugu/preprocess.py --input data/indictts_telugu.csv --output data/Telugu --seed 42
python English/train.py --config configs/english.yaml
python Telugu/train.py --config configs/telugu.yaml
```

The upstream FastSpeech 2 checkout is selected with `FASTSPEECH2_ROOT`. Dataset archives, checkpoints, and generated audio are excluded from source control because of their size; provide a stable download link in the final README when publishing the trained artifacts.