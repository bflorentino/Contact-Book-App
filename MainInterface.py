from TopL import TopL
from GraphicInterface import GraphicInteface
from WorkInterface import WorkInterface
import tkinter as tk
from tkinter import ttk


class MainInterface(GraphicInteface):

    def __init__(self, title, geometry, resize, bg, window):
    
        super().__init__(title, geometry, resize, bg, window)
        self.workInterface = WorkInterface()
        self.contactsIds, self.contactsNames, self.contactsLetters, self.contactsPhoneNumbers = self.workInterface.getContactsBasicInfo()
        self.contactsTotal = tk.StringVar(value = str(len(self.contactsIds)) + " contacts")
        self.openCard = tk.BooleanVar(value=False)
        self.openedTopLevel = tk.BooleanVar(value = False)


    def _openTopLevelAddContacts(self):

        topLevel = tk.Toplevel(self.window)
        topLevelAddContacts = TopL("Add New contact", "350x350", False, None, topLevel)
        topLevelAddContacts.setMainFrame()
        topLevelAddContacts.setAddContactButtons(self._refreshData)
        topLevelAddContacts.setDataForm()
        topLevel.focus_set()
        topLevel.grab_set()
        topLevel.wm_transient(master=self.window)
    

    def _openTopLevelViewContact(self, contact_Id):

        topLevel = tk.Toplevel(self.window)
        topLevelViewContacts = TopL("View contact info", "350x350", False, None, topLevel) 
        contactData = self.workInterface.getUniqueContactnfo(contact_Id)
        topLevelViewContacts.setMainFrame()
        topLevelViewContacts.setUpdateContactButtons(contactData[0], self._refreshData)
        topLevelViewContacts.setContactInfo(contactData)
        topLevel.focus_set()
        topLevel.grab_set()
        topLevel.wm_transient(master=self.window)


    def _refreshData(self):

        self.canvas.pack_forget()
        self.scrollbarFrame.pack_forget()
        self.setContactsFrame()
        self.contactsIds, self.contactsNames, self.contactsLetters, self.contactsPhoneNumbers = self.workInterface.getContactsBasicInfo()
        self.contactsTotal.set(str(len(self.contactsIds)) + " contacts")
        self.setContactsInfoFrame()


    def setMainLabel(self):
    
        labelPhoneFrame = tk.Frame(self.window, bg = self.bgColor)
        labelPhoneFrame.pack(pady = 10)
        labelPhone = tk.Label(labelPhoneFrame, text = "Phone Book", font = ("Arial", 20), bg = self.bgColor)
        labelPhone.pack()

        labelTotalContacts = tk.Label(labelPhoneFrame, textvariable = self.contactsTotal,  
                                        font = ("Arial", 12), bg = self.bgColor)

        labelTotalContacts.pack()


    def setOptionsButtons(self):
    
        buttonsOptionFrame = tk.Frame(self.window, bg = self.bgColor)
        buttonsOptionFrame.pack(anchor= "ne")

        addContactButton = tk.Button(buttonsOptionFrame, bg = self.bgColor, text = "+", 
                                    font = ("Arial", 25), bd = 0, cursor= "hand2", 
                                    command = lambda: self._openTopLevelAddContacts())
        
        addContactButton.grid(row = 0, column=0)
        
        moreOptions = tk.Button(buttonsOptionFrame, bg = self.bgColor, text = ":", 
                                font = ("Arial", 25), bd = 0, cursor = "hand2")
        
        moreOptions.grid(row = 0, column = 1)


    def setContactsFrame(self):

        self.scrollbarFrame = tk.Frame(self.window, bg = self.bgColor)
        self.scrollbarFrame.pack(fill = "both", expand = "yes", padx = 10, pady = 10)

        # Create a canvas 
        self.canvas = tk.Canvas(self.scrollbarFrame, bg= self.bgColor)
        self.canvas.pack(side = tk.LEFT, anchor = "nw", fill="y")
        
        # Add a scrollbar to self.canvas 
        scrollbar = ttk.Scrollbar(self.scrollbarFrame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side = tk.RIGHT, fill= "y")
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.allContactsFrame = tk.Frame(self.canvas, bg = self.bgColor)
        self.canvas.create_window((0, 0,), window = self.allContactsFrame, anchor="nw")


    def setContactsInfoFrame(self):
        
        self.contactsButtons = []
        self.contactsinfoFrames = []
        position = 0

        for letter in range(0,len(self.contactsLetters)):

            self.letterFrame = tk.Frame(self.allContactsFrame, bg = self.bgColor, pady = 10)
            self.letterFrame.pack(anchor = "nw")

            self.letter = tk.Label(self.letterFrame, bg = self.bgColor, text = self.contactsLetters[letter], 
                                    font = ("Arial", 15, "bold"), fg = "#706F6F")
            
            self.letter.pack()

            
            for name in range(position, len(self.contactsNames)):
                
                if self.contactsNames[name][0] == self.contactsLetters[letter]:

                    self.contactFrame = tk.Frame(self.allContactsFrame, bg = "white")
                    self.contactFrame.pack(anchor="nw")         
                    
                    self.contactButton = tk.Button(self.contactFrame, text = self.contactsNames[name], 
                                                    anchor = "w", bg = "white", height=3, bd = 0.5, 
                                                    font = ("Arial", 12), width=42, cursor="hand2")
                    
                    self.contactButton.pack(anchor = "nw")
                    self.contactsButtons.append(self.contactButton)

                    self.contactInfo = tk.Frame(self.contactFrame, bg = "white")
                    self.contactsinfoFrames.append(self.contactInfo)

                    self.phoneLabel = tk.Label(self.contactInfo, text = str(self.contactsPhoneNumbers[name]), bg = "white", font = ("Arial", 11))
                    self.phoneLabel.pack(anchor="center", pady = 5)

                    self.viewMoreAboutContact = tk.Button(self.contactInfo, text = "View contact info", bd = 0, height=2, width=15, cursor="hand2", command= lambda id = self.contactsIds[name]: self._openTopLevelViewContact(id))
                    self.viewMoreAboutContact.pack(anchor="center", pady = 10)
                    self.contactButton.config(command = lambda  frame = self.contactInfo: self._intermediaryToShowContactCard(frame))
                
                else:
                    position = name
                    break
        
        self.xtraFrame = tk.Frame(self.allContactsFrame, bg = "white", height=100)
        self.xtraFrame.pack(anchor = "nw")            
    

    def _intermediaryToShowContactCard(self, frame):

        if self.openCard.get() == False:
            self.openFrameContactCard = frame
            self.openCard.set(True)
            self.workInterface.showContactInfoCard(frame, self.openCard.get())

        else:
            self.openCard.set(False)
            self.workInterface.showContactInfoCard(self.openFrameContactCard, self.openCard.get())

            if frame != self.openFrameContactCard:
                self.openCard.set(True)
                self.openFrameContactCard = frame
                self.workInterface.showContactInfoCard(frame, self.openCard.get())