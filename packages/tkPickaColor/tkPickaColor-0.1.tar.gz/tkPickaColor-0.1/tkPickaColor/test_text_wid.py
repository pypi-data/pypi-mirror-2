from Tkinter import  *
from ScrolledText import ScrolledText
from tkinterhelpers import MenuMaker

class TextWidget(Toplevel):
    def __init__(self, root = None, _text=""):
        Toplevel.__init__(self, root = root)
        self.title("Notes")
        self.t=ScrolledText(self,  bg = "#F6FF76")
        self.t.pack()
        self.notes()
        
    def notes(self):
        notes = open("../README.txt",  "r")
        self.load_text(notes)
        
    def load_text(self,  file):
        for line in file:
            self.t.insert(END,line)

root = Tk()
root.withdraw()
Notes()
root.mainloop()
