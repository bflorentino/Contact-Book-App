import tkinter as tk
from MainInterface import MainInterface

def main():

    if __name__ == "__main__":

        root = tk.Tk()

        window = MainInterface("Phone Book", "418x650", False, "#FAFAFA", root)
        window.setMainLabel() 
        window.setOptionsButtons()
        window.setContactsFrame()
        window.setContactsInfoFrame()

        root.mainloop()

main()