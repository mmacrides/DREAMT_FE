
# DREAMT_FE Project: Setup & Workflow Guide

## Purpose:
This guide provides detailed instructions and descriptions for setting up the DREAMT_FE pipeline, preprocessing physiological sleep data, engineering features, scoring data quality, and running the machine learning models—either with or without cross-validation.

## 📑 Table of Contents
- [DREAMT_FE Project: Setup & Workflow Guide](#dreamt_fe-project-setup--workflow-guide)
- [📑 Table of Contents](#-table-of-contents)
- [Step 1: Environment Setup](#step-1-environment-setup)
- [Step 2: Feature Engineering](#step-2-feature-engineering)
  - [Option A: Re-run Preprocessing](#option-a-re-run-preprocessing)
  - [Option B: Use Existing Outputs](#option-b-use-existing-outputs)
- [Step 3: Calculate Quality Score](#step-3-calculate-quality-score)
  - [Option A: Re-compute Scores](#option-a-re-compute-scores)
  - [Option B: Use Existing Scores](#option-b-use-existing-scores)
- [Step 4: Run Main Pipeline](#step-4-run-main-pipeline)
- [Optional: main_cv.py](#optional-main_cvpy)
- [Modules Overview](#modules-overview)

## Step 1: Environment Setup

### Clone the Repository
```bash
git clone https://github.com/mmacrides/DREAMT_FE.git
cd DREAMT_FE
```

### Create Conda Environment
Uses `environment_final.yml`, which is tailored for M1/M2 Macs:
```bash
conda env create --file environment_final.yml
conda activate dreamt
```

### Skip read_raw_e4.py
This step is not needed since we already have aggregated E4 data. 
PhysioNet only provides the aggregated E4 data as well so it is not possible to reproduce this step. 
`read_raw_e4.py` reads raw sensor data (HR, TEMP, ACC, BVP, EDA, IBI) and aligns them with sleep stages and clinical reports (like AHI). It outputs aligned CSVs to `dataset_sample/E4_aggregate/`.

## Step 2: Feature Engineering

### Option A: Re-run Preprocessing
Use this option if you're extending or reprocessing the E4 data.

#### Clear Old Outputs
```bash
rm dataset_sample/E4_aggregate/*.csv
rm dataset_sample/features_df/*.csv
```

#### Prepare PhysioNet Input
Download and unzip data from: https://physionet.org/content/dreamt/2.0.0/  
Copy each `SID_whole_df.csv` from `data_64Hz/` into `dataset_sample/E4_aggregate/`

#### Run Feature Engineering
```bash
python3 feature_engineering.py
```
**Output:**  
Generates `SID_domain_features_df.csv` in `dataset_sample/features_df/`  
Extracts domain-specific features (e.g., signal statistics, frequency domain features) from the time-aligned E4 data.

### Option B: Use Existing Outputs [preferred choice for faster reproducability]
If you're not modifying the input data or feature engineering process:

- Skip `feature_engineering.py`
- Use the pre-generated:
  - `dataset_sample/features_df/SID_domain_features_df.csv`

## Step 3: Calculate Quality Score

### Option A: Re-compute Scores
Use this if you’ve created an extension for the feature engineering file or changed how quality is computed.

#### Remove Old Scores
```bash
rm results/quality_scores_per_subject.csv
```

#### Run the Quality Scoring Script
```bash
python calculate_quality_score.py
```
**Output:**  
`results/quality_scores_per_subject.csv`  
Computes a participant-level score based on data completeness or signal quality metrics.

### Option B: Use Existing Scores if you have not altered the feature engineering phase [preferred choice for faster reproducability]
- Skip `calculate_quality_score.py`
- Use the pre-generated file in:  
  `results/quality_scores_per_subject.csv`

## Step 4: Run Main Pipeline

```bash
python main.py
```
**What it does:**  
Loads features and quality scores → Splits into train/val/test → Trains a classification model → Evaluates on test data  
Mirrors `experiments.ipynb` but runs as a clean pipeline script.

## Optional: main_cv.py

```bash
python main_cv.py
```
Same flow as `main.py`, but with k-fold cross-validation instead of a fixed train/test split. We did NOT use this file when reproducing our results and instead used `main.py`.

## Modules Overview

| Module                       | Description                                                                         |
|------------------------------|-------------------------------------------------------------------------------------|
| **read_raw_e4.py**           | Converts raw Empatica E4 signal files into aligned CSVs with sleep stage labels and AHI metrics. Skipped in the workflow since we don't have access to pre-aggregated input. |
| **feature_engineering.py**   | Reads aligned physiological data from `E4_aggregate/`, computes engineered features, and outputs them into `features_df/`. |
| **calculate_quality_score.py** | Analyzes engineered features to assign a quality score for each subject, stored in `results/`. |
| **main.py**                  | A module that runs the entire process of data loading, cleaning, splitting, model building, training, testing and evaluating. |
| **main_cv.py**               | Adds cross-validation on top of `main.py`, useful for assessing model robustness and generalization. |
| **Datasets.py**              | A module that read the feature engineered data in feature_df and perform data loading, cleaning, and resampling. The processed data is split into train, test, and validation set. |
| **Models.py**                | A module that builds, trains, and tests the model using the train, test, and validation set from `datasets.py`. It will return a result metrics and confusion matrix of the model performance. |
| **Utils.py**                 | A script that contains all the helper functions for data loading, cleaning, splitting, model building, training, testing, and evaluating. |
