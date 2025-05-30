import json
from patient import Patient
from patient_record import PatientRecord

class PatientEncoder(json.JSONEncoder):
    def default(self, obj): # override the default method to handle custom serialization for Patient and Patient_Record
        if isinstance(obj, (Patient, PatientRecord)):#if the object is a Patient or Patient_Record convert it to a dict
            return obj.to_dict()#use the to_dict method to convert to JSONs wanted format