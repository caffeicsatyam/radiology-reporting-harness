Overview
A radiologist often begins with short, telegraphic dictation rather than a finished report. Your task is to convert that dictation into a complete structured report by editing a supplied normal template.

For every case, test.csv provides exactly eight input columns: case_id, modality, body_part, study_description, patient_age_band, patient_sex, template_content, and dictation. Candidates generate one report for each case_id. Return FINDINGS and IMPRESSION only.

Core reporting rule
Treat the template as the starting report, not merely as an example.

Route every dictated finding to the matching FINDINGS field.
Replace or modify the corresponding normal statement when the dictation describes an abnormality.
Preserve template statements for routinely visualized regions that were not mentioned in the dictation.
Update the IMPRESSION so it accurately summarizes the important abnormal findings.
Do not add findings unsupported by dictation or template_content. Use modality, body_part, study_description, patient_age_band, and patient_sex only as context; these columns do not supply additional findings.
Preserve the supplied template wording and report order whenever possible.
When the provided template contains an OTHER FINDINGS: field, use it for relevant findings that do not belong in another labelled field. Leave it empty when no such finding applies.
FINDINGS and IMPRESSION
FINDINGS contains the detailed observations organized by anatomy or template field. IMPRESSION is the concise clinical summary: it should report the major abnormal findings and may include a possible diagnosis when that diagnosis is supported by the FINDINGS. It should not repeat every normal statement or introduce new information.

The expected report deliberately remains close to the supplied template. Avoid rewriting unchanged normal statements simply for style. Semantically reasonable paraphrases may still receive an edit penalty because the leaderboard measures template-edit fidelity.

Data notice: This benchmark uses de-identified radiology text. case_id is random; exact ages, patient identifiers, accession numbers and study UIDs are not provided. All dates have been removed from the text. The data must not be used for clinical decisions.

Input columns
Column	Meaning
case_id	Random UUID used to match test cases to submission rows.
modality	Imaging modality: XRAY, MRI, CT, or USG.
body_part	Anatomical region examined.
study_description	Name or description of the ordered examination.
patient_age_band	Five-year age band, such as 45-49; ages 90 and above are 90+.
patient_sex	Patient sex recorded as male or female.
template_content	Normal FINDINGS fields and IMPRESSION that must be edited.
dictation	Transcribed radiologist dictation containing the findings to incorporate.
train.csv contains these eight input columns plus the target report. test.csv contains exactly the eight input columns above and does not contain report. sample_submission.csv contains exactly case_id and report.

No clinical history, prior study or image is provided. Do not infer unsupported facts.

Worked chest radiograph example
Dictation

mild right basilar opacity, small right pleural effusion
Normal template

FINDINGS:
SUPPORT DEVICES: None.
CARDIOMEDIASTINAL SILHOUETTE: Within normal size limits.
LUNGS: No focal airspace opacity or pulmonary edema.
PLEURA: No pleural effusion or pneumothorax.
OSSEOUS STRUCTURES: No acute osseous abnormality identified on these views.

IMPRESSION:
No acute cardiopulmonary abnormality.
Expected report

FINDINGS:
SUPPORT DEVICES: None.
CARDIOMEDIASTINAL SILHOUETTE: Within normal size limits.
LUNGS: Mild right basilar airspace opacity. No pulmonary edema.
PLEURA: Small right pleural effusion. No pneumothorax.
OSSEOUS STRUCTURES: No acute osseous abnormality identified on these views.

IMPRESSION:
Mild right basilar airspace opacity and small right pleural effusion.
The lung and pleural statements changed because those abnormalities were dictated. The support devices, cardiomediastinal and osseous fields remained normal because nothing in the input required changing them. The opacity must not be placed under PLEURA, and the effusion must not be placed under LUNGS.

Practical starting approaches
There are no restrictions on the model family or implementation method. Reasonable starting points include:

Prompt engineering: give a capable language model modality, body_part, study_description, patient_age_band, patient_sex, template_content, dictation, and explicit field-preservation rules. Ask it to return only the completed report.
Structured generation: extract findings into a schema, route them to template fields, then render the final report deterministically.
Synthetic-data alignment: generate paired dictation/template/report examples and fine-tune or post-train a smaller model to perform template editing.
Hybrid or agentic pipeline: combine extraction, validation and generation stages, optionally using a hosted model API.
Whatever method you choose, verify negation, laterality, measurements, field routing, unsupported additions and preservation of untouched normal fields.

Submission and hiring review
Upload the completed submission.csv through Kaggle's File Upload option. You may generate the reports outside Kaggle, including with external model APIs. Each report must contain only FINDINGS and IMPRESSION.

A complete hiring-challenge entry must also include the automated pipeline as a Kaggle Notebook:

Create or upload a Kaggle Notebook containing the complete pipeline code. The notebook does not need to execute on Kaggle.
Save a notebook version and share the private notebook with Natoe AI Dev (natoeaidev).
Paste the notebook URL into the Submission Description of your final CSV submission.
A leaderboard submission without an accessible pipeline notebook is incomplete. Do not include API keys; use environment-variable or secret placeholders. The submitted code must reproduce the uploaded CSV without manual case-level editing.

The Kaggle leaderboard uses only RES - Radiology Edit Score, where lower is better. RES measures minimal template-edit fidelity, not full semantic or clinical equivalence. The hiring team may separately review clinical faithfulness, unsupported content, omissions, routing, reproducibility, and system design; this review does not change the Kaggle leaderboard score.