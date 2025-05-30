import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QWidget, QLabel, QTableView, QHeaderView, QPlainTextEdit, QTextEdit
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from exception.invalid_login_exception import InvalidLoginException
from exception.duplicate_login_exception import DuplicateLoginException
from exception.invalid_logout_exception import InvalidLogoutException
from exception.illegal_access_exception import IllegalAccessException
from exception.illegal_operation_exception import IllegalOperationException
from exception.no_current_patient_exception import NoCurrentPatientException
from controller import Controller
from patient import Patient
from datetime import datetime

class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # Continue here with your code!
        self.controller = Controller()
        self.setWindowTitle("SkyNet_Clinic_Management.inc") # change if asked as if might need to be called something exaclty
        self.central_widget = QWidget(self) # central widget for the main window
        self.layout = QVBoxLayout(self.central_widget) # Vertical layout
        self.setCentralWidget(self.central_widget) # assign the central widget
        self.resize(900,700)        #resizes widget to 900x700
        self.show_login_box()

    def show_login_box(self):

        #shows the window before a user is logged in

        self.clear_layout()                                         #makes sure no unwanted pop-up open

        #username input box
        self.username_input = QLineEdit(self)                   #input
        self.username_input.setPlaceholderText("Username: ")    #text before input is entered
        self.username_input.setStyleSheet("""                   
        color: red;
        font-family: "Courier New";
        font-size: 20pt;
                                    """)                        #style of the text
        
        #password input box
        self.password_input = QLineEdit(self)                   #input
        self.password_input.setPlaceholderText("Password: ")    #text before input is entered
        self.password_input.setStyleSheet(
            """ color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )                                                       #style of the text
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password) # do in Echo mode to ensure password is hidden
        self.login_button = QPushButton("Login", self)          #button that says Login
        self.login_button.setStyleSheet(
            """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """)                        #stylesheet of the button
        self.layout.addWidget(self.username_input)              #add username input
        self.layout.addWidget(self.password_input)              #add password input
        self.layout.addWidget(self.login_button)                #add login button
        self.login_button.clicked.connect(self.handle_login)    #once login button is clicked, call handle login

    def handle_login(self):

        #handles login once login_button is clicked

        username = self.username_input.text()                   #gets username from input
        password = self.password_input.text()                   #get password from input
        try:
            self.controller.login(username, password)           #try calling login from controller with inputted username and password
            QMessageBox.information(self, "Login Success", "Logged in successsfully")       #if successful, shows Message Box
            self.show_main_menu()                               #shows the main menu
        except InvalidLoginException:                           #if username or password is wrong, it raises an error
             QMessageBox.warning(self, "Login Failed", "Invalid username or password")
        except DuplicateLoginException:                         #if already logged in, cannot log in again
            QMessageBox.warning(self, "Login Failed", "cannot login again while still logged in")
    
    def handle_logout(self):

        #logs out the patient once the logout button has been pressed from the main menu

        self.controller.logout()                            #call logout from controller
        QMessageBox.information(self, "Logout Success", "You have been logged out")
        self.show_login_box()                               #gives the option for the user to login again
    
    
    
    
    
    
    
    
    def show_add_new_patient_box(self):

        #shows the add new patient menu once add new patient is clicked 
        #the user inputs all the information of the user, which is created when the create patient button is clicked 

        self.clear_layout()                                 #makes sure no unwanted widgets are opened

        self.phn_input = QLineEdit(self)                    #phn input 
        self.phn_input.setPlaceholderText("Patient's Personal Health Number")       #text for phn input
        self.phn_input.setStyleSheet(       
            """color: red;                    
            font-family: "Courier New";
            font-size: 14pt;
                                    """
        )                                                   #stylesheet for phn input

        self.name_input = QLineEdit(self)                   #name input
        self.name_input.setPlaceholderText("Patient's Full Given Name")             #text for name input
        self.name_input.setStyleSheet( """color: red;                    
            font-family: "Courier New";
            font-size: 14pt;
                                    """
        )                                                   #style sheet for name input

        self.birth_date_input = QLineEdit(self)             #birth date input
        self.birth_date_input.setPlaceholderText("Patient's Date Of Birth (YYYY-MM-DD)")        #text for birth date
        self.birth_date_input.setStyleSheet("""color: red;                    
            font-family: "Courier New";
            font-size: 14pt;
                                    """
        )                                                   #style sheet for birth input
        self.birth_date_input.setToolTip("Date Format (YYYY-MM-DD)")  #shows the input format when hovering over the input box 
        
        self.phone_input = QLineEdit(self)                  #phone input
        self.phone_input.setPlaceholderText("Patient's Primary Contact Number")             #text for phone number
        self.phone_input.setStyleSheet( """color: red;                    
            font-family: "Courier New";
            font-size: 14pt;
                                    """
        )                                                   #style sheet for phone input

        self.email_input = QLineEdit(self)                  #email input
        self.email_input.setPlaceholderText("Patient's Primary Contact Email")               #text for email input
        self.email_input.setStyleSheet( """color: red;                    
            font-family: "Courier New";
            font-size: 14pt;
                                    """
        )                                                   #style sheet for email input

        self.address_input = QLineEdit(self)                #address input
        self.address_input.setPlaceholderText("Patient's Primary Address")      #text for address input
        self.address_input.setStyleSheet( """color: red;                    
            font-family: "Courier New";
            font-size: 14pt;
                                    """
        )                                                   #style sheet for address input

        self.layout.addWidget(self.phn_input)                   #add input to window
        self.layout.addWidget(self.name_input)                  #add input to window
        self.layout.addWidget(self.birth_date_input)            #add input to window
        self.layout.addWidget(self.phone_input)                 #add input to window
        self.layout.addWidget(self.email_input)                 #add input to window
        self.layout.addWidget(self.address_input)               #add input to window

        self.create_new_patient_button = QPushButton("Create Patient")          #create patient button
        self.create_new_patient_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )                                                       #style sheet for create patient button
        self.layout.addWidget(self.create_new_patient_button)   #add create patient button
        self.create_new_patient_button.clicked.connect(self.handle_patient_create)          #once create patient is clicked, call handle patient create

        self.show_main_menu_button()                            #show main menu button if patient wants to return to main menu


    def handle_patient_create(self): 

        #handles creating a patient with all the inputs given

        try:
            if self.email_input.text().strip() == "" or self.address_input.text().strip() == "" or self.name_input.text().strip() == "" or self.phone_input.text().strip() == "":
                #if name, phone, email or address input boxes are empty, it must contain a value
                QMessageBox.warning(self, "Creation Failed", "All fields must contain values")
                return
            
            if self.phn_input.text().isdigit():
                #if phn is a number, assign phn input to  phn
                phn = self.phn_input.text()
            else:
                #phn must contain only numbers
                QMessageBox.warning(self, "Creation Failed", "PHN Must Be Digits")
                return

            if self.name_input.text().isdigit():
                #if the name contains any numbers, it must to be changed to only contain letters
                QMessageBox.warning(self, "Creation Failed", "Name Must Not Contain Any Digits")
                return
            else:
                #the name contains only letters, assign name input to name
                name = self.name_input.text()
            
            if self.validate(self.birth_date_input.text()):
                #calls the validate function, which checks if the birth date is in the correct format
                #if it is in the correct format, assign birth date input to birth date
                birth_date = self.birth_date_input.text()
            else:
                #birth date must adhere to the format and be valid according to the calender
                QMessageBox.warning(self, "Creation Failed", "Birth Date wrong")
                return
            phone_number_no_space = self.phone_input.text().replace(" ","") # remove all spaces in the number 
            if not phone_number_no_space.isdigit(): # check to see if what is remaining after clearing spaces is all digits
                QMessageBox.warning(self, "Creation Failed", "Phone Number Must Be Digits") # if not then raise warning
                return 
            else: 
                phone = phone_number_no_space  #else phone number is all good and we can assign the number with no spaces to phone

            email = self.email_input.text()             #assign email input to email
            address = self.address_input.text()         #assign address input to address
            self.controller.create_patient(phn, name, birth_date,phone,email,address)       #calls create patient from controller now that all the inputs have been handled and assigned
            QMessageBox.information(self, "Patient Created", "Patient Created Successfully")
            
            self.show_add_new_patient_box()             #shows add new patient menu
        except IllegalOperationException:               #if phn is registered already, raise error
            QMessageBox.warning(self, "Creation Failed", "cannot add a patient with a phn that is already registered")


    def show_search_patient_box(self):

        #shows the search patient menu once search patient is clicked 

        self.clear_layout()                                             #makes sure no unwanted widgets are opened
        
        #phn input for search patient
        self.phn_input = QLineEdit(self)
        self.phn_input.setPlaceholderText("Patient's PHN")
        self.phn_input.setStyleSheet("""color: red;                    
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.phn_input)       #add phn input to the window
        
        #search patient button
        self.search_patient_button = QPushButton("Search patient by PHN")
        self.search_patient_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.search_patient_button)       #add search patient button to the window
        self.search_patient_button.clicked.connect(self.handle_search_patient)      #once search patient button is clicked, call handle search patient

        self.show_main_menu_button()                            #show main menu button if patient wants to return to main menu


    def handle_search_patient(self):

        #handles search patient once search patient button is clicked

        search_phn_value = self.phn_input.text()        #grabs phn from input
        patient = self.controller.search_patient(search_phn_value)      #calls search patient from controller class with given phn
        if patient is None:
            #if phn doesnt exist, input a valid one
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid PHN")
            return

        #now that patient has been found, display the results

        details = (
                f"PHN: {patient.phn}\n"
                f"Name: {patient.name}\n"
                f"D.O.B: {patient.birth_date}\n"
                f"Phone Number: {patient.phone}\n"
                f"Email: {patient.email}\n"
                f"Address: {patient.address}\n"
        )   # holds searched patient details
        QMessageBox.information(self, "Patient Found", "Loading Details Now")
        self.show_searched_patient(details) #calls show searched patient, which shows the patient that has been searched

    def show_searched_patient(self,details):

        #once patient has been searched and details have been assigned, show the patient

        self.clear_layout()                         #makes sure no unwanted widgets are opened

        patient_label = QLabel(details)             #assign details as a QLabel to patient label
        patient_label.setStyleSheet("""
        font-family: "Courier New";
        font-size: 20pt;
                                    """)            #style patient label
        patient_label.setWordWrap(True)             #breaks into multiple lines if text is too long 
        self.layout.addWidget(patient_label)        #add the patient details on the window

        #find another patient button
        self.next_patient_button = QPushButton("Find Anouther Patient")
        self.next_patient_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.next_patient_button) #adds find another patient button to screen
        self.next_patient_button.clicked.connect(self.show_search_patient_box) #if find another patient button is clicked, show the search patient menu
        self.show_main_menu_button()                    #show main menu button if patient wants to return to main menu
        
    def show_retrieve_patients_box(self):

        #once retrieved patients has been clicked, show the retrieve patients menu

        self.clear_layout()                         #makes sure no unwanted widgets are opened

        #patient name input
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Patient's Name")
        self.name_input.setStyleSheet("""color: red;                    
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.name_input)      #add patient name input to the window

        #retrieve patient by name button
        self.retrieve_patient_button = QPushButton("Search patient by Name")
        self.retrieve_patient_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.retrieve_patient_button) #adds retrieve patient button to the window
        self.retrieve_patient_button.clicked.connect(self.handle_retrieve_patients) #if retrieve patient button is clicked, call handle retrieve patients
        self.show_main_menu_button()                #show main menu button if patient wants to return to main menu

    def handle_retrieve_patients(self):

        #handles retrieve patients once retrieve patient button is clicked

        name = self.name_input.text().strip()       #get name from input
        if not name:
            #if name doesn't exist, enter a valid name
            QMessageBox.warning(self, "Invalid Input", "Please Enter A Valid Name")
            self.show_retrieve_patients_box #return back to retrieve patients menu
            return
        patients = self.controller.retrieve_patients(name)      #calls retrieve patient from controller with given name
        if not patients:
            #if there are no patients with the given name, return back to retrieve notes menu
            QMessageBox.warning(self, "Invalid Input", f"Could not find Patient's with the Name: {name}")
            self.show_retrieve_patients_box
            return
        self.clear_layout()                         #makes sure no unwanted widgets are opened
        model = QStandardItemModel()                #set model as a QStandardItemModel
        model.setHorizontalHeaderLabels(["PHN","Name","D.O.B","Phone#", "Email","Address"]) #set horizontal header labels for all patient information
        for patient in patients: #go through every patient in patients, which is returned from retrieve notes in controller

            phn_item = QStandardItem(patient.phn)
            name_item = QStandardItem(patient.name)
            dob_item = QStandardItem(patient.birth_date)
            phone_item = QStandardItem(patient.phone)
            email_item = QStandardItem(patient.email)
            address_item = QStandardItem(patient.address)
            model.appendRow([phn_item, name_item, dob_item, phone_item, email_item, address_item])
            #create and append retrieved patient 
        
        self.table_view = QTableView()          #create a table view
        self.table_view.setModel(model)         #connect model to table view
        header = self.table_view.horizontalHeader()     #get header of table
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch) #make sure columns automatially resize to evenly fit available space
        self.layout.addWidget(self.table_view)      #add the table to the window

        #retrieve new patient button 
        self.retrieve_patients_button = QPushButton("Retrieve New Patients") # create a push button for new patients
        self.retrieve_patients_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.retrieve_patients_button)        #add retrieve new patient button to window
        self.retrieve_patients_button.clicked.connect(self.show_retrieve_patients_box)  #if retrieve new patient button is clicked, go to retrieve patients menu
        self.show_main_menu_button()                #show main menu button if patient wants to return to main menu

    def show_update_patient_menu(self): # sets up the patient update menu layout
        self.clear_layout() # clear the layout so nothing overlaps from last page
        self.phn_input = QLineEdit(self) # sets up the phn_input to take whatever is put into the QLineEdit 
        self.phn_input.setPlaceholderText("Patient's PHN") # puts a placeholder so the user know what needs to go inside
        self.phn_input.setStyleSheet("""color: red;                    
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        ) # some style changes for looks

        self.layout.addWidget(self.phn_input) # add the PHN input widget to the layout
        self.search_patient_update_button = QPushButton("Find Patient File") 
        self.search_patient_update_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.search_patient_update_button)
        self.search_patient_update_button.clicked.connect(self.show_update_patient) # connect the button's click signal to the show_update_patient function so it can take care of the remaining logic

        self.show_main_menu_button() 
    def show_update_patient(self):
        # logic to retrieve and display patient details for updating
        phn_input_cur = self.phn_input.text() # get the phn entered by the user ensuring its text form
        patient = self.controller.search_patient(phn_input_cur) # search the patient using the phn
        if patient is None: # if the phn is not valid we ask the user to correct the mistake and return them back to the prompt so they can
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid PHN")
            return
        details = ( # use the found search values and place them in details
                f"PHN: {patient.phn}\n"
                f"Name: {patient.name}\n"
                f"D.O.B: {patient.birth_date}\n"
                f"Phone Number: {patient.phone}\n"
                f"Email: {patient.email}\n"
                f"Address: {patient.address}\n"
        )
        # then assign the cur's with these values, this is so that later if details are found to be given as nothing(meaning no change) we can just use the values of the cur's to access what they were
        self.name_cur = patient.name
        self.phn_cur = patient.phn
        self.birth_date_cur = patient.birth_date
        self.phone_cur = patient.phone
        self.address_cur = patient.address
        self.email_cur = patient.email
        QMessageBox.information(self, "Patient Found", "Loading Details Now")
        self.show_searched_patient_for_update(details)

    def show_searched_patient_for_update(self, details):
        # alot of this function is repeated logic thus only explaining new logic, refer to above for logic explained
        self.clear_layout()
        patient_label = QLabel(details)
        patient_label.setStyleSheet("""
        font-family: "Courier New";
        font-size: 20pt;
                                    """)
        patient_label.setWordWrap(True) # ensures that no lines go over and get cutoff, by setting true we can make sure all details are shown
        self.layout.addWidget(patient_label)

        self.new_phn_input = QLineEdit(self)
        self.new_phn_input.setPlaceholderText("New Patient's Personal Health Number")
        self.new_phn_input.setStyleSheet(
            """color: red;                    
            font-family: "Courier New";
            font-size: 14pt;
                                    """
        )

        self.new_name_input = QLineEdit(self)
        self.new_name_input.setPlaceholderText("New Patient's Full Given Name")
        self.new_name_input.setStyleSheet( """color: red;                    
            font-family: "Courier New";
            font-size: 14pt;
                                    """
        )

        self.new_birth_date_input = QLineEdit(self)
        self.new_birth_date_input.setPlaceholderText("New Patient's Date Of Birth (YYYY-MM-DD)")
        self.new_birth_date_input.setStyleSheet("""color: red;                    
            font-family: "Courier New";
            font-size: 14pt;
                                    """
        )
        self.new_birth_date_input.setToolTip("Date Format (YYYY-MM-DD)") # this allows for the user to hover the input widget button and see the format in case they need to see it without
                                                                        # making them delete the whole thing again
        
        self.new_phone_input = QLineEdit(self)
        self.new_phone_input.setPlaceholderText("New Patient's Primary Contact Number")
        self.new_phone_input.setStyleSheet( """color: red;                    
            font-family: "Courier New";
            font-size: 14pt;
                                    """
        )

        self.new_email_input = QLineEdit(self)
        self.new_email_input.setPlaceholderText("New Patient's Primary Contact Email")
        self.new_email_input.setStyleSheet( """color: red;                    
            font-family: "Courier New";
            font-size: 14pt;
                                    """
        )

        self.new_address_input = QLineEdit(self)
        self.new_address_input.setPlaceholderText("New Patient's Primary Address")
        self.new_address_input.setStyleSheet( """color: red;                    
            font-family: "Courier New";
            font-size: 14pt;
                                    """
        )

        self.layout.addWidget(self.new_phn_input)
        self.layout.addWidget(self.new_name_input)
        self.layout.addWidget(self.new_birth_date_input)
        self.layout.addWidget(self.new_phone_input)
        self.layout.addWidget(self.new_email_input)
        self.layout.addWidget(self.new_address_input)

        self.create_new_patient_button = QPushButton("Update Patient details")
        self.create_new_patient_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.create_new_patient_button)
        self.create_new_patient_button.clicked.connect(self.handle_patient_update)


        self.diff_patient_button = QPushButton("Update a Different Patient")
        self.diff_patient_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.diff_patient_button)
        self.diff_patient_button.clicked.connect(self.show_update_patient_menu)
        self.show_main_menu_button()
        
    
    def handle_patient_update(self):
        reply = QMessageBox.question( # this creates a reply box, this ensure that the user does not update the wrong patient on accident, it shows the name and gives them a chance to decline if wrong
            self, "Action Required!", f"Are You Sure You Want To Update {self.name_cur}'s File",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No # default to no otherwise
        )
        if reply == QMessageBox.StandardButton.No: # if they found the details were wrong and they want someone else to update, simply return to last screen when no is hit
            return
        try: 
            if self.new_phn_input.text() == "": # if the input if blank then use the old value as no update data given
                new_phn_value = self.phn_cur
            elif not self.new_phn_input.text().isdigit(): # if data is given to us to update with, but the data is not formatted as required then decline it and prompt them to enter it again
                QMessageBox.warning(self, "Creation Failed", "PHN Must Be Digits")
                return
            else: # if its not blank and it has the correct format we will proceed to update information as requested using their new input
                new_phn_value = self.new_phn_input.text()

            if self.new_name_input.text().strip() == "":
                new_name_value = self.name_cur
            elif self.new_name_input.text().isdigit():
                QMessageBox.warning(self, "Creation Failed", "Name Must Not Contain Any Digits")
                return
            else:
                new_name_value = self.new_name_input.text()

            if self.new_birth_date_input.text().strip() == "": 
                new_birth_date_value = self.birth_date_cur
            elif not self.validate(self.new_birth_date_input.text()): # same idea as rest, in that it checks the format just has to make a call to validate becuase it is date formatting which is complex
                QMessageBox.warning(self, "Creation Failed", "Birth Date wrong")
                return
            else:
                new_birth_date_value = self.new_birth_date_input.text()

            if self.new_phone_input.text().strip() == "": # if blank use old value
                new_phone_value = self.phone_cur
            else:
                phone_number_value_no_space = self.new_phone_input.text().replace(" ","") # if not blank then we want to remove any spaces so they don't mess with testing
                if not phone_number_value_no_space.isdigit(): # now test the no space value for proper format (aka all digits) and if it's false (not true) raise a warning
                    QMessageBox.warning(self, "Creation Failed", "Phone Number Must Be Digits And Contain No Spaces")
                    return
                else: # if everything is in order format wise then update the phone to the new information given by the user
                    new_phone_value = self.new_phone_input.text().strip()
            new_email_value = self.new_email_input.text() if self.new_email_input.text().strip() != "" else self.email_cur # checks if email is updated and if yes use new one (as long as not blank) else keep same
            new_address_value = self.new_address_input.text() if self.new_address_input.text().strip() != "" else self.address_cur # same idea as line above just with address
            self.controller.update_patient(self.phn_cur, new_phn_value,new_name_value,new_birth_date_value,new_phone_value,new_email_value,new_address_value) # feed all updated fields to the update_patient in controller
            QMessageBox.information(self, "Patient Updated", "Patient New Information Has Been Registered")
            self.show_update_patient_menu()
        except IllegalOperationException:
            QMessageBox.warning(self, "Update Failed", "New PHN Given Is Already Registered, Please Enter A Valid PHN")



    def show_delete_old_patient_box(self):

        #once delete patient is clicked, show delete patient menu

        self.clear_layout()                     #makes sure no unwanted widgets are opened

        #phn input
        self.phn_old_input = QLineEdit(self)
        self.phn_old_input.setPlaceholderText("Patient's Personal Health Number")
        self.phn_old_input.setStyleSheet("""color: red;                    
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.phn_old_input)   #add phn input to the window

        #delete patient button
        self.delete_new_patient_button = QPushButton("Delete Patient")
        self.delete_new_patient_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.delete_new_patient_button)   #add delete patient button to window
        self.delete_new_patient_button.clicked.connect(self.handle_delete_patient)  #if delete patient button is clicked, call delete patient
        self.show_main_menu_button()            #show main menu button if patient wants to return to main menu
        
    def handle_delete_patient(self): # add condition to confirm deletetion before deleting

        #handles deleting the patient once delete patient button is clicked

        phn_old = self.phn_old_input.text().strip()         #phn to be deleted
        patient = self.controller.search_patient(phn_old)   #finds patient to be deleted and assigns it to patient by
        if patient is None:
            #if patient is none, enter a valid phn
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid PHN")
            return
        reply_delete = QMessageBox.question(
            #shows a pop up with question if user wants to delete patient or not
            self, "Action Required!", f"Are you sure you want to Delete {patient.name}?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No # default to no otherwise
        )
        if reply_delete == QMessageBox.StandardButton.No:   #if no don't delete patient 
            return
        phn_old = self.phn_old_input.text()
        self.controller.delete_patient(phn_old)             #calls delete patient from controller with phn given
        QMessageBox.information(self, "Old Patient Deleted", "Old Patient Deleted Successfully")    #shows if patient has been deleted successfully
        self.show_delete_old_patient_box()                  #go back to delete patient menu

    def show_list_patients(self):

        #lists all the patients

        self.clear_layout()                                         #makes sure no unwanted widgets are opened
        patients = self.controller.list_patients()                  #call list patients from controller and assign to patient                
        model = QStandardItemModel()                                #create a QStandardItemModel named model
        model.setHorizontalHeaderLabels(["PHN","Name","D.O.B","Phone#", "Email","Address"])     #set horizontal header labels
        for patient in patients:                     #go through every patient in patients, which is returned from list notes in controller
            phn_item = QStandardItem(patient.phn)
            name_item = QStandardItem(patient.name)
            dob_item = QStandardItem(patient.birth_date)
            phone_item = QStandardItem(patient.phone)
            email_item = QStandardItem(patient.email)
            address_item = QStandardItem(patient.address)
            model.appendRow([phn_item, name_item, dob_item, phone_item, email_item, address_item])
            #create and append patients
        self.table_view = QTableView()          #create a table view
        self.table_view.setModel(model)         #connect model to table view
        header = self.table_view.horizontalHeader()     #get header of table
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch) #make sure columns automatially resize to evenly fit available space
        self.layout.addWidget(self.table_view)      #add the table to the window
        self.show_main_menu_button()        #show main menu button if patient wants to return to main menu
        
    

    
    
    
    
    
    
    def show_start_appointment_menu(self):

        #shows the menu before user starts an appointment

        self.clear_layout()                             #makes sure no unwanted widgets are opened
        
        #phn input to start appointment
        self.phn_input = QLineEdit(self)    
        self.phn_input.setPlaceholderText("Patient's PHN To Start Appointment")
        self.phn_input.setStyleSheet("""color: red;                    
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.phn_input)   #add phn input to window

        #start appointment button
        self.start_appointment_button = QPushButton("Search patient by PHN")
        self.start_appointment_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.start_appointment_button) #add start appointment button to window
        self.start_appointment_button.clicked.connect(self.handle_start_appointment)    #if clicked, call handle start appointment

        self.show_main_menu_button()           #show main menu button if patient wants to return to main menu

    def handle_start_appointment(self):

        #starts the appointment once start appointment button has been clicked

        phn_value = self.phn_input.text()           #phn input
        patient = self.controller.search_patient(phn_value)     #calls search patient from controller and assigns to patient
        if patient is None:
            #if patient is none, please enter valid phn
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid PHN")
            return
        self.name_of_cur = patient.name               #current patient name
        patient = self.controller.set_current_patient(phn_value)        #sets the current patient according to given phn
        self.show_notes_menu()                      #show notes menu button if patient wants to return to notes menu

    def show_end_appointment(self):

        #ends the appointment

        self.clear_layout()
        self.controller.unset_current_patient()                     #unsets the correct patient
        QMessageBox.information(self, "Appointment Ended", "Appointment Ended Successfully")            
        self.show_main_menu()                       #show main menu button if patient wants to return to main menu

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def show_create_note_box(self):

        #window that appears when create new note button is pressed 
        #allows patient to create a new note

        self.clear_layout()                                         #makes sure no unwanted widgets are opened
        self.note_editor = QPlainTextEdit(self)                     #make text box to input note
        self.note_editor.setPlaceholderText("Enter Notes here")     #placeholder text
        self.layout.addWidget(self.note_editor)                     #add note editor to window

        #create new note button
        self.create_new_note_button = QPushButton("Save Note")
        self.create_new_note_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.create_new_note_button)      #add create note button to window
        self.create_new_note_button.clicked.connect(self.handle_create_new_note)    #if clicked, call handle create new note
        self.show_note_menu_button()                            #show button to return to notes menu

    def handle_create_new_note(self):

        #handles creating new note once new note button is clicked

        self.saved_note = self.note_editor.toPlainText()        #convert inputted note text to text
        self.controller.create_note(self.saved_note)            #call create note in controller with saved note
        QMessageBox.information(self, "Note Created", f"Note Has Been Created For {self.name_of_cur} Successfully")
    
    
    def show_retrieve_notes_box(self):

        #window that appears when retrieve existing notes button is pressed 
        #retrieves every note with the inputted text

        self.clear_layout()                                             #makes sure no unwanted widgets are opened

        #note keyword input
        self.note_fetch_input = QLineEdit(self)                         
        self.note_fetch_input.setPlaceholderText("Type Text From Note(s) Here:")
        self.note_fetch_input.setStyleSheet("""
            color: black;                    
            font-family: "Courier New";
            font-size: 20pt; """
        )
        self.layout.addWidget(self.note_fetch_input)    #add note keyword input to window

        #fetch notes button
        self.fetch_notes_button = QPushButton("Fetch Notes")
        self.fetch_notes_button.setStyleSheet( """background-color: red;
            color: black;                    
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.fetch_notes_button)  #add fetch notes button to window
        self.fetch_notes_button.clicked.connect(self.handle_retrieve_notes)     #if clicked, call handle retrieve notes
        self.show_note_menu_button()                    #show button to return to notes menu



    def handle_retrieve_notes(self):

        #handles retrieve notes once fetch notes button is clicked

        search_text = self.note_fetch_input.text().strip()          #assigns inputted keyword to search text
        matching_notes = self.controller.retrieve_notes(search_text)        #calls retrieve notes from controller
        if not matching_notes:      
            #if matching notes does not exist, return
            QMessageBox.information(self, "No Matchs", "No Notes For This Patient Contain Entered Text")
            return
        self.clear_layout()                     #makes sure no unwanted widgets are opened

        combined_notes = "\n\n---\n\n".join([f"Note index: {note.index}\nNote # {note.index}, from {note.timestamp}\n{note.text}" for note in matching_notes])
        #formats and merges notes into one string, using "\n\n---\n\n" to seperate them

        self.note_editor = QPlainTextEdit()                     #creates QPlainTextEdit and assigns it to note editor
        self.note_editor.setPlainText(combined_notes)           #makes the contents of note editor to the combined notes string
        self.note_editor.setReadOnly(True)                      #make it read only
        self.layout.addWidget(self.note_editor)                 #add note editor to window

        #fetch new note button
        self.fetch_new_notes_button = QPushButton("Fetch New Notes")
        self.fetch_new_notes_button.setStyleSheet( """background-color: red;
            color: black;                    
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.fetch_new_notes_button)  #add fetch new note button to window
        self.fetch_new_notes_button.clicked.connect(self.show_retrieve_notes_box)   #if clicked, call show retrieve notes box
        self.show_note_menu_button()                        #show button to return to notes menu
        
    def show_update_note(self):

        #window that opens up when update note button is pressed
        #allows the user to input the index of the note to be updated

        self.clear_layout()                             #makes sure no unwanted widgets are opened

        #index for update note input
        self.update_note_index_input = QLineEdit(self)  
        self.update_note_index_input.setPlaceholderText("Note Index To Be Updated")
        self.update_note_index_input.setStyleSheet("""color: red;                    
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.update_note_index_input) #add index for update note input to window

        #update note button
        self.update_note_button = QPushButton("Update Note")
        self.update_note_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.update_note_button)  #add update note button to window
        self.update_note_button.clicked.connect(self.handle_update_note)        #if clicked, call handle update note
        self.show_note_menu_button()                    #show button to return  to note menu
   
    def handle_update_note(self):
        
        #handles updating the notes
        
        self.clear_layout()                     #makes sure no unwanted widgets are opened

        note_index = self.update_note_index_input.text().strip()        #gets the note index from input
        if not note_index.isdigit():
            #if index is not a digit, please enter an index
            QMessageBox.warning(self, "Invalid Input", "Please enter an Index")
            self.show_update_note()
            return
        note_index = int(note_index)            #convert the note index from string to int
        update_note = self.controller.search_note(note_index)           #call search note from controller with note index
        if update_note is None:
            #if note index does not exist, enter a valid index
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid Index")
            self.show_update_note()
            return
        self.display_update_note_content(update_note)           #if index is valid, call display update note content
        
    def display_update_note_content(self, note):

        #displays the text of the note that is to be updated
        #user is free to change the text

        self.clear_layout()             #makes sure no unwanted widgets are opened

        self.note_text_input = QTextEdit(note.text)         #creates QTextEdit with contents of note.text and assigns it to note text input
        self.layout.addWidget(self.note_text_input)         #adds it to the window

        #save changes button
        self.save_button = QPushButton("Save Changes")
        self.save_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.save_button)     #add save changes button to window
        self.save_button.clicked.connect(lambda:self.save_note_button(note))        #if clicked calls lambda function, which calls save note button  
        self.show_note_menu_button()                     #show button to return  to note menu
    
    def save_note_button(self, note):

        #saves the note after the user finishes editing it

        updated_text = self.note_text_input.toPlainText().strip()       #converts the updated note text to string
        if not updated_text:
            #if note is empty, it cannot be
            QMessageBox.warning(self, "Invalid Input", "Note Cannot Be Empty")
            return
        reply = QMessageBox.question(
            #shows a pop up with question if user wants to update note or not
            self, "Action Required!", f"Are you sure you want to Update {updated_text}?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No # default to no otherwise
        )
        if reply == QMessageBox.StandardButton.No:      #if no dont update note
            return
        note.text = updated_text                        #assign updated text to note.text
        confirmed = self.controller.update_note(note.index, note.text)      #calls update note in controller and assigns it to confirmed
        if confirmed: 
            #if note is updated, show pop up and return to menu
            QMessageBox.information(self, "Success", "Note Updated Successfully")
            self.show_notes_menu()
        else:
            #failed to update note
            QMessageBox.critical(self, "Error", "Failed To Update The Note")

    def show_delete_notes(self):

        #window that appears when delete note button is pressed

        self.clear_layout()                                     #makes sure no unwanted widgets are opened

        #note index input
        self.note_index_input = QLineEdit(self)
        self.note_index_input.setPlaceholderText("Note Index To Be Deleted")
        self.note_index_input.setStyleSheet("""color: red;                    
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.note_index_input) #add note index input to window

        #delete note button
        self.delete_new_note_button = QPushButton("Delete Note")
        self.delete_new_note_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.delete_new_note_button)          #add delete note button to window
        self.delete_new_note_button.clicked.connect(self.handle_delete_notes)       #if clicked, call handle delete note
        self.show_note_menu_button()                 #show button to return  to note menu

    def handle_delete_notes(self):

        #handles deleting the note with given index

        self.clear_layout()                                         #makes sure no unwanted widgets are opened

        note_index = self.note_index_input.text().strip()           #converts the index to string
       
        if not note_index.isdigit():
            #if not a number, please enter an index
            QMessageBox.warning(self, "Invalid Input", "Please enter an Index")
            self.show_delete_notes()
            return
        note_index = int(note_index)                    #converts the note index from string to int
        
        deleted_note = self.controller.search_note(note_index)              #calls search note in controller with given note index
        
        if deleted_note is None:
            #if deleted note is none, please enter a valid index
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid Index")
            self.show_delete_notes()
            return
        
        reply_delete = QMessageBox.question(
            #shows a pop up with question if user wants to delete note or not
            self, "Action Required!", f"Are you sure you want to Delete {deleted_note.text}?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No # default to no otherwise
        )
        if reply_delete == QMessageBox.StandardButton.No:       #if no dont delete note
            self.show_delete_notes()
            return
        
        self.controller.delete_note(note_index)                 #calls delete note in controller with given note index

        QMessageBox.information(self, "Old Patient Deleted", "Note Deleted Successfully")           #if deleted successfully, show popup
        self.show_notes_menu()                              #show notes menu once deleted             

    def handle_list_patient_record(self):

        #lists all the patients notes

        notes = self.controller.list_notes()            #calls list notes in controller and assigns it to notes
        self.clear_layout()                             #makes sure no unwanted widgets are opened

        notes_final = "\n\n---\n\n".join([f"Note index: {note.index}\nNote # {note.index}, from {note.timestamp}\n{note.text}" for note in notes])
        #formats and merges notes into one string, using "\n\n---\n\n" to seperate them

        self.note_editor = QPlainTextEdit()                     #creates QPlainTextEdit and assigns it to note editor
        self.note_editor.setPlainText(notes_final)           #makes the contents of note editor to the final notes string
        self.note_editor.setReadOnly(True)                      #make it read only
        self.layout.addWidget(self.note_editor)                 #add note editor to window

        self.show_note_menu_button()         #show button to return  to note menu



















    def show_notes_menu(self):

        #shows the patients details and the current appointment information, which is the notes menu

        self.clear_layout()                                             #makes sure no unwanted widgets are opened
        patient = self.controller.get_current_patient()                 #gets the current patient
        if patient is None:
            #if patient is none, enter a valid phn
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid PHN")
            return

        details = (
                f"PHN: {patient.phn}\n"
                f"Name: {patient.name}\n"
                f"D.O.B: {patient.birth_date}\n"
                f"Phone Number: {patient.phone}\n"
                f"Email: {patient.email}\n"
                f"Address: {patient.address}\n"
        )   #holds the current patients details

        patient_label = QLabel(details)             #assign details as a QLabel to patient label 
        patient_label.setStyleSheet("""
        font-family: "Courier New";
        font-size: 20pt;
                                    """)
        patient_label.setWordWrap(True)             #breaks into multiple lines if text is too long
        self.layout.addWidget(patient_label)        #add the patient details on the window
        
        #create new note button
        self.new_note_button = QPushButton("Create New Note")
        self.new_note_button.setStyleSheet(
            """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;                     """
        )
        self.layout.addWidget(self.new_note_button)         #add new note button to window
        self.new_note_button.clicked.connect(self.show_create_note_box)     #if new note button is clicked, call show create note box

        #retrieve notes button
        self.retrieve_notes_button = QPushButton("Retrieve Existing Notes")
        self.retrieve_notes_button.setStyleSheet(
            """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;                     """
        )
        self.layout.addWidget(self.retrieve_notes_button)   #add retrieve notes button to window
        self.retrieve_notes_button.clicked.connect(self.show_retrieve_notes_box) #if retrieve button is clicked, call show retrieve notes box

        #update note button
        self.update_note_button = QPushButton("Update Existing Note")   
        self.update_note_button.setStyleSheet(
            """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;                     """
        )
        self.layout.addWidget(self.update_note_button)      #add update notes button to window
        self.update_note_button.clicked.connect(self.show_update_note)#if update notes button is clicked, call 

        self.delete_note_button = QPushButton("Delete Existing Note")       #delete existing note button
        self.delete_note_button.setStyleSheet(
            """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;                     """
        )
        self.layout.addWidget(self.delete_note_button)          #add delete existing note button to window
        self.delete_note_button.clicked.connect(self.show_delete_notes) #if delete existing note button clicked, call show delete notes

        #list patient record button
        self.list_patient_record_button = QPushButton("List Patient Record")
        self.list_patient_record_button.setStyleSheet(
            """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;                     """
        )
        self.layout.addWidget(self.list_patient_record_button)  #add list patient record button to window
        self.list_patient_record_button.clicked.connect(self.handle_list_patient_record)    #if list patient button is clicked, call handle list patient record

        #end current appointment button
        self.end_appointment_button = QPushButton("End Current Appointment")
        self.end_appointment_button.setStyleSheet(
            """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;                     """
        )
        self.layout.addWidget(self.end_appointment_button)      #add end appointment button to window
        self.end_appointment_button.clicked.connect(self.show_end_appointment)      #if end appointment is clicked, call show end appointment


    def show_main_menu(self):

        #shows the main menu once logged in

        self.clear_layout()                                     #makes sure no unwanted widgets are opened

        #create new patient button
        self.new_patient_button = QPushButton("Create New Patient")
        self.new_patient_button.setStyleSheet(
            """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.new_patient_button)  #add create patient button to window
        self.new_patient_button.clicked.connect(self.show_add_new_patient_box)      #if clicked, call show add new patient box

        #search patient button
        self.search_patient_button = QPushButton("Search Patient")
        self.search_patient_button.setStyleSheet(
            """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.search_patient_button)   #add search patient button to window
        self.search_patient_button.clicked.connect(self.show_search_patient_box)    #if clicked, call show search patient box
        
        #retrieve patients button
        self.retrieve_patients_button = QPushButton("Retrieve Patients by Name")
        self.retrieve_patients_button.setStyleSheet(
            """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.retrieve_patients_button)    #add retrieve patient button to window
        self.retrieve_patients_button.clicked.connect(self.show_retrieve_patients_box)  #if clicked, call show retrieve patients box
        
        #update patient button
        self.update_patient_button = QPushButton("Change Patient Data")
        self.update_patient_button.setStyleSheet(
            """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.update_patient_button)   #add update patient button to window
        self.update_patient_button.clicked.connect(self.show_update_patient_menu)   #if clicked, call show update_patient_menu

        #delete patient button
        self.delete_patient_button = QPushButton("Remove Patient")
        self.delete_patient_button.setStyleSheet(
            """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.delete_patient_button)   #add delete patient button to window
        self.delete_patient_button.clicked.connect(self.show_delete_old_patient_box)        #if clicked, call show delete old patient box

        #list all patients button
        self.list_patients_button = QPushButton("List All Patient")
        self.list_patients_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.list_patients_button)    #add list patient button to windiw
        self.list_patients_button.clicked.connect(self.show_list_patients)  #if clicked call show list patients

        #start appointment with patient button
        self.start_appointment_button = QPushButton("Start Appointment With Patient")
        self.start_appointment_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.start_appointment_button)        #add start appointment button to window
        self.start_appointment_button.clicked.connect(self.show_start_appointment_menu) #if clicked, call show start appointment menu
        
        #logout button
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.logout_button)   #add logout button to window
        self.logout_button.clicked.connect(self.handle_logout)      #if clicked, call handle logout








    def validate(self, date):
        
        #makes sure the date is valid and is in the correct format 
        
        try:
            if date != datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d'): #if date is invalid or in the wrong format, raise ValueError
                raise ValueError
            return True #return true if valid
        except ValueError:
            return False    #return false if not
        
    def clear_layout(self):

    #makes sure no unwanted widgets are opened

        for i in reversed(range(self.layout.count())): 
             self.layout.itemAt(i).widget().setParent(None)

    def show_note_menu_button(self):

        #button such that when it is clicked, it shows the notes menu

        #note menu button
        self.note_menu_button = QPushButton("Appointment Menu")
        self.note_menu_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.note_menu_button)        #add note menu button to window
        self.note_menu_button.clicked.connect(self.show_notes_menu)     #if note menu button is clicked, call show notes menu

    def show_main_menu_button(self):

        #button such that when it is clicked, it shows the main menu

        #main menu button
        self.main_menu_button = QPushButton("Main Menu")
        self.main_menu_button.setStyleSheet(
        """background-color: red; color: black;
            font-family: "Courier New";
            font-size: 20pt;
                                    """
        )
        self.layout.addWidget(self.main_menu_button)        #add main menu to button
        self.main_menu_button.clicked.connect(self.show_main_menu)          #when main menu button is clicked, call show main menu



def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
