# DREAMT: Dataset for Real-time sleep stage EstimAtion using Multisensor wearable Technology

## Directory Structure

The main components of the project pipeline includes: 
* Extracting data from the raw data
* Perform preprocessing and feature enginering on the data
* Training models for classification

```bash
.
├── dataset_sample
    └── features_df
        └── SID_domain_features.csv
    └── E4_aggregate_subsample
        └── subsampled_SID_whole_df.csv
    └── participant_info.csv
├── results
│   └── quality_score_per_subject.csv
├── read_raw_e4.py
├── calculate_quality_score.py
├── feature_engineering.py
├── datasets.py
├── models.py
├── main.py
└── utils.py

```

## Setup

1. Clone this repository.
2. Create a Conda environment from `.yml` file.
```
conda env create --file environment.yml
```

## Description
`dataset_sample` is the folder containing a sample data folder for feature engineered data for every participant, a file for participant information, and subsampled raw signal data for each participant.  

`features_df` is the folder contarining the files for feature engineered data.  

`sid_domain_features_df.csv` is the csv file containing features calculated from the raw Empatica E4 data recorded during data collection.  

`participant_info.csv` is the csv file containing the basic information of the participant. 

`cpap_analysis.py` is a module that takes in the data and output the breathing information of each patient. The result will be outputed into a json file with patient number as file name.  

`quality_score_per_subject.csv`: is a file summarizing the percentage of artifacts of each subject's data calculated from features dataframe `sid_domain_features_df.csv`.   

`read_raw_e4.py` is a module that read raw Empatica E4 data, sleeps stage label, and sleep report to generate a dataframe that aligns the Empatica E4 data with sleep stage and sleep performance, such as Apnea-Hypopnea Index, by time.  

`read_raw_PSG.py` is a module that read raw polysomnography (PSG) data and extract the data during Empatica E4 recording.  

`feature_engineering.py` is a module that read the processed data by `read_raw_e4.py` and perform feature engineering on the data. The result data is stored in `feature_df` in `data`. 

`datasets.py` is a module that read the feature engineered data in `feature_df` and perform data loading, cleaning, and resampling. The processed data is split into train, test, and validation set.  

`models.py` is a module that build, train, and test the model using the train, test, and validation set from `datasets.py`. It will return a result metrics and confusion matrix of the model performance.  

`main.py` is a module that run the entire process of data loading, cleaning, splitting, model building, training, testing and evaluating.  

`utils.py` is a script that contains all the helper functions for data loading, cleaning, splitting, model building, training, testing, and evaluating.  

## Additional Notes

1. Clone this repo
2. Run conda list --export > requirements.txt in the repo path to convert environment file to requirements.txt
