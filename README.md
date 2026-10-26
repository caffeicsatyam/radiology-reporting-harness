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

## Notes

- The solution is intentionally conservative and template-aware.
- It avoids unsupported clinical claims and preserves normal findings.
- The focus is on faithful minimal edits rather than rewriting the report from scratch.
- The approach is designed to be reliable, structured, and easy to validate.
