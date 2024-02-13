import pandas as pd
import numpy as np
from datetime import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def death_age(rows):
    DOB, DOD = rows[0], rows[1]
    if str(DOD) != 'nan':
        return (dt.strptime(DOD, '%Y-%m-%d %H:%M:%S') - dt.strptime(DOB, '%Y-%m-%d %H:%M:%S')).days / 365.25
    
def threedigiticd(codes):
    if isinstance(codes, list):
        icd9_list = []
        for code in codes:
            if code != 'nan':
                icd9_list = ["".join(filter(str.isdigit, str(code)))[:3] for code in codes]
        return icd9_list
                    
    else:
        return []
    
    
Admissions = pd.read_csv("C:\\Users\\micha\\Documents\\Data science projects\\Mimic_project\\Mimic_datasets\\ADMISSIONS.csv")
Diagnoses = pd.read_csv("C:\\Users\\micha\\Documents\\Data science projects\\Mimic_project\\Mimic_datasets\\DIAGNOSES_ICD.csv")
Labs = pd.read_csv("C:\\Users\\micha\\Documents\\Data science projects\\Mimic_project\\Mimic_datasets\\LABEVENTS.csv")
Patients = pd.read_csv("C:\\Users\\micha\\Documents\\Data science projects\\Mimic_project\\Mimic_datasets\\PATIENTS.csv")
#Prescriptions = pd.read_csv("C:\\Users\\micha\\Documents\\Data science projects\\Mimic_project\\Mimic_datasets\\PRESCRIPTIONS.csv")

Dataset = pd.DataFrame()
Dataset['SUBJECT_ID'] = Patients['SUBJECT_ID']
Dataset['Alive'] = Patients['EXPIRE_FLAG'] == 0
Dataset["Death_Age"] = Patients[['DOB', 'DOD']].apply(death_age, axis = 1)

Admissions = Admissions.groupby('SUBJECT_ID').agg({'HADM_ID':lambda x: x.tolist(), 'ADMISSION_TYPE': lambda x: x.tolist()[0]}).reset_index()
Admissions = Admissions.explode('HADM_ID')
Diagnoses = Diagnoses.groupby('SUBJECT_ID').agg({'HADM_ID': lambda x: x.tolist()[0], 'ICD9_CODE': lambda x: x.tolist()}).reset_index()

mask = Labs['FLAG'] == 'abnormal'
Labs = Labs[mask].reset_index(drop=True)
Labs = Labs.iloc[:,[1,2,3,8]]

Patient_Data = pd.merge(Admissions, Diagnoses, on=['SUBJECT_ID', "HADM_ID"], how = 'left')
Patient_Data = pd.merge(Dataset, Patient_Data, on=['SUBJECT_ID'], how = 'left')
Patient_Data['ICD9_CODE'] = Patient_Data['ICD9_CODE'].apply(threedigiticd)

print(Patient_Data.head(100))

