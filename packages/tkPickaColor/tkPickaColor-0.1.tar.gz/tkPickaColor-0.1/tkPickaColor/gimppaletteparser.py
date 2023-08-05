from palettebuilder import DrawPalette
from Tkinter import *
import re, os.path
import shutil

class GimpPaletteParser(object):
    def __call__(self, gimp_file_path):
        try:
            gimp_file = open(gimp_file_path)
            #-- shutil.copy(gimp_file_path, os.path.join(gimp_file_path, ".bak")
        except IOError:
            return None, None, None
        return self.parse(gimp_file)

    def get_last(self, line):    
        pos = line.find(":")
        return line[pos + 1:].strip()

    def parse(self, gimp_file):
        name = ''
        columns = 0
        for line in gimp_file:
            line = line.strip()
            if line.startswith('Name'):
                name = self.get_last(line)
                continue
            if line.upper().startswith('COLUMNS'):
                columns = int(self.get_last(line))
                continue
            if line.startswith("#"):
                break
        if columns == '' or columns == 0:
            columns = 16
        colors = []
        pieces = []
        for line  in gimp_file :
            line = line.strip()
            if line.startswith('#'):
                continue
            if  len(line.strip())<= 0:
                break
            if line.strip() == "mt":
                rgb = ""
            else:
                pieces = (re.split("\W+",  line.strip()))
                r, g, b = pieces[0:3]
                rgb =  '#%02x%02x%02x' % (int(r), int(g), int(b))
            colors.append(rgb)
        return name, columns, colors

if __name__=="__main__":
    
    #gimp_file = './Default.gpl'
#    gimp_file = './Reds_And_Purples.gpl'
#    gimp_file = './Visibone_2.gpl'
#    gimp_file = './resources/Greens.gpl'
    gimp_file = "/home/steve/favs.gpl"
#    gimp_file = './Tango.gpl'

    pgf = GimpPaletteParser()
    name,  columns,  colors = pgf(gimp_file)
    root = Tk()
    canv = Canvas(root,  height = 400)
    canv.pack()
    DrawPalette(canv, colors, name, columns)
    root.mainloop()
