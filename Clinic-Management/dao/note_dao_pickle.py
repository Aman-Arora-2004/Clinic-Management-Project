from dao.note_dao import NoteDAO
from note import Note
from datetime import datetime
import pickle
import os
class NoteDAOPickle(NoteDAO):
    def __init__(self, autosave, phn): 
        self.notes = [] # holds the notes for the current patient
        self.autosave = autosave # saves the autosave 
        self.autocounter = 0 # start our autocounter at 0 for indexing
        self.phn = phn # setup phn for use in storage setup later
        if self.autosave: # checks autosave status
            self.load_notes() # loads any saved notes from storage automatially if needed
    def load_notes(self): # load saved notes from the file if they exist, else create directory if needed
        records_path = 'clinic/records'  # define path for storage of records
        if not os.path.exists(records_path): # ensure the records file exists or else create it
            os.makedirs(records_path)
        filepath = f'clinic/records/{self.phn}.dat' # setup filename using phn in records as outlined in 3.3 with patiend phn and .dat
        if os.path.exists(filepath): # if there exists a current patient open it up and load it, then save the autocounter to the current 
                                     # number len of notes so we are indexing properly.
            with open(filepath, 'rb') as file:
                self.notes = pickle.load(file)
                self.autocounter = len(self.notes)
    def save_notes(self): # saves the current patients notes to a file which is named based on the patients phn
        records_path = 'clinic/records'
        if not os.path.exists(records_path):# if records_path does not exist then create it
            os.makedirs(records_path)
        filepath = f'clinic/records/{self.phn}.dat' # defines current patients filename based on phn
        with open(filepath, 'wb') as file: # open the file up in binrary write mode and dump the notes using pickle
            pickle.dump(self.notes, file)

    def search_note(self, key): # searchs for the given note given the key(aka index value)
        for note in self.notes: # goes through each note in a loop
            if note.index == key: # if the note.index matchs the key
                return note # return the found note
        else:
            return None # if no matchs found then the note does not exist
    
    def create_note(self, text): # creates a note given the text input of the note
        note_index = self.autocounter+1 # updates the counter so we keep track of total for indexing reasons
        new_note = Note(note_index, text) # creates the new note object
        self.notes.append(new_note)  # adds the cur_patients new note 
        self.autocounter += 1 # and includes the index from our counter for later useage
        self.save_notes() # saves the current patients notes to a file which is named based on the patients phn
        return new_note
    
    def retrieve_notes(self, search_string): # gets the notes that are equal to a given a string to search for
        note_list = [] # define a list which we will populate with the equal notes to the search string given
        for note in self.notes: # loops through note by note
            if search_string.lower() in note.text.lower(): # find all the notes with the given text inside
                note_list.append(note) # adds any found to our grand list
        return note_list # then we return the grand list

    def update_note(self, key, text):# updates our current patients note
        key.text = text # update to new text
        key.timestamp = datetime.now() # updates the time stamp to new time
        self.save_notes() # saves the current patients notes to a file which is named based on the patients phn
    
    def delete_note(self, key): # deletes a note given a key text
        for note in self.notes: 
            if note == key: # comes the key with the notes througout the list
                self.notes.remove(key) # if found removes the note in the list at the given key
                self.autocounter -= 1 # counter is now one less as we removed a note
                self.reindex_notes() # updates all the indexes in the notes remaining
                self.save_notes() # saves the current patients notes to a file which is named based on the patients phn
                return True # deleted a note succefully 
        return False # did not find the note to delete
    
    def list_notes(self): # lists all the patients current notes
        notes_list = [] # a list of the notes we will return 
        for note in self.notes: # goes through all the notes
            notes_list.append(note) # appends the notes to our notes_list
        notes_list = notes_list[::-1] # reverse the entire list so the last notes created are before older ones
        return notes_list # finally return the notes list
    def reindex_notes(self): # for updating the remaining indexs 
        cur_index = 1 # we start at one
        for note in self.notes: # for all remaining notes 
            note.index = cur_index # updates the indexes to fill the gap created by delete
            cur_index += 1 # go to next index 
        
