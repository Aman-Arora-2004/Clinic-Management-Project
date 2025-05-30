import hashlib
from patient import Patient
from patient_record import PatientRecord
from note import Note
from datetime import datetime
from exception.invalid_login_exception import InvalidLoginException
from exception.duplicate_login_exception import DuplicateLoginException
from exception.invalid_logout_exception import InvalidLogoutException
from exception.illegal_access_exception import IllegalAccessException
from exception.illegal_operation_exception import IllegalOperationException
from exception.no_current_patient_exception import NoCurrentPatientException
from dao.patient_dao_json import PatientDAOJSON
from dao.patient_dao import PatientDAO
from dao.note_dao import NoteDAO
from dao.note_dao_pickle import NoteDAOPickle

class Controller:
    def __init__(self, autosave=False):
            
            #Initilize controller

            self.logged_in = False          #logged in
            self.cur_patient = None         #current patient
            self.autosave = autosave        #autosave (for persistence)
            self.users = {}                 #holds the users
            self.patient_dao = PatientDAOJSON(autosave=self.autosave) #instantiates a PATIENDAOJSON class that inherits from the abstract PatientDAO class and assigns it to a field
            self.load_users("users.txt") #loads the users into load_users function to be assigned to the
                                                #appropriate dict of users for use in login and logout

    def load_users(self, file_path):

        #function to read users from the filepath. 
        #takes a filepath as an input and splits the username and hashed password. then adds the username and password to users dictionary

        with open(file_path, 'r') as file:
            for line in file:
                username, hashed_password = line.strip().split(',')     #splits the username and hashed password
                self.users[username] = hashed_password                  #adds username and password to self.users

    def login(self, username, password):

        #function to login. user enters a username and password,
        #function checks to see if values are correct and if yes then logs in and returns True

        if self.logged_in:                                              #if already logged in, raise error
            raise DuplicateLoginException("cannot login again while still logged in")
        
        if username not in self.users:                                  #if username is not in the list of users, raise error 
            raise InvalidLoginException("login in with incorrect username")                
        
        input_hash = hashlib.sha256(password.encode()).hexdigest()      #password is converted to a byte, which is then converted to a hash value, which is then
                                                                        #converted to a hex hash value, which we will use to compare with our stored passwords in user.txt

        if self.users[username] != input_hash:                          #if password is wrong, raise error
            raise InvalidLoginException("login in with incorrect password")
        self.logged_in = True                                           #logged in 
        return True
                
    def logout(self):

        #function to log user out
        #inputs nothing and returns true if logged out successfully

        if not self.logged_in:                                          #if not logged in, throw error
            raise InvalidLogoutException("log out only after being logged in")
        
        if self.cur_patient is not None:                                #if cur patient is set, it must be unset before logging out
            self.unset_current_patient()
        
        self.logged_in = False                                          #logged out
        return True 
        
    def search_patient(self, phn):

        #function to search patient by phn. 
        #inputs a patients phn and if found, outputs the patient

        if not self.logged_in:                                          #if not logged in, throw error
           raise IllegalAccessException("cannot search patient without logging in")
        return self.patient_dao.search_patient(phn)                     #calls search_patient in patient_dao. If successful, it returns the patient

    def create_patient(self, phn, name, birth_date, phone, email, address):

        #function to create new patient
        #inputs phn, name, birth date, phone, email and address
        #outputs the new patient that is created

        if not self.logged_in:                                          #if not logged in, throw error
            raise IllegalAccessException("cannot create patient without logging in")
        
        if self.patient_dao.search_patient(phn) is None:                #calls search patient in patient_dao, if there is no patient already, create new one
            new_patient = Patient(phn, name, birth_date, phone, email, address)     #new patient object
            self.patient_dao.create_patient(new_patient)                #calls create_patient in patient_dao, which creates the new patient and adds it to self.patients in patientdaojson
            return new_patient                                          #returns created patient
        
        raise IllegalOperationException("cannot add a patient with a phn that is already registered")
    
    def retrieve_patients(self, name):

        #function to retrieve a list of patients that have the name as a part of the patients name
        #inputs a name and outputs a list of patient that have the name as part of their name

        if not self.logged_in:                                          #if not logged in, throw error
            raise IllegalAccessException("cannot retrieve patients without logging in")
        return self.patient_dao.retrieve_patients(name)                 #calls retrieve_patients in patient_dao, which retrieves a list of patients that have the name as a part of the patients name
    
    def update_patient(self, phn, new_phn, name, birth_date, phone, email, address):

        #function to search patient by phn, retrieve their data and update any part of it
        #inputs a phn, and all the data that is getting updated including new_phn, name, birth date, email, address

        if not self.logged_in:                                          #if not logged in, throw error      
            raise IllegalAccessException("cannot update patient without logging in")
        
        if self.cur_patient is not None:                                #if cur patient is not none, throw error
            raise  IllegalOperationException("cannot update the current patient")
        
        patient = self.search_patient(phn)                              #searches the patient from given phn and assigns to patient
        
        if not patient:                                                 #cant find patient with given phn, throw error
            raise IllegalOperationException("cannot update patient with a phn that is not registered")
        
        if(patient.phn == new_phn and patient.name == name and patient.birth_date == birth_date and patient.phone == phone and patient.email == email and patient.address == address):
            return None                                                 # this is reached in the case nothing is changed
        
        if new_phn != phn and self.patient_dao.search_patient(new_phn): #return none if it cant update to new_phn
            raise IllegalOperationException("cannot update patient and give them a registered phn")
        
        updated_data = {                                                #update all the data
            'phn': new_phn,
            'name': name,
            'birth_date': birth_date,
            'phone': phone,
            'email': email,
            'address': address
        }

        self.patient_dao.update_patient(phn, updated_data)              #calls update_patients in patients_dao, which gives the updated data values to phn
        return self.patient_dao.search_patient(new_phn)                 #if the patient is updated, it searches for the new_phn and returns the patient
    
    def delete_patient(self, phn):

        #function to search patient by phn and delete them.
        #inputs a phn and outputs the patient that is deleted

        if not self.logged_in:                                          #if not logged in, throw error
            raise IllegalAccessException("cannot delete patient without logging in")
        
        if self.cur_patient is not None:                                #if current patient is not none, throw error
            raise IllegalOperationException("cannot delete the current patient")
        
        patient = self.patient_dao.search_patient(phn)                  #searches the patient from given phn and assigns to patient

        if not patient:                                                 #cant find patient with given phn
            raise IllegalOperationException("cannot delete patient with a phn that is not registered")
        
        self.patient_dao.delete_patient(phn)                            #calls delete_patient in patient_dao, which deletes the patient with the given phn
        return patient                                                  #return deleted patients

    def list_patients(self):

        #function to return a list of all patients
        #inputs nothing and outputs a list of all the patients

        if not self.logged_in:                                          #if not logged in, throw error
            raise IllegalAccessException("cannot list patients without logging in")
        
        return self.patient_dao.list_patients()                         #calls list_patients in patients_dao, which then returns the grand list of all patients
    
    def set_current_patient(self, phn):

        #function to set the current patient
        #inputs a phn and outputs the patient that is currently set

        if not self.logged_in:                                          #if not logged in, throw error
            raise IllegalAccessException("cannot set current patient without logging in")
        
        patient = self.search_patient(phn)                              #searches the patient from given phn and assigns to patient

        if patient is None:                                             #if patient not found, throw error
            raise IllegalOperationException("cannot set non-existent patient as the current patient")
        self.cur_patient = patient                                      #set current patient
        return patient                                                  #return current_patient
    
    def get_current_patient(self):

        #function to get the current patient
        #inputs nothing and outputs the patient that is currently set

        if not self.logged_in:                                          #if not logged in, throw error
            raise IllegalAccessException("cannot get current patient without logging in")
        
        return self.cur_patient                                         #returns current patient
    
    def unset_current_patient(self):

        #function to unset the current patient
        #inputs nothing and outputs True if the patient was unset, false otherwise

        if not self.logged_in:                                          #if not logged in, throw error
            raise IllegalAccessException("cannot unset current patient without logging in")
        
        if self.cur_patient is not None:                                #if current patient is set, unset it
            self.cur_patient = None                                     #unset patient
            return True
        return False
    
    def create_note(self, text_note):

        #function to create a new note
        #stores the index as the auto-incrementented counter in note_dao_pickle and also stores the timestamp and textnote 
        #inputs text that the note will contain and outputs the new note

        if not self.logged_in:                                          #if not logged in, throw error
            raise IllegalAccessException("cannot add note for a patient without logging in")
        
        if self.cur_patient is None:                                    #if patient is not set, throw error
            raise NoCurrentPatientException("cannot add note without a valid current patient")
        
        new_note = self.cur_patient.patient_record.note_dao.create_note(text_note) #calls create note from note_dao from patient record, which creates the new note
        self.cur_patient.patient_record.note_dao.save_notes()           #saves the current patients' notes to a file based on the patients phn
        return new_note                                                 #return newly created note
    
    def search_note(self, note_index):

        #function to search the notes from the given note index
        #inputs a note index and outputs the note if found

        if not self.logged_in:                                          #if not logged in, throw error
            raise IllegalAccessException("cannot search note for a patient without logging in")
        
        if self.cur_patient is None:                                    #if current patient is not set, throw error
            raise NoCurrentPatientException("cannot search note without a valid current patient")
        
        return self.cur_patient.patient_record.note_dao.search_note(note_index) #calls search note from note_dao from patient_record, which searches for the 
                                                                                #note given the index and returns it
    
    def retrieve_notes(self, text_note):

        #function to retrieve a list of notes that have the searched text_note as a part of the notes name
        #inputs text note and outputs a list of notes that contain that text

        if not self.logged_in:                                          #if not logged in, throw error
            raise IllegalAccessException("cannot retrieve notes for a patient without logging in")
        
        if self.cur_patient is None:                                    #if current patient is not set, throw error
            raise NoCurrentPatientException("cannot retrieve notes without a valid current patient")
        
        return self.cur_patient.patient_record.note_dao.retrieve_notes(text_note) #calls retrieve_notes from note_dao from patient_record, which retrieves
                                                                                  #a list of notes that have the searched text_note as a part of the notes name

    def update_note(self, note_index, new_text_note):

        #function to select a note by the index, retrieve the details and timestamp and update the details and the timestamp to the current time
        #inputs the note_index and the new text and outputs the updated note

        if not self.logged_in:                                          #if not logged in, throw error
            raise IllegalAccessException("cannot update note for a patient without logging in")
        
        if self.cur_patient is None:                                    #if current patient is not set, throw error
            raise NoCurrentPatientException("cannot update note without a valid current patient")
        
        current_note = self.search_note(note_index)                     #searches the note from given index and assigns to current_note
        
        if not current_note:                                            #make sure that there exists a note at this index to be updated
            return None
        
        if current_note == new_text_note:                               #if both notes are the same nothing have been updated!
            return None
        
        self.cur_patient.patient_record.note_dao.update_note(current_note, new_text_note)   #calls update_note from note_dao from patient_record which
        #selects a note by the index, retrieves the text and timestamp and update the text and the timestamp to the current time
        
        self.cur_patient.patient_record.note_dao.save_notes()            #saves the current patients' notes to a file based on the patients phn
        
        return current_note                                              #return current note
        
    def delete_note(self, note_index):

        #function to delete the note given by the index
        #inputs the index that the note has to be deleted and outputs true if note is deleted

        if not self.logged_in:                                         #if not logged in, throw error
            raise  IllegalAccessException("cannot delete note for a patient without logging in")
        
        if self.cur_patient is None:                                   #if current patient is not set, throw error
            raise NoCurrentPatientException("cannot delete note without a valid current patient")
        
        current_note = self.cur_patient.patient_record.note_dao.search_note(note_index) #searches the note from given index and assigns to current_note

        if not current_note:                                           #double checking that current_note we were asked to delete even exists
            return None
        
        deleted = self.cur_patient.patient_record.note_dao.delete_note(current_note) #calls delete_note from note_dao from patient_record, which deletes the current note
        #and outputs true if deleted
        
        if deleted:                                                     #if deleted is true, save the note
            self.cur_patient.patient_record.note_dao.save_notes()       #saves the current patients' notes to a file based on the patients phn
        
        return deleted                                                  #return true or false based on if note is deleted or not
        
    
    def list_notes(self):

        #function to list all the notes for a given patient
        #inputs nothing and outputs a list of all the notes, from the last created to first created

        if not self.logged_in:                                  #if not logged in, throw error
            raise IllegalAccessException("cannot list notes for a patient without logging in")
        
        if self.cur_patient is None:                            #if current patient is not set, throw error
            raise NoCurrentPatientException("cannot list notes without a valid current patient")
        
        return self.cur_patient.patient_record.note_dao.list_notes()    #calls list_notes from notes_dao from patient_record which lists all the notes for a given patient from last to first created
