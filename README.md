# DREAMT_FE Project: Setup & Workflow Guide

> **Purpose:**  
> Step‑by‑step instructions for setting up, preprocessing, feature engineering, and running the DREAMT_FE pipeline locally.

---

## 📑 Table of Contents

- [DREAMT\_FE Project: Setup \& Workflow Guide](#dreamt_fe-project-setup--workflow-guide)
  - [📑 Table of Contents](#-table-of-contents)
  - [Step 1: Environment Setup](#step1-environment-setup)
  - [Step 2: Feature Engineering](#step2-feature-engineering)
    - [Option A: Re‑run Preprocessing](#option-a-rerun-preprocessing)
    - [Option B: Use Existing Outputs](#option-b-use-existing-outputs)
  - [Step 3: Calculate Quality Score](#step3-calculate-quality-score)
    - [Option A: Re‑compute Scores](#option-a-recompute-scores)
    - [Option B: Use Existing Scores](#option-b-use-existing-scores)
  - [Step 4: Run Main Pipeline](#step4-run-main-pipeline)
  - [Optional: `main_cv.py`](#optional-main_cvpy)
  - [Helper Modules Overview](#helper-modules-overview)
    - [Datasets.py](#datasetspy)
    - [Models.py](#modelspy)
    - [Utils.py](#utilspy)

---

## Step 1: Environment Setup

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/mmacrides/DREAMT_FE.git
   cd DREAMT_FE
   ```

2. **Create Conda Environment**  
   The provided `environment_mac.yml` has Linux‑incompatible packages removed for M1/M2 Macs:
   ```bash
   conda env create --file environment_mac.yml
   conda activate dreamt
   ```

3. **Skip Pre‑Aggregation**  
   We’re starting from pre‑aggregated E4 files, so you can skip the “read_raw_e4.py” step.

   **Background on `read_raw_e4.py`:**  
   > Reads raw Empatica E4 signals (HR, TEMP, ACC, BVP, EDA, IBI), aligns them with sleep stages & reports (e.g. AHI), and outputs CSVs into  
   > `dataset_sample/E4_aggregate/…`  
   >  
   > Since we already have those aggregated files, this step is **skipped**.

---

## Step 2: Feature Engineering

### Option A: Re‑run Preprocessing

1. **Wipe Old Outputs**  
   ```bash
   rm dataset_sample/E4_aggregate/*.csv
   rm dataset_sample/features_df/*.csv
   ```

2. **Inject PhysioNet Data**  
   - Download the zipped file from https://physionet.org/content/dreamt/2.0.0/. Unzip the file.  
   - Copy each `data_64Hz/SID_whole_df.csv` into `dataset_sample/E4_aggregate/`.

3. **Run Feature Engineering**  
   ```bash
   python3 feature_engineering.py
   ```
   - **Output:**  
     `dataset_sample/features_df/SID_domain_features_df.csv`

---

### Option B: Use Existing Outputs

- **Skip** `feature_engineering.py`  
- We already have:  
  `dataset_sample/features_df/SID_domain_features_df.csv`

---

## Step 3: Calculate Quality Score

### Option A: Re‑compute Scores

1. **Remove Old Scores**  
   ```bash
   rm results/quality_scores_per_subject.csv
   ```

2. **Run Scoring Script**  
   ```bash
   python calculate_quality_score.py
   ```
   - **Output:**  
     `results/quality_scores_per_subject.csv`

---

### Option B: Use Existing Scores

- **Skip** `calculate_quality_score.py`  
- We already have:  
  `results/quality_scores_per_subject.csv`

---

## Step 4: Run Main Pipeline

```bash
python main.py
```

> **What It Does:**  
> Loads data → Cleans & splits → Builds, trains & tests model → Evaluates performance  
>
> (Identical to `experiments.ipynb`, but in script form.)

---

## Optional: `main_cv.py`

```bash
python main_cv.py
```

> Same end‑to‑end flow as `main.py`, **plus** cross‑validation.

---

## Helper Modules Overview

### Datasets.py  
> **Role:** Loads & cleans feature‑engineered data, resamples, and splits into `train`/`val`/`test`.  
> Used by: `main.py`, `main_cv.py`.

### Models.py  
> **Role:** Defines model architectures, trains/tests them, and returns metrics & confusion matrices.  
> Used by: `main.py`, `main_cv.py`.

### Utils.py  
> **Role:** Shared helper functions for loading, cleaning, splitting, model building, training, testing, and evaluation.  
> Used by: `Datasets.py`, `Models.py`, `main.py`, `main_cv.py`.  

---
