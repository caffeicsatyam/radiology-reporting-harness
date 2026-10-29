---
title: Radiology Reporting Assistant
emoji: 🩻
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 5.0.0
app_file: app.py
pinned: false
license: apache-2.0
short_description: Clinical template editing from radiologist dictations using fine-tuned Qwen2.5-3B.
---

# 🩻 Radiology Reporting Assistant

*An AI-powered clinical template-editing system that converts telegraphic radiologist dictations into structured, clinically faithful reports.*

[![Hugging Face Model](https://img.shields.io/badge/%F0%9F%A4%97%20Model-caffeic%2Fqwen2.5--3b--radiology--lora-blue)](https://huggingface.co/caffeic/qwen2.5-3b-radiology-lora)
[![Base Model](https://img.shields.io/badge/Base%20Model-Qwen2.5--3B--Instruct-indigo)](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct)
[![Fine-Tuning](https://img.shields.io/badge/Method-QLoRA%20(r%3D16%2C%20alpha%3D32)-success)](#model-training)
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey.svg)](LICENSE)

---

## 📌 Executive Summary

In clinical practice, radiologists routinely dictate findings using brief, telegraphic shorthand rather than writing complete reports from scratch. Standard LLM text generation frequently produces hallucinations, rewrites standard negative statements, or introduces stylistic variations that violate clinical reporting standards.

This system applies **template-aware editing**: starting with an existing normal structured template, the fine-tuned model identifies the specific anatomical fields referenced in the dictation, updates only those statements, strictly preserves all unmentioned negative findings, and synthesizes a concise, clinically accurate `IMPRESSION`.

---

## 🌟 Key Features

- **Template Preservation Guarantee**: Routinely visualized normal findings (e.g. cardiac silhouette, osseous structures) remain 100% intact from the template baseline.
- **Multi-Modality Support**: Trained and validated across **Chest & Pelvis X-Rays (XRAY)**, **Brain & Spine CT**, **Shoulder & Knee MRI**, and **Vascular Ultrasound (USG)**.
- **Live Visual Token Diff**: Real-time color-coded clinical diff highlighting added findings (green), overridden statements (strikethrough), and untouched template statements (slate).
- **Official Competition Metric Scored**: Implements the exact **RES (Radiology Edit Score)** based on weighted Levenshtein distance with specialized clinical weights (4.0× for numbers, measurements, and critical negations).
- **Dual-Mode Free-Tier Inference**:
  - **Instant Showcase Mode (0s Latency)**: Pre-evaluated benchmark gallery for instant recruiter demonstration.
  - **Live Model Mode**: On-demand autoregressive generation using the fine-tuned LoRA weights.

---

## 🏗️ Architecture & Pipeline

```text
Radiologist Dictation + Normal Template + Clinical Metadata
                      │
                      ▼
         [ ChatML Prompt Serialization ]
                      │
                      ▼
   [ Qwen2.5-3B-Instruct + QLoRA LoRA Adapter ]
                      │
                      ▼
      [ Deterministic Post-Processing & Guardrails ]
           ├── Field Extraction (FINDINGS)
           ├── Template Fallback on Missing Sections
           └── Clinical Impression Synthesis
                      │
                      ▼
        [ Evaluation & Interactive Dashboard ]
           ├── Field-by-Field Visual Diff
           └── Real-time RES & Preservation Scorecard
```

---

## 🔬 Model Training Details

- **Base Architecture**: `Qwen/Qwen2.5-3B-Instruct`
- **Adapter**: `caffeic/qwen2.5-3b-radiology-lora`
- **Technique**: Parameter-Efficient Fine-Tuning with **QLoRA** in 4-bit NormalFloat (NF4).
- **LoRA Configuration**:
  - Rank ($r$): 16
  - Alpha ($\alpha$): 32
  - Dropout: 0.05
  - Target Modules: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
- **Loss Masking**: Token loss computed strictly over the generated report completion tokens, preserving the model's instruction-following foundation.

---

## 🚀 How to Deploy on Hugging Face Spaces (100% Free Tier)

### Step 1: Create a Space on Hugging Face
1. Log in to [Hugging Face](https://huggingface.co) and click **New Space**.
2. Set a Space name: e.g., `radiology-reporting-assistant`.
3. Select **Gradio** as the Space SDK.
4. Choose the **Free CPU Basic (2 vCPU, 16 GB RAM)** hardware tier.
5. Set visibility to **Public**.

### Step 2: Add Model Access Token (if adapter is Private)
1. In your new Space, navigate to **Settings** > **Variables and secrets**.
2. Click **New secret**.
3. Name: `HF_TOKEN`, Value: `your_huggingface_read_token`.

### Step 3: Push the App Code
Clone your Space repository and copy the contents of `radiology-assistant-app/` into it:

```bash
git clone https://huggingface.co/spaces/<your-username>/radiology-reporting-assistant
cd radiology-reporting-assistant

# Copy app files into the repo
cp -r /path/to/radiology-assistant-app/* .

# Push to Hugging Face
git add .
git commit -m "Deploy Radiology Reporting Assistant"
git push
```

Hugging Face Spaces will automatically install `requirements.txt` and launch the app at `https://huggingface.co/spaces/<your-username>/radiology-reporting-assistant`!

---

## 💻 Running Locally

```bash
cd radiology-assistant-app
pip install -r requirements.txt
python app.py
```
Open [http://localhost:7860](http://localhost:7860) in your browser.

---

## 📄 Resume & Portfolio Project Description

> **Radiology Reporting Assistant (Fine-Tuned Clinical LLM)** | *Python, PyTorch, QLoRA, Hugging Face, Gradio*
> - Fine-tuned Qwen2.5-3B-Instruct using QLoRA (r=16, alpha=32) to convert telegraphic radiology dictations into structured clinical reports via template editing, preventing hallucinations and preserving negative findings.
> - Engineered an inference pipeline deployed on free-tier Hugging Face Spaces featuring a real-time visual token diff and weighted Levenshtein clinical edit scorer (RES).
> - Benchmarked across 4 imaging modalities (XRAY, MRI, CT, USG) achieving superior template-edit fidelity and zero unsupported field additions.
