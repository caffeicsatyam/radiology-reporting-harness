"""Configuration constants, system prompts, and model identifiers."""

import os
import math
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# Hugging Face Repository IDs
BASE_MODEL_ID = os.getenv("BASE_MODEL_ID", "Qwen/Qwen2.5-3B-Instruct")
ADAPTER_MODEL_ID = os.getenv("ADAPTER_MODEL_ID", "caffeic/qwen2.5-3b-radiology-lora")
HF_TOKEN = os.getenv("HF_TOKEN", None)

# Generation hyperparameters
MAX_NEW_TOKENS = 1280
RETRY_MAX_NEW_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.0  # Greedy decoding for clinical reproducibility
SEED = 42

# Official System Prompt used during QLoRA fine-tuning
SYSTEM_PROMPT = (
    "You are an expert radiology report editor. "
    "Generate the final report from the supplied template and dictation. "
    "Preserve template structure and wording where appropriate. "
    "Do not invent findings."
)

def clean_value(val):
    """Normalize input fields, handling NaN and None."""
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return ""
    return str(val).strip()

def build_user_prompt(
    modality: str,
    body_part: str,
    study_description: str,
    patient_age_band: str,
    patient_sex: str,
    template_content: str,
    dictation: str,
) -> str:
    """Build the exact input prompt used in fine-tuning and inference."""
    return "\n".join([
        "Generate the final radiology report from the supplied template and dictation.",
        "",
        "Requirements:",
        "- Incorporate all relevant dictated findings accurately.",
        "- Preserve the template's structure and wording where appropriate.",
        "- Do not invent findings.",
        "- Produce exactly two top-level sections:",
        "  FINDINGS:",
        "  IMPRESSION:",
        "- Return only the final report.",
        "",
        "MODALITY:", clean_value(modality), "",
        "BODY PART:", clean_value(body_part), "",
        "STUDY DESCRIPTION:", clean_value(study_description), "",
        "PATIENT AGE BAND:", clean_value(patient_age_band), "",
        "PATIENT SEX:", clean_value(patient_sex), "",
        "TEMPLATE:", clean_value(template_content), "",
        "DICTATION:", clean_value(dictation),
    ]).strip()

def build_prompt_messages(
    modality: str,
    body_part: str,
    study_description: str,
    patient_age_band: str,
    patient_sex: str,
    template_content: str,
    dictation: str,
) -> list[dict]:
    """Return standard ChatML messages list."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": build_user_prompt(
                modality,
                body_part,
                study_description,
                patient_age_band,
                patient_sex,
                template_content,
                dictation,
            ),
        },
    ]
