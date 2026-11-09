# src/models · Experiments track

Claim-detection experiments (proposal §6.5).

**Status:** not started.

1. Baselines: majority class; TF-IDF + logistic regression.
2. Fine-tuned Arabic models: AraBERT, CAMeLBERT, MARBERT.
3. LLMs: zero-shot and few-shot.
4. Cross-lingual transfer from ViClaim (needs the ViClaim transcripts; check access).
5. Effect of transcription: automatic vs corrected text on the same segments (D006).
6. Leave-one-topic-out (needs at least 2 complete topics, D008).

Every run is defined by a config in `experiments/` and reported with its commit hash and seed. The metric and label formulation depend on D002.
