"""Inference pipeline for Radiology Reporting Assistant.
Handles model loading (with Peft LoRA adapter), tokenization, post-processing guardrails,
and dual-mode generation (Instant Benchmark Cache + On-demand Live Inference).
Optimized for lazy imports so showcase and diff features run even without torch installed locally.
"""

import os
import re
from .config import (
    BASE_MODEL_ID,
    ADAPTER_MODEL_ID,
    HF_TOKEN,
    MAX_NEW_TOKENS,
    RETRY_MAX_NEW_TOKENS,
    build_prompt_messages,
)
from .scorer import extract_report_sections
from .presets import CLINICAL_PRESETS

# Global model cache
_MODEL = None
_TOKENIZER = None
_EOS_IDS = None


def clean_report(text: str) -> str:
    """Normalize model output format to strict FINDINGS and IMPRESSION sections."""
    t = str(text or "").replace("<|im_end|>", "").strip()
    m = re.search(r"\bFINDINGS\s*:", t, flags=re.I)
    if m:
        t = t[m.start():]
    t = re.sub(r"^\s*FINDINGS\s*:", "FINDINGS:", t, flags=re.I)
    t = re.sub(r"\n\s*IMPRESSION\s*:", "\n\nIMPRESSION:", t, flags=re.I)
    return t.strip()


def finalize_report(raw_text: str, template: str) -> tuple[str, str]:
    """Apply safety guardrails preventing hallucinated sections and enforcing template fallbacks."""
    t = clean_report(raw_text)
    has_f = re.search(r"FINDINGS\s*:", t, flags=re.I)
    has_i = re.search(r"IMPRESSION\s*:", t, flags=re.I)
    _, tpl_impression = extract_report_sections(template)

    if not has_f:
        return clean_report(template), "fallback_template"
    if not has_i:
        return (t + "\n\nIMPRESSION:\n" + tpl_impression).strip(), "fallback_template_impression"
    return t, "ok"


def is_model_loaded() -> bool:
    """Check if model and tokenizer are already resident in memory."""
    return _MODEL is not None and _TOKENIZER is not None


def load_model_and_tokenizer(device: str = None):
    """Load the base model and QLoRA adapter into memory with CPU/GPU memory optimizations."""
    global _MODEL, _TOKENIZER, _EOS_IDS

    if is_model_loaded():
        return _MODEL, _TOKENIZER

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel
    except ImportError as e:
        raise ImportError(
            f"Required ML packages missing ({e}). Live model inference requires 'pip install torch transformers peft accelerate'."
        )

    token = HF_TOKEN or os.getenv("HF_TOKEN")

    print(f"[Loading Tokenizer] Base model: {BASE_MODEL_ID}...")
    tok = AutoTokenizer.from_pretrained(
        ADAPTER_MODEL_ID if token else BASE_MODEL_ID,
        token=token,
        trust_remote_code=True,
    )
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    tok.padding_side = "right"

    im_end_id = tok.convert_tokens_to_ids("<|im_end|>")
    eos_ids = sorted({i for i in [im_end_id, tok.eos_token_id, tok.pad_token_id] if i is not None})

    # Device selection
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"[Loading Model] Target device: {device.upper()}...")
    if device == "cuda":
        from transformers import BitsAndBytesConfig

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_ID,
            quantization_config=bnb_config,
            device_map="auto",
            dtype=torch.float16,
            token=token,
        )
    else:
        # Optimized CPU loading for free-tier Spaces (16 GB RAM)
        dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float32
        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_ID,
            dtype=dtype,
            device_map="cpu",
            low_cpu_mem_usage=True,
            token=token,
        )

    print(f"[Loading LoRA Adapter] {ADAPTER_MODEL_ID}...")
    model = PeftModel.from_pretrained(
        base_model,
        ADAPTER_MODEL_ID,
        token=token,
    )
    model.eval()
    model.config.use_cache = True

    _MODEL = model
    _TOKENIZER = tok
    _EOS_IDS = eos_ids
    print("[Model Ready] Inference pipeline initialized successfully!")
    return _MODEL, _TOKENIZER


def generate_report_live(
    modality: str,
    body_part: str,
    study_description: str,
    patient_age_band: str,
    patient_sex: str,
    template_content: str,
    dictation: str,
    max_tokens: int = MAX_NEW_TOKENS,
) -> tuple[str, str, dict]:
    """Execute live autoregressive generation using the fine-tuned LoRA model."""
    import torch

    model, tokenizer = load_model_and_tokenizer()

    messages = build_prompt_messages(
        modality,
        body_part,
        study_description,
        patient_age_band,
        patient_sex,
        template_content,
        dictation,
    )

    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    with torch.no_grad():
        enc = tokenizer(prompt, return_tensors="pt").to(model.device)
        prompt_len = enc["input_ids"].shape[1]

        out = model.generate(
            **enc,
            max_new_tokens=max_tokens,
            do_sample=False,
            num_beams=1,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=_EOS_IDS,
            use_cache=True,
        )

        new_ids = out[0, prompt_len:].tolist()
        finished = any(e in new_ids for e in _EOS_IDS)
        raw_text = tokenizer.decode(new_ids, skip_special_tokens=True).strip()

        # Retry with extended tokens if truncated
        if not finished and max_tokens < RETRY_MAX_NEW_TOKENS:
            out = model.generate(
                **enc,
                max_new_tokens=RETRY_MAX_NEW_TOKENS,
                do_sample=False,
                num_beams=1,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=_EOS_IDS,
                use_cache=True,
            )
            new_ids = out[0, prompt_len:].tolist()
            raw_text = tokenizer.decode(new_ids, skip_special_tokens=True).strip()

    final_text, status = finalize_report(raw_text, template_content)
    stats = {
        "prompt_tokens": prompt_len,
        "generated_tokens": len(new_ids),
        "status": status,
        "mode": "live_model",
    }
    return final_text, status, stats


def get_instant_preset_report(dictation: str, template_content: str) -> str | None:
    """Check if the current input matches a pre-computed clinical benchmark case."""
    d_clean = dictation.strip()
    t_clean = template_content.strip()

    for p in CLINICAL_PRESETS.values():
        if p["dictation"].strip() == d_clean or p["template_content"].strip() == t_clean:
            return p.get("target_report", "")
    return None
