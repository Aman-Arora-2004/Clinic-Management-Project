from dao.note_dao import NoteDAO
from dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
    def __init__(self,phn):

        #Initilize Patient Record

        self.note_dao = NoteDAOPickle(NoteDAO, phn)         #instantiates a NoteDAOPickle class that inherits from the abstract NoteDAO class and assigns it to a field
                                                            #also passes PHN for 3.3
        self.notes = []

    def to_dict(self):

        #convert self (which is a patient) to a dictionary
        
        record_dict = vars(self)
        return record_dict