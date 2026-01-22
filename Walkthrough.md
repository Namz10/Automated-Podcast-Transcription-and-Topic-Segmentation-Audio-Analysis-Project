# Project Walkthrough: Automated Podcast Analyzer

This document summarizes the technical execution of the **Automated Podcast Transcription and Topic Segmentation** project.

## Milestone 1: Data Acquisition & AI Pipeline
- **Audio Engineering**: We implemented a robust preprocessing pipeline that performs **Spectral Gating** for noise removal and **RMS Normalization** for volume consistency. This ensures the highest possible transcription accuracy.
- **ASR Implementation**: Integrated **OpenAI Whisper (Base)** for speech-to-text. The pipeline handles chunked audio processing to prevent memory overflows and features incremental saving for reliability.

## Milestone 2: Topic Segmentation & Analysis
- **Algorithm Comparison**: We implemented two segmentation methods:
    1. **Baseline**: Cosine similarity between consecutive sentences.
    2. **Embedding-Based (SBERT)**: A more advanced approach using **Sentence-BERT** to detect semantic drifts. The embedding-based method was selected for the final product due to its superior "human-like" boundary detection.
- **Knowledge Extraction**: For every segment, we automatically extract **top keywords** using RAKE and generate a **1-2 sentence executive summary** using the T5 model.

## Milestone 3: Web Interface & Indexing
- **The Dashboard**: A full-stack application providing a "Table of Contents" for podcasts.
- **Navigation**: Features **Segment Jumping**, allowing users to skip directly to topics of interest without manual scrubbing.
- **Discovery**: Implemented a **Global Search** engine that indexes across segments, keywords, and summaries.

---

### Technical Highlights
- **Design**: Modern Dark Mode with Glassmorphism and Framer Motion animations.
- **Performance**: Sub-second search indexing and smooth scrolling navigation.
- **Scale**: The system is modular and can process any MP3/WAV podcast source.

---
*Created as the final project walkthrough for the industry submission.*
