from Tkinter import  *
from ScrolledText import ScrolledText
from tkinterhelpers import MenuMaker

class DisplayText(Toplevel):
    "show text widget displaying text from provided file, read-only"
    def __init__(self,  file_name = '',  doc_title = "", root = None,):
        Toplevel.__init__(self, root )
        self.t=ScrolledText(self,  bg = "#F6FF76")
        self.t.pack()
        self.set_menu_items()
        mm = MenuMaker() 
        mm.menuMaker(self, self.menuItems)
        self.load_text(open(file_name,  "r"))
#        if text_name == 'helpnotes':
#            self.notes()
        self.focus_set()
        self.grab_set()
        self.wait_window()

    def set_menu_items(self):
        self.menuItems = [
            ('Quit', 0, self.on_quit)]

    def on_quit(self):
        self.destroy()

    def notes(self):
        self.title("Cheat Sheet")
        notes = open("./resources/cheatsheet.txt",  "r")
        self.load_text(notes)
        
    def load_text(self,  file):
        for line in file:
            self.t.insert(END,line)

if __name__=='__main__':
    root = Tk()
    root.withdraw()
    DisplayText('./resources/cheatsheet.txt')
    root.mainloop()
