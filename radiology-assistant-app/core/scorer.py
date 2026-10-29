"""Official Radiology Edit Score (RES) metric implementation and clinical fidelity checks.
Computes weighted Levenshtein distance, field-level preservation, and impression fidelity.
"""

import re
import unicodedata

UNITS = {
    "millimeters": "mm",
    "millimeter": "mm",
    "centimeters": "cm",
    "centimeter": "cm",
}

FUNCTION_WORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "at", "for", "with", "without",
    "from", "by", "as", "is", "are", "was", "were", "be", "been", "being", "this", "that",
    "these", "those", "there", "it", "its", "than", "into", "over", "under", "within",
}

CRITICAL_WORDS = {
    "no", "not", "without", "negative", "absent", "right", "left", "bilateral",
    "mild", "moderate", "severe", "marked", "minimal", "trace", "small", "large",
    "acute", "chronic", "subacute", "new", "stable", "fracture", "dislocation",
    "tear", "rupture", "effusion", "pneumothorax", "pneumonia", "mass", "lesion",
    "stenosis", "occlusion", "thrombosis", "edema", "swelling",
}

UNIT_WORDS = {"mm", "cm"}

NUM_RE = re.compile(r"[+-]?\d+(?:\.\d+)?")
LABEL_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9 /&(),.\-]{0,59}?)\s*:\s*(.*)$")


