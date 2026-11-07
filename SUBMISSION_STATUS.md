# Submission Status

## Verified in this repository

- English and Telugu pipeline entry points
- Hugging Face dataset preparation code
- Telugu train and validation manifests generated locally
- Reproducible configuration files and assignment test sentences
- Variance-adaptor plotting utility
- Technical report structure and reproducibility instructions
- Git branch hygiene and large-file exclusions

## Pending experiment artifacts

- English dataset preparation
- FastSpeech 2 upstream checkout and language-specific preprocessing
- 5-hour training and 1-hour validation runs for both languages
- Trained checkpoints
- Generated WAV files for the required test sentences
- Duration, pitch, energy, and loss plots
- Final measured results and subjective audio analysis

The pending items are intentionally marked rather than fabricated. To complete them, set `FASTSPEECH2_ROOT`, prepare the English dataset, run both training jobs, and add the resulting small plots, logs, and test samples to `Results/`. The large training datasets, caches, and checkpoints remain excluded by `.gitignore`.