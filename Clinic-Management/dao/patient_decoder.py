import json
from patient import Patient

class PatientDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.object_hook) # Initializes the JSONDecoder and sets the object_hook to our custom object_hook
    def object_hook(self, obj):
        if 'phn' in obj and 'name' in obj: # Make surethe object dict has the key 'phn or 'name'
                                           # just to make extra sure we are dealing with a Patient
            return Patient( # then create and return the Patient using the values from our dict
                phn =obj['phn'],
                name=obj['name'],
                birth_date=obj['birth_date'],
                phone=obj['phone'],
                email=obj['email'],
                address=obj['address']
            )