def normalize_for_score(text: str) -> str:
    """Normalize text for metric evaluation: lowercase, unit standardizing, number masking."""
    if text is None:
        return ""
    text = unicodedata.normalize("NFKC", str(text)).lower()

    for src, dst in UNITS.items():
        text = re.sub(rf"\b{re.escape(src)}\b", dst, text)

    text = re.sub(r"(?m)^\s*(?:\d+[\.\)]|[-*•])\s+", "", text)
    text = re.sub(r"(?<=[a-z])-(?=[a-z])", "", text)
    text = re.sub(r"(?<=[a-z])(?=\d)", " ", text)
    text = re.sub(r"(?<=\d)(?=[a-z])", " ", text)

    protected = []

    def protect(m):
        protected.append(m.group(0))
        return f" zznum{len(protected) - 1}zz "

    text = re.sub(r"(?<![\w.])[+-]?\d+(?:\.\d+)?", protect, text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"zznum(\d+)zz", lambda m: protected[int(m.group(1))], text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize_score(text: str) -> list[str]:
    """Tokenize normalized text."""
    t = normalize_for_score(text)
    return t.split() if t else []


def token_weight(token: str) -> float:
    """Assign clinical importance weights to tokens."""
    if NUM_RE.fullmatch(token):
        return 4.0
    if token in UNIT_WORDS or token in CRITICAL_WORDS:
        return 4.0
    if token in FUNCTION_WORDS:
        return 0.25
    return 2.0


def weighted_levenshtein(ref: list[str], pred: list[str]) -> float:
    """Compute weighted Levenshtein distance normalized to [0.0, 1.0]."""
    n, m = len(ref), len(pred)
    if n == 0 and m == 0:
        return 0.0
    rw = [token_weight(t) for t in ref]
    pw = [token_weight(t) for t in pred]

    prev = [0.0] * (m + 1)
    for j in range(1, m + 1):
        prev[j] = prev[j - 1] + pw[j - 1]
    for i in range(1, n + 1):
        cur = [prev[0] + rw[i - 1]] + [0.0] * m
        for j in range(1, m + 1):
            sub = prev[j - 1] + (0.0 if ref[i - 1] == pred[j - 1] else max(rw[i - 1], pw[j - 1]))
            cur[j] = min(prev[j] + rw[i - 1], cur[j - 1] + pw[j - 1], sub)
        prev = cur

    denom = max(sum(rw), sum(pw))
    return min(prev[m] / denom, 1.0) if denom else 0.0


def word_edit_score(reference: str, prediction: str) -> float:
    """Calculate edit score between two strings."""
    return weighted_levenshtein(tokenize_score(reference), tokenize_score(prediction))


def extract_report_sections(report: str) -> tuple[str, str]:
    """Split report into FINDINGS and IMPRESSION sections."""
    report = str(report or "")
    f = re.search(r"FINDINGS\s*:\s*(.*?)(?=\n\s*IMPRESSION\s*:|\Z)", report, flags=re.I | re.S)
    i = re.search(r"IMPRESSION\s*:\s*(.*)\Z", report, flags=re.I | re.S)
    findings = f.group(1).strip() if f else ""
    impression = i.group(1).strip() if i else ""
    return findings, impression


def parse_labeled_fields(text: str) -> dict[str, str]:
    """Parse colon-delimited anatomical fields (e.g. 'LUNGS: ...', 'PLEURA: ...')."""
    fields, label, buf = {}, None, []

    def flush():
        if label is not None:
            content = " ".join(buf).strip()
            if content:
                fields[label] = content

    for line in (text or "").splitlines():
        m = LABEL_RE.match(line)
        if m and len(m.group(1).split()) <= 6:
            flush()
            label = re.sub(r"\s+", " ", m.group(1)).strip().upper()
            buf = [m.group(2).strip()] if m.group(2).strip() else []
        elif label is not None and line.strip():
            buf.append(line.strip())
    flush()
    return fields


def calculate_findings_score(template: str, reference: str, prediction: str) -> float:
    """Calculate weighted findings edit score, emphasizing modified sections over unchanged ones."""
    ref_f, _ = extract_report_sections(reference)
    pred_f, _ = extract_report_sections(prediction)
    tpl_f, _ = extract_report_sections(template)

    ref_fields = parse_labeled_fields(ref_f)
    pred_fields = parse_labeled_fields(pred_f)
    tpl_fields = parse_labeled_fields(tpl_f)

    if not ref_fields:
        return word_edit_score(ref_f, pred_f)

    num = den = 0.0
    for field, ref_text in ref_fields.items():
        changed = normalize_for_score(tpl_fields.get(field, "")) != normalize_for_score(ref_text)
        w = 3.0 if changed else 1.0
        num += w * word_edit_score(ref_text, pred_fields.get(field, ""))
        den += w

    for field in tpl_fields:
        if field not in ref_fields:
            num += word_edit_score("", pred_fields.get(field, ""))
            den += 1.0

    return min(num / den, 1.0) if den else word_edit_score(ref_f, pred_f)


def calculate_impression_score(reference: str, prediction: str) -> float:
    """Compute impression edit score."""
    _, ref_i = extract_report_sections(reference)
    _, pred_i = extract_report_sections(prediction)
    return word_edit_score(ref_i, pred_i)


def score_report(template: str, reference: str, prediction: str) -> dict[str, float]:
    """Compute complete RES score breakdown."""
    findings_score = calculate_findings_score(template, reference, prediction)
    impression_score = calculate_impression_score(reference, prediction)
    res = 0.65 * findings_score + 0.35 * impression_score
    return {
        "findings_score": round(findings_score, 4),
        "impression_score": round(impression_score, 4),
        "res": round(res, 4),
    }


def analyze_template_fidelity(template: str, report: str) -> dict:
    """Analyze how faithfully the report preserved the normal template fields."""
    tpl_f, tpl_i = extract_report_sections(template)
    rep_f, rep_i = extract_report_sections(report)

    tpl_fields = parse_labeled_fields(tpl_f)
    rep_fields = parse_labeled_fields(rep_f)

    preserved = []
    modified = []
    invented = []
    omitted = []

    for field, tpl_val in tpl_fields.items():
        if field in rep_fields:
            rep_val = rep_fields[field]
            if normalize_for_score(tpl_val) == normalize_for_score(rep_val):
                preserved.append(field)
            else:
                modified.append(field)
        else:
            omitted.append(field)

    for field in rep_fields:
        if field not in tpl_fields:
            invented.append(field)

    total_tpl_fields = len(tpl_fields) or 1
    preservation_pct = round((len(preserved) / total_tpl_fields) * 100, 1)

    return {
        "total_fields": len(tpl_fields),
        "preserved_fields": preserved,
        "modified_fields": modified,
        "invented_fields": invented,
        "omitted_fields": omitted,
        "preservation_rate_pct": preservation_pct,
        "has_impression": bool(rep_i.strip()),
    }
