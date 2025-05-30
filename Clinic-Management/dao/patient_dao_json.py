from dao.patient_dao import PatientDAO
from patient import Patient
from dao.patient_decoder import PatientDecoder
from dao.patient_encoder import PatientEncoder
import json
import os
class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave):
        self.patients = [] # holds the patients list
        self.autosave = autosave # assigns autosave
        self.load_patients() # loads any saved patients from storage automatially if needed
    def load_patients(self):# loads saved patients from the file if they exist
        if os.path.exists('clinic/patients.json'): # checks that the file exists
            with open('clinic/patients.json', 'r') as file: # if it does open and read
                self.patients = json.load(file, cls=PatientDecoder) # load the patient information using PatientDecoder
    def save_patients(self): # write the current patients to the storage file
        with open('clinic/patients.json', 'w') as file: # open file in write mode to save data
            json.dump(self.patients, file, cls=PatientEncoder) # coverts the patient list to a json format using Patient Encoder

    def search_patient(self, key): # searchs for the patient by key given which is a phn value
        for patient in self.patients: # go through all the patients 
            if patient.phn == key: # compare the values of the phns to the key
                return patient # return the matching patient that had the phn == key
        return None # if no match was found return none
    def create_patient(self, patient): # adds a patient object to the patients list
        self.patients.append(patient) # append it to the list
        self.save_patients() # write the current patients to the storage file
        return patient

    def retrieve_patients(self, search_string): # finds the patients which have the search_string in the name
        retrieved_list = [] # the list to return with all the matching patients
        for patient in self.patients:  # simple for loop for all patients to be checked
            if search_string in patient.name: # checks if our current patient contains the name given
                retrieved_list.append(patient) # adds all that pass to the list
        return retrieved_list
    def update_patient(self, key, patient): # iterate over the list of patients to find the patient with the given key(phn)
        for existing_patient in self.patients:
            if existing_patient.phn == key:
                # update all the details of the patient with the given information from 'patient' dict
                existing_patient.phn = patient['phn']
                existing_patient.name = patient['name']
                existing_patient.birth_date = patient['birth_date']
                existing_patient.phone = patient['phone']
                existing_patient.email = patient['email']
                existing_patient.address = patient['address']
                self.save_patients()# write the current patients new data to the storage file
    def delete_patient(self, key):# delete the patient with the given phn
        self.patients = [patient for patient in self.patients if patient.phn != key] # useing deletion by exlusion just save only the ones that do not match
        self.save_patients() # write the new current patients list to the storage file
    def list_patients(self):# lists the current patients list
        return self.patients # return the list of patients

