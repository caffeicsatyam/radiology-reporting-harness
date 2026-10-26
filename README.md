<p align="center">
  <h1>Radiology Reporting Assistant</h1>
  <br>
  <em>AI-powered template editing for turning brief radiology dictations into structured, clinically consistent reports.</em>
  <br><br>
  <a title="Python" target="_blank" href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat-square"></a>
  <a title="Pandas" target="_blank" href="https://pandas.pydata.org/"><img src="https://img.shields.io/badge/pandas-2.x-orange.svg?style=flat-square"></a>
  <a title="LLM" target="_blank" href="https://platform.openai.com/"><img src="https://img.shields.io/badge/LLM-Ready-4F46E5.svg?style=flat-square"></a>
  <a title="Template Editing" target="_blank" href="https://en.wikipedia.org/wiki/Template_method_pattern"><img src="https://img.shields.io/badge/Template-Editing-green.svg?style=flat-square"></a>
</p>

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Key Features](#key-features)
- [Workflow](#workflow)
- [Example](#example)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Model Fine-Tuning](#model-fine-tuning)
- [Notes](#notes)

---

## Overview

This project is a solution for transforming short radiology dictations into complete structured reports by editing a normal template instead of generating the report from scratch.

The goal is to keep the output clinically consistent, minimally invasive, and faithful to the original template while incorporating the findings described by the dictation.

---

## How It Works

The system starts from an existing report template and modifies only the parts that need to change.

```text
Dictation + template
        |
        v
Extract findings
        |
        v
Map findings to the correct section
        |
        v
Update only affected template statements
        |
        v
Generate concise impression
        |
        v
Validate and output final report
```

This makes the pipeline more reliable than freeform generation because it preserves normal statements and only changes the relevant findings.

---

## Key Features

- Template-aware report generation
- Anatomy-specific finding routing
- Preservation of unchanged normal statements
- Minimal edit strategy for high template fidelity
- Concise impression generation from the most important findings
- Guardrails against unsupported additions
- Works across varied exam types and body regions

---

## Workflow

### 1. Load the input context

The pipeline reads the clinical context from the data, including:

- modality
- body part
- study description
- patient age band
- patient sex
- report template
- dictation

### 2. Extract findings

The model identifies which findings are relevant, including:

- normal vs. abnormal findings
- laterality and anatomical location
- severity or degree when present
- fields affected in the template

### 3. Edit the template

Only the relevant findings sections are updated. Everything else remains intact.

### 4. Generate the impression

The impression condenses the major abnormal findings into a short clinically useful summary.

### 5. Validate output quality

The final result is checked for:

- unsupported additions
- incorrect field routing
- negation mistakes
- unnecessary rewriting of unchanged statements

---

## Example

### Input dictation

```text
mild right basilar opacity, small right pleural effusion
```

### Resulting report

```text
FINDINGS:
SUPPORT DEVICES: None.
CARDIOMEDIASTINAL SILHOUETTE: Within normal size limits.
LUNGS: Mild right basilar airspace opacity. No pulmonary edema.
PLEURA: Small right pleural effusion. No pneumothorax.
OSSEOUS STRUCTURES: No acute osseous abnormality identified on these views.

IMPRESSION:
Mild right basilar airspace opacity and small right pleural effusion.
```

This example reflects the project’s core design: edit the relevant parts of the template while leaving the rest untouched.

---

## Project Structure

```text
.
├── README.md
├── sample_submission.csv
├── test.csv
├── train.csv
├── Radiology_reporting_harness.ipynb
├── radiology-reporting-harness/
│   ├── sample_submission.csv
│   ├── test.csv
│   └── train.csv
├── .gitignore
└── .env.example
```

---

## Setup

### Prerequisites

- Python 3.10+
- pip
- optional LLM access if using a model-based pipeline

### Install

```bash
git clone https://github.com/caffeicsatyam/radiology-reporting-harness.git
cd radiology-reporting-harness
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install pandas numpy python-dotenv
```

### Environment variables

```bash
export OPENAI_API_KEY=your_key_here
```

---

## Usage

A typical flow looks like this:

```python
import pandas as pd

# Load the input dataset
df = pd.read_csv("test.csv")

# For each row:
# 1. read the template content
# 2. extract findings from the dictation
# 3. route them to the correct report sections
# 4. update the template
# 5. generate the impression
# 6. save the final output
```

The central idea is simple:

> Start from a valid medical template and make only the necessary edits.

---

## Model Fine-Tuning

The notebook fine-tunes `Qwen/Qwen2.5-3B-Instruct` for template-aware radiology report editing using supervised fine-tuning (SFT) with 4-bit QLoRA. Run [Radiology_reporting_harness.ipynb](./Radiology_reporting_harness.ipynb) in a GPU-enabled notebook environment such as Google Colab.

### Training data

The notebook loads separate training and validation JSONL files (`train_sft_train.jsonl` and `train_sft_val.jsonl`). Each record contains:

```json
{
  "input": {
    "template_content": "...",
    "dictation": "...",
    "modality": "...",
    "body_part": "...",
    "study_description": "...",
    "patient_age_band": "...",
    "patient_sex": "..."
  },
  "output": {
    "report": "..."
  }
}
```

Each example is formatted with the Qwen chat template: the input provides the clinical context, template, and dictation, while `output.report` is the target final report. The prompt instructs the model to preserve the template, avoid invented findings, and return `FINDINGS` and `IMPRESSION` sections.

### Fine-tuning configuration

- **Quantization:** 4-bit NF4 with double quantization
- **LoRA:** rank 16, alpha 32, dropout 0.05; applied to attention and MLP projection layers
- **Training:** 3 epochs, maximum sequence length 2,048, batch size 1 with 8 gradient-accumulation steps
- **Optimization:** paged 8-bit AdamW, learning rate `2e-4`, constant scheduler
- **Evaluation and checkpoints:** evaluate and save every 50 steps, retain up to 2 checkpoints, and load the checkpoint with the best evaluation loss

The notebook trains with TRL's `SFTTrainer` and saves the trained LoRA adapter and tokenizer to `/content/qwen2.5-3b-radiology-lora`. This is an adapter, not a full copy of the base model; load it alongside the same Qwen base model for inference.

---

## Notes

- The solution is intentionally conservative and template-aware.
- It avoids unsupported clinical claims and preserves normal findings.
- The focus is on faithful minimal edits rather than rewriting the report from scratch.
- The approach is designed to be reliable, structured, and easy to validate.
