from GraphicInterface import GraphicInteface
from WorkInterface import WorkInterface
import tkinter as tk

class TopL(GraphicInteface):
    """[summary]

    Args:
        GraphicInteface ([type]): [description]
    """

    def __init__(self, title, geometry, resize, bg, window):

        super().__init__(title, geometry, resize, bg, window)
        self.workInterface = WorkInterface()        


    def setMainFrame(self):
        """It will set the topLevel mainFrame """

        self.mainFrame = tk.Frame(self.window, bd = 3, relief="sunken")
        self.mainFrame.pack(fill = "both", expand = "yes", padx=15, pady=15)

    
    def setDataForm(self):
        """It will set the contacts Form to fill information about new contacts, update their info
            or just view their info. The function is gonna generate the different entries and labels
            necessary for the user.
        """

        self.nameLabel = tk.Label(self.mainFrame, text = "Name:", anchor="nw")
        self.lastNameLabel = tk.Label(self.mainFrame, text = "Last Name:", anchor="nw")
        self.phoneNumberLabel = tk.Label(self.mainFrame, text="Phone Number:", anchor="nw")
        self.emaiLabel = tk.Label(self.mainFrame, text = "Email:", anchor="nw")

        self.nameLabel.grid(row = 0, column = 0, pady = 15, padx=10)
        self.nameEntry = tk.Entry(self.mainFrame, width=30)
        self.nameEntry.grid(row = 0, column = 1) 
        
        self.lastNameLabel.grid(row = 1, column = 0, padx=10)
        self.lastnameEntry = tk.Entry(self.mainFrame, width=30)
        self.lastnameEntry.grid(row = 1, column = 1) 

        self.phoneNumberLabel.grid(row = 2, column=0, pady = 15, padx = 10)
        self.phoneNumberEntry = tk.Entry(self.mainFrame, width=30)
        self.phoneNumberEntry.grid(row = 2, column = 1) 

        self.emaiLabel.grid(row = 3, column = 0, padx = 10)
        self.emailEntry = tk.Entry(self.mainFrame, width=30)
        self.emailEntry.grid(row = 3, column = 1) 


    def setAddContactButtons(self, refresh):
        """It will set the necessary buttons so the user can add a new contact
            and save in the database.

        Args:
            refresh (function): [It's a callback function, but it's sent as parameter here just
                                to send it to another function]
        """

        self.buttonAdd = tk.Button(self.mainFrame, text = "Add Contact", width=15, cursor="hand2", 
                                    command=lambda: self.workInterface.sendNewContactData(self.nameEntry.get(), 
                                    self.lastnameEntry.get(), self.phoneNumberEntry.get(), self.emailEntry.get(), 
                                    self.window, refresh))

        self.buttonAdd.grid(row = 4, column = 0, columnspan=2 , pady = (45, 10))

        self.buttonCancel = tk.Button(self.mainFrame, text = "Cancel", width=15, cursor="hand2", 
                                    
                                    command = self.window.destroy)
        self.buttonCancel.grid(row = 5, columnspan=2)  


    def setContactInfo(self, data):
        """[It will set the the contact Info in the topLevel. 
            All contact data will be visible]

        Args:
            data (list): [it's a list containing all the contact data to set in the toplevel]
        """

        data = [data[x] if data[x] != None else "" for x in range(len(data))]

        self.setDataForm()

        self.nameEntry.insert(0, data[1])
        self.nameEntry.config(state="readonly")
        self.lastnameEntry.insert(0, data[2])
        self.lastnameEntry.config(state="readonly")
        self.phoneNumberEntry.insert(0, data[3])
        self.phoneNumberEntry.config(state="readonly")
        self.emailEntry.insert(0, data[4])
        self.emailEntry.config(state="readonly")


    def setUpdateContactButtons(self, id, refresh):
        """
            In case the user needs to update or delete any contact information, these buttons will ve 
            visible in the window. This sets the button in the window.

        Args:
            id (int): [The contact key to update or delete]
            refresh (function): [It's a callback function, but it's sent as parameter here just
                                to send it to another function]
        """

        self.updateContact = tk.Button(self.mainFrame, text = "Update Data", width=15, cursor="hand2", 
                                        command = lambda: self._setUpdateContactInfoButtons(id, refresh))

        self.updateContact.grid(row = 4, column = 0, columnspan=2 , pady = (45, 10))
        
        self.deleteContact = tk.Button(self.mainFrame, text = "Delete Contact", width=15, cursor="hand2", 
                                        command= lambda: self.workInterface.Deletecontact(id, refresh, self.window))
        
        self.deleteContact.grid(row = 5, columnspan=2, pady = (0, 10))

        self.buttonCancel = tk.Button(self.mainFrame, text = "Cancel", width=15, cursor="hand2", 
                                        command = self.window.destroy)
        
        self.buttonCancel.grid(row = 6, columnspan=2)  


    def _setUpdateContactInfoButtons(self, id, refresh):
        """ In case the user has pressed the button to update the contact
            this function is gonna make visible one button to save the new information
            in the database.

        Args:
            id (int): [the key contact to update informaction]
            refresh (function): [It's a callback function, but it's sent as parameter here just
                                to send it to another function]
        """
        
        self.returned = False
        self.updateContact.grid_forget()
        self.deleteContact.grid_forget()
        self.nameEntry.config(state="normal")
        self.lastnameEntry.config(state="normal")
        self.phoneNumberEntry.config(state="normal")
        self.emailEntry.config(state="normal")

        self.updateContactInfo = tk.Button(self.mainFrame, text = "Save new Data", width=15, cursor="hand2",
                                    command = lambda: self.workInterface.UpdateContactInfo(["contact_Name", "last_Name", "Phone_Number", "Email"],
                                    [self.nameEntry.get(), self.lastnameEntry.get(), self.phoneNumberEntry.get(), 
                                    self.emailEntry.get()], id, refresh, self.window))
        
        self.updateContactInfo.grid(row = 4, column = 0, columnspan=2 , pady = (45, 10)) 