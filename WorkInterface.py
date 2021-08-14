from Database import Database
import tkinter as tk
from tkinter import messagebox
import re

class WorkInterface():
    
    def __init__(self):

        self.database = Database()
        self.contacts = self.database.selectAllContactsName()
        self.contactsNames = [x[1] for x in self.contacts]
        self.contactsPhoneNumbers = [x[2] for x in self.contacts]


    # Top Level Add Contacts Methods     
    _closeWindow = lambda self, win: win.destroy() 
    
    def sendNewContactData(self, name, lastName, phoneNumber, email, window, refresh):
        """ 
        It sends the data to the database so it can be inserted in the table.
        The parameters it receibes are name, lastName, phoneNumber, email, window and refresh.
        The 4 first parameters are the data sent to the database and, 
        the window is sent here, so it can be sent as parameter to a function
        which is going to close the window. Refresh is a callback function to refresh
        the contacts list in the main interface.
        """

        if not name ==  "" and not phoneNumber == "":
            
            phonePattern = re.compile(r'''
            ^\d\d\d- #Area code
            \d\d\d- #First Three digits
            \d\d\d\d$ #Last four digits
            ''', re.VERBOSE)

            correctPhonePattern = phonePattern.search(phoneNumber)

            if lastName == "":
                lastName = None

            if email == "":
                email = None
            else:
                Emailpattern = re.compile(r"^\w+@(gmail|hotmail|outlook)\.com$", re.IGNORECASE)
                correctEmailPattern = Emailpattern.search(email)

                if not correctEmailPattern:
                    email = None

            if correctPhonePattern:

                if self.notRepeated(name, phoneNumber):
                    print(self.contactsNames)
                    
                    Insertion = self.database.insertContactInfo(name, lastName, phoneNumber, email)
    
                    if Insertion:
                        messagebox.showinfo("Data added", "Data added correctly")
                        self._closeWindow(window)
                        refresh()
            
                    else:
                        messagebox.showerror("Connection Error","No connection to database")
                
                else:
                    messagebox.showerror("Repeated data",'The name or the phone number cannot be equal to any in the database''')
                    
            else:
                messagebox.showerror("Incorrect information", "The phone Number added is not valid.\nThe pattern must be ###-###-#### where # is a number")
        
        else:
            messagebox.showerror("Missing data", "Phone Number or Name is not optional.")

        
    # Main Interface Methods 
    def getContactsBasicInfo(self): 
        """ 
            It gets the data from all contacts in the database. Every property is saved
            in a list which is going to save all the corresponding data.
            For example: ContactsIds is gonna get all the ids gotten from the database

        Returns:
            contactsIds, contactsNames, contactsLetters, contactsPhoneNumbers: These are the 
            different properties gotten from the database.
        """
        self.contacts = self.database.selectAllContactsName()
        self.contactsIds = [x[0] for x in self.contacts]
        self.contactsNames = [x[1] for x in self.contacts]
        self.contactsPhoneNumbers = [x[2] for x in self.contacts]
        self.contactsLetters = []
    
        for firstLetter in self.contactsNames:

            if firstLetter[0] not in self.contactsLetters:
                self.contactsLetters.append(firstLetter[0])
        
        return self.contactsIds, self.contactsNames, self.contactsLetters, self.contactsPhoneNumbers


    def showContactInfoCard(self, frame, packFrame):
    
        if packFrame:
            frame.pack()
        else:
            frame.pack_forget()


    def getUniqueContactnfo(self, id):

        return self.database.selectContact(id)           


    def UpdateContactInfo(self, dataToUpdate, newData, id, refresh, window):
        """
            It's gonna update any contact info in the database.
            The received parameters are dataToUpdate(a list with the properties to update),
            newData(a list with the new values of every property to update),
            id(the contact key to the one the changes will be done),
            refresh (a callback function to refresh the contact list in the main interface),
            window(a window which is gonna be closed by the end of the funtion)
        """

        updated = self.database.updateContactInfo(dataToUpdate, newData, id)

        if updated:
            messagebox.showinfo("Data Updated", "The contact data has been updated")
            self._closeWindow(window)
            refresh()
        else:
            messagebox.showerror("No Updated", "The contact data could not be updated")

    
    def Deletecontact(self, id, refresh, window):

        """ It's gonna delete the contact sent by the parameter (id).
            It's gonna call the function to close the window sent as parameter(window)
            and it's going to refresh the main interface contact list by executing the 
            callback function sent as parameter (refresh)
        """

        confirmation =  messagebox.askyesno("Delete Contact", "Are you sure you want to delete this contact from your list?")

        if confirmation:

            deleted =  self.database.deleteContactInfo(id)

            if deleted:
                messagebox.showinfo("Deleted", "Contact deleted")
                self._closeWindow(window)
                refresh()
            else:
                messagebox.showerror("Error", "An error occured and the contact wasn't deleted")
    

    def notRepeated(self, name, phone):
        """It will check if the name or the phone are not repeated in the database

        Args:
            name (string): [The contact name]
            phone (phone)" [The contact phone number]

        Returns:
            [True]: [if neither the name nor the phone number are already in the database]
            [False]: [if either the name nor the phone number are already in the database]
        """

        if (name not in self.contactsNames) and (phone not in self.contactsPhoneNumbers):
            return True
        
        else:
            return False