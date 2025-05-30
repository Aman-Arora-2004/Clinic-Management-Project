from patient_record import PatientRecord
class Patient:
    def __init__(self, phn, name, birth_date, phone, email, address):

        #Initilize Patient 

        self.phn = phn                                              #personal health number
        self.name = name                                            #name 
        self.birth_date = birth_date                                #birth date
        self.phone = phone                                          #phone number
        self.email = email                                          #email
        self.address = address                                      #address
        self.patient_record = PatientRecord(phn)                   #call to patient record class
    
    def __eq__(self, other):

        #compare if two patients are equal, return true if yes, false if no

        if (isinstance(other, Patient)):                            #if other is of type patient
            return (self.phn == other.phn and self.name == other.name and self.birth_date == other.birth_date and self.phone == other.phone and self.email == other.email and self.address == other.address)
        return False
    
    def to_dict(self):
        
        #convert self (which is a patient) to a dictionary

        patient_dict = vars(self)
        return patient_dict