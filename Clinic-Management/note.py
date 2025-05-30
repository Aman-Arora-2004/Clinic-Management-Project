from datetime import datetime
class Note:
    def __init__(self, index, text):

        #Initilize note

        self.index = index #note index
        self.text = text   #note text
        self.timestamp = datetime.now()

    def __eq__(self, other): 

        #compare if two notes are equal, return true if they are, return false if not

        if isinstance(other, Note):              #if other is of type note
            return (self.index == other.index and self.text == other.text)
        return False