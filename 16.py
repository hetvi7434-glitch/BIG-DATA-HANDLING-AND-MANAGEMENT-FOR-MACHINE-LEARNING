import os
import warnings

# Suppress background TensorFlow/Keras and Hugging Face logging warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore")

from transformers import pipeline, logging as hf_logging
hf_logging.set_verbosity_error()

# Step 1: Initialize pretrained Hugging Face Summarization Pipeline
print("Loading Hugging Face summarization pipeline...")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", framework="pt")

# Step 2: Define an extended article on Big Data & AI
article = """
Big Data has fundamentally changed the landscape of artificial intelligence and machine learning.
Traditionally, organizations relied on relational databases that scaled vertically by adding more compute
resources to a single server. However, with the exponential growth of web traffic, social media feeds,
and IoT sensors, modern data platforms transitioned to distributed frameworks like Apache Spark.
Apache Spark utilizes in-memory computing and Directed Acyclic Graphs to process petabytes of information
across commodity hardware clusters. Furthermore, the advent of Self-Attention Transformers and Large Language
Models has created an insatiable demand for high-quality, web-scale corpora, solidifying big data engineering
as the core foundational backbone of modern Generative AI.
"""

s

# Step 3: Generate summary with controlled length
summary = summarizer(article, max_length=60, min_length=25, do_sample=False)

print("\n--- ORIGINAL ARTICLE LENGTH ---")
print(f"Word Count: {len(article.split())} words")

print("\n--- GENERATED CONDENSED SUMMARY ---")
print(summary[0]['summary_text'])
print(f"Summary Word Count: {len(summary[0]['summary_text'].split())} words")


