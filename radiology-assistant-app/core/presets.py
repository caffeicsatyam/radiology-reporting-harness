"""Curated real-world clinical benchmark cases across XRAY, CT, MRI, and USG.
Used for instantaneous showcase demonstrations and recruiter evaluation.
"""

CLINICAL_PRESETS = {
    "cxr_worked": {
        "title": "Chest X-Ray: Basilar Opacity & Effusion",
        "case_id": "worked-example-chest-01",
        "modality": "XRAY",
        "body_part": "Chest",
        "study_description": "XR CHEST 2V AP/LATERAL",
        "patient_age_band": "60-64",
        "patient_sex": "male",
        "template_content": "FINDINGS:\nSUPPORT DEVICES: None.\nCARDIOMEDIASTINAL SILHOUETTE: Within normal size limits.\nLUNGS: No focal airspace opacity or pulmonary edema.\nPLEURA: No pleural effusion or pneumothorax.\nOSSEOUS STRUCTURES: No acute osseous abnormality identified on these views.\n\nIMPRESSION:\nNo acute cardiopulmonary abnormality.",
        "dictation": "mild right basilar opacity, small right pleural effusion",
        "target_report": "FINDINGS:\nSUPPORT DEVICES: None.\nCARDIOMEDIASTINAL SILHOUETTE: Within normal size limits.\nLUNGS: Mild right basilar airspace opacity. No pulmonary edema.\nPLEURA: Small right pleural effusion. No pneumothorax.\nOSSEOUS STRUCTURES: No acute osseous abnormality identified on these views.\n\nIMPRESSION:\nMild right basilar airspace opacity and small right pleural effusion."
    },
    "hip_oa": {
        "title": "Pelvis & Hip X-Ray: Osteoarthritis",
        "case_id": "2c88d015-b359-4e2c-9c62-61a23ce9d1c3",
        "modality": "XRAY",
        "body_part": "Hip",
        "study_description": "XR RT HIP 2V",
        "patient_age_band": "90+",
        "patient_sex": "female",
        "template_content": "FINDINGS:\nBONES: No acute fracture or focal osseous lesion.\nJOINTS: No dislocation. The joint spaces are normal.\nSOFT TISSUES: The soft tissues are unremarkable.\n\nIMPRESSION:\nNo acute osseous abnormality.",
        "dictation": "No acute fracture or dislocation. Mild right hip osteoarthrosis with mild superolateral joint space narrowing and small marginal acetabular and femoral head osteophytes. Mild degenerative changes of the bilateral sacroiliac joints Mild degenerative changes of the visualized lower lumbar spine. Pelvic ring is intact.",
        "target_report": "FINDINGS:\nBONES: No acute fracture. Mild degenerative changes of the visualized lower lumbar spine are present. The pelvic ring is intact.\n\nJOINTS: Mild right hip osteoarthrosis is present with mild superolateral joint space narrowing and small marginal acetabular and femoral head osteophytes. Mild degenerative changes of the bilateral sacroiliac joints are noted. There is no dislocation.\n\nSOFT TISSUES: The soft tissues are unremarkable.\n\nIMPRESSION:\n1. Mild osteoarthrosis of the right hip.\n2. Mild degenerative changes of the bilateral sacroiliac joints and visualized lower lumbar spine.\n3. No acute fracture or dislocation."
    },
    "brain_ct": {
        "title": "Brain CT: Cerebral Volume Loss & Ischemia",
        "case_id": "1d9cea61-1c0c-4d18-89a0-72a0328d6216",
        "modality": "CT",
        "body_part": "Head",
        "study_description": "CT BRAIN W/O-S",
        "patient_age_band": "75-79",
        "patient_sex": "female",
        "template_content": "FINDINGS:\nBRAIN: Brain parenchyma appears normal in attenuation and morphology. No midline shift or intra extra-axial collection. Gray-white matter differentiation is preserved.\nVENTRICLES: The ventricles are normal in size and configuration.\nORBITS: The globes and retrobulbar soft tissues are symmetric and unremarkable.\nSINUSES AND MASTOIDS: The paranasal sinuses and mastoid air cells are clear.\nSOFT TISSUES: No significant facial or scalp soft tissue swelling evident. \nBONES: No acute skull fracture or lesion.\n\nIMPRESSION:\nNo acute intracranial abnormality.",
        "dictation": "Age-appropriate cerebral volume loss. \nmild  There are periventricular white matter low density changes, compatible with chronic small vessel ischemic changes. \nchronic infarction/encephalomalacia at right pisterior parietal lobe\nmoderate  There are periventricular white matter low density changes, compatible with chronic small vessel ischemic changes. \natheroscelrotsis of intracranial arteries",
        "target_report": "FINDINGS:\nBRAIN: There is age-appropriate cerebral volume loss. There is chronic infarction/encephalomalacia at the right posterior parietal lobe. There are moderate periventricular white matter low density changes, compatible with chronic small vessel ischemic changes. The remaining brain parenchyma appears normal in attenuation and morphology. No midline shift or intra extra-axial collection. No acute infarction.\nVENTRICLES: The ventricles are normal in size and configuration.\nORBITS: The globes and retrobulbar soft tissues are symmetric and unremarkable.\nSINUSES AND MASTOIDS: The paranasal sinuses and mastoid air cells are clear.\nSOFT TISSUES: No significant facial or scalp soft tissue swelling evident.\nBONES: No acute skull fracture or lesion.\nThere is atherosclerosis of the intracranial arteries.\n\nIMPRESSION:\n1. Chronic right posterior parietal lobe infarction with associated encephalomalacia.\n2. Moderate chronic small vessel ischemic changes.\n3. Age-appropriate cerebral volume loss.\n4. Atherosclerosis of the intracranial arteries.\n5. No acute intracranial hemorrhage or mass effect."
    },
    "shoulder_mri": {
        "title": "Shoulder MRI: Tendinosis & Impingement",
        "case_id": "2066ed76-9f41-4ac8-95f6-74ec1e4cef8a",
        "modality": "MRI",
        "body_part": "Shoulder",
        "study_description": "MRI RT SHOULDER WO",
        "patient_age_band": "45-49",
        "patient_sex": "male",
        "template_content": "FINDINGS:\nTENDONS:\nSUPRASPINATUS: The tendon is intact with normal signal intensity.\nINFRASPINATUS: The tendon is intact with normal signal intensity.\nSUBSCAPULARIS: The tendon is intact with normal signal intensity.\nTERES MINOR: The tendon is intact with normal signal intensity.\nBICEPS BRACHII, LONG HEAD: The tendon is normally located within the bicipital groove and is intact.\nLIGAMENTS:\nGLENOHUMERAL: The superior, middle, and inferior glenohumeral ligaments are intact.\nJOINTS:\nGLENOHUMERAL JOINT: No joint effusion. The articular cartilage is preserved. The labrum is intact.\nACROMIOCLAVICULAR JOINT: No significant degenerative changes or osteophytes.\nBONES: No acute fracture, dislocation, or aggressive osseous lesion. Normal bone marrow signal.\nMUSCLES: The rotator cuff muscles demonstrate normal bulk and signal intensity without evidence of atrophy or edema.\n\nIMPRESSION:\nNormal MRI of the [left/right] shoulder.",
        "dictation": "MRI RIGHT SHOULDER WITHOUT CONTRAST Right shoulder pain for 4 months. Multiplanar, multisequence MRI of the right shoulder was performed without intravenous contrast. None. Rotator cuff shows moderate supraspinatus tendinosis with low-grade bursal-sided/intrasubstance partial-thickness tearing at the distal insertion/footprint. Mild insertional tendinosis of the subscapularis tendon without a discrete tear. Infraspinatus and teres minor tendons are intact. No full-thickness rotator cuff tear or tendon retraction. Muscles shows rotator cuff musculature demonstrates preserved bulk without fatty atrophy or muscle edema. Long head of biceps tendon is intact and normally positioned within the bicipital groove. Moderate fluid distends the biceps tendon sheath, consistent with tenosynovitis. Labrum shows mild degenerative fraying of the superior labrum without a displaced tear on this non-arthrographic examination. Glenohumeral joint shows moderate glenohumeral joint effusion with distention of the subscapularis recess. Mild diffuse chondral thinning without advanced glenohumeral osteoarthritis. Acromioclavicular joint shows moderate acromioclavicular osteoarthrosis with joint space narrowing, capsular hypertrophy, and inferiorly directed osteophytes producing mild narrowing of the supraspinatus outlet. Acromion is type II acromion. Bursa shows moderate subacromial-subdeltoid bursitis. Bones shows small subcortical cystic changes with mild reactive marrow edema in the greater tuberosity at the supraspinatus insertion. No acute fracture or aggressive osseous lesion. Capsule/Rotator interval shows mild thickening and edema within the rotator interval and inferior glenohumeral capsule, which may be seen with adhesive capsulitis. Correlate clinically. Moderate supraspinatus tendinosis with low-grade bursal-sided/intrasubstance partial-thickness insertional tear. No full-thickness rotator cuff tear. Mild insertional subscapularis tendinosis without a discrete tear. Moderate long head of the biceps tenosynovitis. Moderate glenohumeral joint effusion with distention of the subscapularis recess. Moderate subacromial-subdeltoid bursitis. Moderate acromioclavicular osteoarthrosis with inferior osteophytic spurring resulting in mild subacromial outlet narrowing. Reactive cystic changes and mild marrow edema in the greater tuberosity at the supraspinatus insertion. Mild rotator interval and inferior capsular thickening/edema, which may reflect adhesive capsulitis in the appropriate clinical setting.",
        "target_report": "FINDINGS:\nTENDONS:\nSUPRASPINATUS: There is moderate supraspinatus tendinosis with low-grade bursal-sided/intrasubstance partial-thickness tearing at the distal insertion/footprint.\nINFRASPINATUS: The infraspinatus tendon is intact.\nSUBSCAPULARIS: There is mild insertional tendinosis of the subscapularis tendon without a discrete tear.\nTERES MINOR: The teres minor tendon is intact.\nBICEPS BRACHII, LONG HEAD: Moderate fluid distends the biceps tendon sheath, consistent with tenosynovitis. The tendon is intact and normally positioned within the bicipital groove.\n\nLIGAMENTS:\nGLENOHUMERAL: There is mild thickening and edema within the rotator interval and inferior glenohumeral capsule, which may be seen with adhesive capsulitis. The superior and middle glenohumeral ligaments are intact.\n\nJOINTS:\nGLENOHUMERAL JOINT: There is a moderate glenohumeral joint effusion with distention of the subscapularis recess. There is mild diffuse chondral thinning without advanced glenohumeral osteoarthritis. There is mild degenerative fraying of the superior labrum without a displaced tear on this non-arthrographic examination. The remainder of the labrum is intact.\nACROMIOCLAVICULAR JOINT: There is moderate acromioclavicular osteoarthrosis with joint space narrowing, capsular hypertrophy, and inferiorly directed osteophytes producing mild narrowing of the supraspinatus outlet.\n\nBONES: There are small subcortical cystic changes with mild reactive marrow edema in the greater tuberosity at the supraspinatus insertion. There is a Type II acromion. No acute fracture or aggressive osseous lesion.\n\nMUSCLES: The rotator cuff musculature demonstrates preserved bulk without fatty atrophy or muscle edema.\n\nThere is moderate subacromial-subdeltoid bursitis. No full-thickness rotator cuff tear or tendon retraction.\n\nIMPRESSION:\nModerate supraspinatus tendinosis with low-grade bursal-sided/intrasubstance partial-thickness insertional tear. No full-thickness rotator cuff tear.\nMild insertional subscapularis tendinosis without a discrete tear.\nModerate long head of the biceps tenosynovitis.\nModerate glenohumeral joint effusion with distention of the subscapularis recess. Moderate subacromial-subdeltoid bursitis.\nModerate acromioclavicular osteoarthrosis with inferior osteophytic spurring resulting in mild subacromial outlet narrowing.\nReactive cystic changes and mild marrow edema in the greater tuberosity at the supraspinatus insertion.\nMild rotator interval and inferior capsular thickening/edema, which may reflect adhesive capsulitis in the appropriate clinical setting."
    },
    "cxr_norm": {
        "title": "Chest X-Ray: Mild Thoracic Spondylosis",
        "case_id": "218fc4a5-c7e9-44a7-9aea-54e56bb22663",
        "modality": "XRAY",
        "body_part": "Chest",
        "study_description": "XR CXR 2V",
        "patient_age_band": "65-69",
        "patient_sex": "male",
        "template_content": "FINDINGS:\nLUNGS: Lungs are clear. No focal air-space consolidation.\nPLEURAL SPACES: No pleural effusion or pneumothorax.\nHEART: Cardiac silhouette is within normal size limits.\nMEDIASTINUM/HILA: Cardiomediastinal silhouette is within normal limits. No mediastinal widening or hilar enlargement.\nDIAPHRAGM: Diaphragms are unremarkable. No subdiaphragmatic free air.\nBONES: No acute osseous abnormality identified on this examination.\nSOFT TISSUES: No acute soft tissue abnormality identified on the provided images.\n\nIMPRESSION:\nNo acute abnormality.",
        "dictation": "no effusuon, infiltrates\nmild thoracic spondylosis",
        "target_report": "FINDINGS:\nLUNGS: Lungs are clear. No focal air-space consolidation.\nPLEURAL SPACES: No pleural effusion or pneumothorax.\nHEART: Cardiac silhouette is within normal size limits.\nMEDIASTINUM/HILA: Cardiomediastinal silhouette is within normal limits. No mediastinal widening or hilar enlargement.\nDIAPHRAGM: Diaphragms are unremarkable. No subdiaphragmatic free air.\nBONES: Mild thoracic spondylosis is present. No acute osseous abnormality identified on this examination.\nSOFT TISSUES: No acute soft tissue abnormality identified on the provided images.\n\nIMPRESSION:\n1. Mild thoracic spondylosis.\n2. No acute cardiopulmonary abnormality."
    },
    "vascular_usg": {
        "title": "Vascular Ultrasound: Venous Evaluation",
        "case_id": "22e8239e-dc46-4372-987a-97d9548c51de",
        "modality": "USG",
        "body_part": "Unknown",
        "study_description": "BLEV",
        "patient_age_band": "65-69",
        "patient_sex": "female",
        "template_content": "FINDINGS:\nDEEP VEINS: The common femoral, superficial femoral, and popliteal veins are echolucent and compressible.  There is normal color Doppler flow throughout. The visualized calf veins are also patent.\nSUPERFICIAL VEINS: The visualized great and short saphenous veins are patent with competent sapheno-femoral and sphenopopliteal junction. No incompetent perforators.\nSOFT TISSUES: No popliteal fossa cyst or other abnormalities.\n\nIMPRESSION:\nNo deep venous thrombosis in the [_laterality_] lower extremity.",
        "dictation": "Bilateral lower extremity pain for 3 weeks. None. Gray-scale, color Doppler, and spectral Doppler ultrasound evaluation of the deep venous systems of both lower extremities was performed. The common femoral, femoral, popliteal, posterior tibial, and peroneal veins are patent and fully compressible bilaterally, with preserved spontaneous flow and augmentation. No intraluminal thrombus is identified. A 3.1 x 0.9 x 0.9 cm avascular cystic structure is present in the right popliteal fossa, compatible with a popliteal (Baker) cyst. No sonographic evidence of deep venous thrombosis in either lower extremity. Right popliteal fossa cyst measuring 3.1 cm, consistent with a Baker cyst. Clinical management of the right popliteal cyst as indicated. Thank you for your referral.",
        "target_report": "FINDINGS:\nDEEP VEINS: The common femoral, femoral, popliteal, posterior tibial, and peroneal veins are patent and fully compressible bilaterally, with preserved spontaneous flow and augmentation. No intraluminal thrombus is identified.\n\nSUPERFICIAL VEINS: The visualized great and short saphenous veins are patent with competent sapheno-femoral and sphenopopliteal junction. No incompetent perforators.\n\nSOFT TISSUES: A 3.1 x 0.9 x 0.9 cm avascular cystic structure is present in the right popliteal fossa, compatible with a popliteal (Baker) cyst. No other abnormalities are seen in the left popliteal fossa.\n\nIMPRESSION:\n1. No sonographic evidence of deep venous thrombosis in either lower extremity.\n2. Right popliteal fossa cyst measuring 3.1 cm, consistent with a Baker cyst."
    }
}

def get_preset_choices():
    return [(v["title"], k) for k, v in CLINICAL_PRESETS.items()]

def get_preset_by_key(key: str) -> dict:
    return CLINICAL_PRESETS.get(key, list(CLINICAL_PRESETS.values())[0])
