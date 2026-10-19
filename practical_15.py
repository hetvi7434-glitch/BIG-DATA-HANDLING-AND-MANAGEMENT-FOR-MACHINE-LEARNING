import os
import sys
import warnings

# ----------------- FIX FOR PYTHON 3.13 & TENSORFLOW CRASH -----------------
# Completely disable TensorFlow backend to prevent the Python 3.13 ops.py crash
os.environ["USE_TF"] = "0"
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TORCH"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

warnings.filterwarnings("ignore")
# --------------------------------------------------------------------------

from transformers import pipeline, logging as hf_logging

# Suppress verbose info/warning logs during model loading
hf_logging.set_verbosity_error()

# Step 1: Initialize pretrained Hugging Face Sentiment Analysis Pipeline
print("Loading Hugging Face sentiment-analysis pipeline...")
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    framework="pt"  # Explicitly force PyTorch backend
)

# Step 2: Define sample product & service customer reviews
reviews = [
    "PySpark makes distributed computing on massive datasets incredibly fast and enjoyable!",
    "The dataset had too many corrupted records and missing values, causing the training to crash.",
    "Transformers and Large Language Models are revolutionizing artificial intelligence.",
    "The data engineering pipeline was slow and poorly documented."
]

# Step 3: Run inference and display results
print("\n--- PREDICTED SENTIMENT SCORES ---")
for i, review in enumerate(reviews, 1):
    result = classifier(review)[0]
    label = result['label']
    score = result['score'] * 100
    print(f"Review {i}: '{review}'")
    print(f"Result   : [{label}] with {score:.2f}% confidence\n")
