'''
tkPickaColor provides a Tkinter dialog to find and return one or more strings
for colors in the "#FFFFFF" format.

from tkPickaColor import tkpickacolor
...
result = tkpickacolor.askColors()
'''
__author__ = "Steve Solomon"
__license__ = "GPLv3"
__version__ = "0.1.0"
__email__ = "codeduffer@gmail.com"
__status__ = "Beta"

from defaultvalues import *
from Tkinter import *
from colorservices import *
from palettebuilder import HarmonyPalettes, DrawPalette
from gimppaletteparser import GimpPaletteParser
from tkinterhelpers  import MenuMaker
from textwidget import DisplayText
import tkFont
import re, os, os.path
import pdb

class PickaColor(Toplevel):
    def __init__(self, color_list = [], root = None):
        Toplevel.__init__(self, root)
        base_dir =  os.path.split(__file__)[0]
        self.ini_dir = self.get_ini_dir()
        self.color_list = color_list
        self.set_menu_items()
        self.spect_foto = PhotoImage(file = os.path.join(base_dir,'resources/spectrum.gif'))
        self.values_foto = PhotoImage(file = os.path.join(base_dir,'resources/grayvalues.gif'))
        self.config(bg = BASE_COLOR)
        self.copied_color = ""
        self.hue = self.sat = self.val = 100
        self.num_chips = 8
        self.make_widgets()
        HarmonyPalettes(self.canv, "#3D3DFF")
        self.focus_set()
        self.grab_set()
        self.wait_window()

    def get_ini_dir(self):
        "user configuration files"
        ini_dir = os.path.expanduser("~/.tkpacini")
        if not os.path.exists(ini_dir):
            os.mkdir(ini_dir)
        return ini_dir

    def set_menu_items(self):
        self.menuItems = [
            ('OK', 0, self.on_ok),
            ('Quit', 0, self.on_quit),
            ('Favorites', 0, [
                ('Tidy', 0, self.tidy_favorites),
                ('Save', 0, self.save_favorites),
                ('Delete all', 0, self.delete_all_favs),
                ('Reload', 0, self.reload_favs)
                 ]), 
            ('Cheat Sheet', 1,  self.display_help_notes)
                 ]

    def make_widgets(self):
        self.local_hue = 0
        self.local_val = 0
        self.title("TkPickAColor")
        mm = MenuMaker()
        mm.menuMaker(self, self.menuItems)
        self.bind("<Alt-KeyPress-t>", self.tidy_favorites)
        self.bind("<Alt-KeyPress-T>", self.tidy_favorites)
        self.bind("<Alt-KeyPress-d>", self.delete_all_favs)
        self.bind("<Alt-KeyPress-D>", self.delete_all_favs)
        self.bind("<Alt-KeyPress-c>", self.swatch_to_chip) # paste swatch color into chips
        self.bind("<Alt-KeyPress-C>", self.swatch_to_chip)
        self.bind("<Alt-KeyPress-p>", self.swatch_to_palette) # paste swatch color to 
        self.bind("<Alt-KeyPress-P>", self.swatch_to_palette)
        self.bind_arrows()

        self.border = 20
        self.color_var = StringVar()

        # Palette canvas
        self.canv = Canvas(self, height = 100, width = 50, bg = BASE_COLOR)
        self.canv.grid(row = 0, column = 3, rowspan = 4, sticky = N + S)
        self.canv.bind("<Button-1>" , self.add_rgb_to_chip)
        self.canv.bind("<Button-3>" , self.set_swatch_color)
        self.canv.bind("<Control-Button-1 >", self.save_rgb_to_paste)

        frame_graphics = Frame(self, bg = BASE_COLOR)
        frame_graphics.grid(column = 0, row = 0, sticky = N)

        # Spectrum selector
        self.spectrum = Label(frame_graphics, bg = BASE_COLOR,
                width = self.spect_foto.width() + self.border,
                height = self.spect_foto.height() + self.border,
                image = self.spect_foto)
        self.spectrum.grid(row = 0, column = 0, sticky = N)
        self.spectrum.bind('<B1-Motion>', self.on_spect_motion)

        # Value selector
        self.values = Label(frame_graphics, bg = BASE_COLOR,
                  width = self.values_foto.width() + self.border,
                  height = self.values_foto.height() + self.border,
                  image = self.values_foto) #values graphic
        self.values.grid(row = 1, column = 0, sticky = N)
        self.values.bind('<B1-Motion>', self.on_values_motion)

        #Swatch - sample color
        frame_swch = Frame(self, bg = BASE_COLOR)
        frame_swch.grid(column = 1, row = 0, sticky = N)
        self.swatch = Label(frame_swch, width = 20, height = 8)
        self.swatch.grid(column = 0, row = 0, sticky = N + E + S + W)
        self.set_swatch_color("#3D3DFF")
        self.swatch.bind("<Control Button-1>", self.save_rgb_to_paste)
        self.swatch.bind("<Button-3>", self.display_array)
        self.swatch.bind("<Button-1>", self.add_chip)

        # Color entry widget
        entry_font = tkFont.Font(size = 11)
        self.color_entry = Entry(frame_swch, bg = '#FFFF66',
                            width = 10,
                            textvariable = self.color_var, font = entry_font)
        self.color_entry.bind("<Enter>", self.on_entry)
        self.color_entry.bind("<Alt E>", self.on_entry)
        self.color_entry.bind("<Return>", self.make_valid)
        self.color_entry.bind("<Leave>", self.on_leave)
#        self.color_entry.config(state = DISABLED)

        self.color_entry.grid(column = 0, row = 1, pady = 10)

        # Favorites
        frame_favs = Frame(self, bg = BASE_COLOR)
        frame_favs.grid(column = 0, row = 1, columnspan = 2)
        self.canv_favs = Canvas(frame_favs, height = 100, width = 550,
                                bg = BASE_COLOR)
        self.canv_favs.grid(column = 0, row = 0, sticky = E + W)
        self.canv_favs.bind("<Button-1>" , self.add_rgb_to_chip)
        self.canv_favs.bind("<Button-3>" , self.set_swatch_color)
        self.canv_favs.bind("<Control Button-3>" , self.delete_a_fav)
        self.canv_favs.bind("<Control Button-1>" , self.add_a_fav)
        self.load_favorites()

        # colors to be returned to client3
        frame_chips = Frame(self, bg = BASE_COLOR)
        frame_chips.grid(column = 0, row = 2, columnspan = 3, sticky = S)
        self.chips = ColorChips(frame_chips, self.num_chips)

    def load_favorites(self, reload = False):
        def tag(ndx):
            return "tag" + str(ndx).rjust(4, "0")
        canvas = self.canv_favs
        canvas.config(bg = BASE_COLOR)
        gpp = GimpPaletteParser()
        fav_file = os.path.join(self.ini_dir, "Favorites.gpl")
        name, columns, colors = gpp(fav_file)
        if not colors:
            colors = []
                # add empty strings ("") to colors to total len of 100
        to_add = ["" for x in range(100 - len(colors))]
        colors.extend(to_add)
        if reload:
            pass
            for ndx, color in enumerate(colors, 1):
                canvas.itemconfig(tag(ndx), fill = color)
        else:
            columns = 25
            DrawPalette(canvas, colors, name, columns, start = (1, 1), tags = True)

    # :::::::::::::::::::::  utilities  :::::::::::::::::::::::::: #
    def bind_arrows(self):
        self.bind("<Control-Right>", self.on_arrow_key)
        self.bind("<Control-Left>", self.on_arrow_key)
        self.bind("<Control-Up>", self.on_arrow_key)
        self.bind("<Control-Down>", self.on_arrow_key)
        self.bind("<Alt-Right>", self.on_control_arrow)
        self.bind("<Alt-Left>", self.on_control_arrow)

    def unbind_arrows(self):
        self.unbind("<Control-Right>")
        self.unbind("<Control-Left>")
        self.unbind("<Control-Up>")
        self.unbind("<Control-Down>")
        self.unbind("<Alt-Right>")
        self.unbind("<Alt-Left>")

    def set_hsv(self, arg):
        "sets self.hue, .sat, & .val"
        #assumes arg is in a correct form
        if isinstance(arg, (tuple, list)): 
            self.hue, self.sat, self.val = arg
            return 1
        elif isinstance(arg,  str):
            self.hue,  self.sat, self.val = getHSV(arg)
            return 1
        else:
            return 0

    # ::::::::::::::::::::: Callbacks :::::::::::::::::::::::::: #

    def on_ok(self):
        self.save_favorites()
        self.color_list.extend(self.chips.return_colors())
        self.destroy()

    def on_quit(self):
        self.destroy()

    def display_help_notes(self):
        DisplayText("./resources/cheatsheet.txt")

    def on_arrow_key(self, event):
        "changing hue, saturation, and value of swatch's color"
        if isinstance(event, str):
            key = event
        else:
            key = event.keysym
        if key == "Right" and self.hue < 360: #+ hue level
            if self.sat == 0: # in weird zone
                self.local_hue += 1
            else:
                self.hue += 1
        elif key == "Control-Right" and self.val < 100: #+ val level
            if self.sat == 0: # in weird zone
                self.local_val += 1
            else:
                self.val += 1
        elif key == "Left" and self.hue > 0:
            if self.sat == 0: # in weird zone
                self.local_hue -= 1
            self.hue -= 1
        elif  key == "Control-Left" and self.val > 0: #+ val level
            if self.sat == 0: # in weird zone
                self.local_val -= 1
            else:
                self.val -= 1
        elif key == "Up" and self.sat > 0:
            if self.sat ==1: # ie almost to the weird zone
                self.local_hue = self.hue  #take snapshot
                self.local_val = self.val
            self.sat -= 1
        elif key == "Down" and self.sat < 100: 
            if self.sat == 0: # ie leaving weird zone
                self.hue = self.local_hue
                self.val = self.local_val
            self.sat += 1
        self.set_swatch_color((self.hue , self.sat , self.val))

    def on_control_arrow(self,  event):
        "helper for changing value of swatch color"
        key = event.keysym
        if key == "Right":
            self.on_arrow_key("Control-Right")
        if key == "Left":
            self.on_arrow_key("Control-Left")

    def swatch_to_chip(self,  event):
        "add swatch color to chips"
        self.chips.add_sample(self.swatch.cget("bg"))

    def swatch_to_palette(self, event):
        HarmonyPalettes(self.canv, self.swatch.cget("bg") )

    #--------- Favorite callbacks  --------------------
    def save_favorites(self):
        c = self.canv_favs
        def tag(num):
            return "tag" + str(num).rjust(4, "0")
        fav_file = os.path.join(self.ini_dir, "Favorites.gpl")
        file = open(fav_file, "w")
        file.write("columns : 25 \n#\n#\n")
        for t in range (1, 100):
            rgb = c.itemcget(tag(t), "fill")
            if rgb == "":
                file.write("mt\n")
            else:
                file.write("%s %s %s\n" % (int(rgb[1:3], 16), int(rgb[3:5], 16),
                                           int(rgb[5:7], 16)))
        file.close()

    def delete_a_fav(self, event):
        "empty the square clicked on favorites"
        canvas, item = self.get_canvas_item(event)
        canvas.itemconfig(item, fill = "")

    def delete_all_favs(self, event = None):
        def tag(ndx):
            return "tag" + str(ndx).rjust(4, "0")
        for id in range(1, 101):
            self.canv_favs.itemconfig(tag(id), fill = "")

    def reload_favs(self, event = None):
        "overwrite current fav display from file"
        self.load_favorites(reload = True)

    def tidy_favorites(self, event = None):
        "move empty (mt) square to the end if the display "
        canvas = self.canv_favs
        mts = []
        for id in range(1, 101):
            color = canvas.itemcget(id, "fill")
            if color: # square has a color
                if len (mts): # i.e. has ids of now mt squares
                    target = mts.pop(0)
                    canvas.itemconfig(target, fill = color)
                    canvas.itemconfig(id, fill = "")
                    mts.append(id)
                else:
                    continue
            else:
                mts.append(id)

    def add_a_fav(self, event):
        "paste a stored color"
        def tag(ndx):
            return "tag" + str(ndx).rjust(4, "0")
            # get fill of target drop-site
        canvas, item = self.get_canvas_item(event)
        target_fill = canvas.itemcget(item, "fill")
        if not target_fill:
            # if target empty
            # just drop in the new color
            canvas.itemconfig(item, fill = self.copied_color)
        else:
            # insert a space by shifting everything to the right
            # starting at end and working backward
            target_tag = canvas.itemcget(item, "tags")[:7]#.strip()
            insert_ndx = int(target_tag[3:7])
            for sqr in range(100, insert_ndx - 1, -1):
                next_color = canvas.itemcget(tag(sqr - 1), "fill")
                canvas.itemconfig(tag(sqr), fill = next_color)
            canvas.itemconfig(target_tag, fill = self.copied_color)

    def save_rgb_to_paste(self, event = None):
        "copy the color of a square"
        wid = event.widget
        if isinstance(wid, Canvas):
            canvas, item = self.get_canvas_item(event)
            self.copied_color = canvas.itemcget(item, "fill")
        else:
            self.copied_color = wid.cget("bg")

    def get_canvas_item(self, event):
        "helper"
        canvas = event.widget
        x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
        return  canvas, canvas.find_closest(x, y)

    #---------------------Spectrum callbacks----------------------------------
    def on_spect_motion(self, event):
        """the x, y coordinates map to the hue (0-360) and saturation (0-100)
            of the HSV color space"""
        eh = event.x - self.border / 2
        es = event.y - self.border / 2
        if eh > 360:
            self.hue = 360
        elif eh < 0:
            self.hue = 0
        else:
            self.hue = eh
        if es > 100:
            self.sat = 100
        elif es < 0:
            self.sat = 0
        else:
            self.sat = es
        val = 100 #??? should it reset to full color??
        color = getRGB((self.hue, self.sat, val))
        txt = 'hue: ' + str(self.hue) + ' sat: ' + str(self.sat) + ' val: ' + str(val)
        self.swatch.config(text = txt, bg = color, fg = '#000000')
        self.color_var.set(color.upper())

    #----------------------Values callbacks -------------------------
    def on_values_motion(self, event):
        "adjusting x-position maps to the 'Value' (0 = 100) of the HSV color space"
        vh = int((event.x - self.border / 2) / 2.55)
        if vh > 100:
            self.val = 100
        elif vh < 0:
            self.val = 0
        else:
            self.val = vh
        self.set_swatch_color((self.hue, self.sat, self.val))

    def add_rgb_to_chip(self, event):
        canv, item = self.get_canvas_item(event)
        color = canv.itemcget(item, 'fill')
        if color: # skip if clicking a empty square in favorites
           self.chips.add_sample(color)

    def set_swatch_color(self, arg):
        "set swatch to color of:an event, color string, or a hvs tuple"
        is_hsv_set = False
        if isinstance(arg, Event): #ie an event
            canv, item = self.get_canvas_item(arg)
            color = canv.itemcget(item, 'fill')
        elif isinstance(arg, tuple):
            color = getRGB(arg)
            is_hsv_set = True
        else:
            color = arg
        color = color.upper()
        if not is_hsv_set:
            self.set_hsv(color)
        if self.val < 60:
            text_color = '#FFFFFF'
        else:
            text_color = '#000000'
        txt = 'hue:' + str(self.hue) + ' sat:' + str(self.sat) + ' val:' + str(self.val)  
        self.swatch.config(bg = color, fg = text_color,  text = txt)
        self.color_var.set(color)

    def display_array(self, event):
        widgt = event.widget
        baseRGB = widgt.cget("bg")
        HarmonyPalettes(self.canv, baseRGB)

    def add_chip(self, event):
        wid = event.widget
        self.chips.add_sample(wid.cget("bg"))

    #-----------------Entry Widget callbacks------------------------
    def on_entry(self, event):
        self.color_entry.config(cursor = "pencil")
        self.temp_color_str = self.color_var.get()
        self.color_entry.selection_range(0, END)
        self.color_entry.icursor(END)
        self.unbind_arrows()

    def on_leave(self, event):
        self.make_valid()
        self.color_entry.selection_range(0, 0)
        self.bind_arrows()

    def make_valid(self, event = None):
        "returns either a valid rgb string or an empty string"
        candidate = self.color_var.get().upper().strip()
        pat = re.compile('[A-F0-9]{6}$')
        if candidate.startswith("#"):
            candidate = candidate[1:]
        _match = pat.match(candidate)
        if _match:
            rtrn = ("#" + candidate)
            self.set_swatch_color(rtrn)
        else:
            rtrn = self.temp_color_str
            self.color_var.set(rtrn)

class ColorChips(object):
    "colors to be returned to client"
    def __init__(self, parent, num_chips = 7):
        self.num_chips = num_chips
        self.return_samples = []
        self.avail_slot = 0
        self.build_widgets(parent)

    def build_widgets(self, parent):
        "display 'blank' chips (labels)"
        for num in range(self.num_chips):
            b = Label(parent, bg = BASE_COLOR, text = "",
                name = str(num), relief = GROOVE, height = 5, width = 8)
            b.grid(row = 2, column = num, sticky = S)#,  pady = 5)
            b.bind("<Button-3>", self.on_right_click) # reverse colors
            b.bind("<Button-1>", self.on_left_click)   # delete color clicked
            self.return_samples.append(b)

    def on_left_click(self, event):
        "move color up|left (swap colors of two neighboring chips)"
        samples = self.return_samples
        numb = len(samples)
        wid = event.widget
        ndx = int(str(wid)[-1:]) # list index of clicked
        if ndx > 0 and ndx < self.avail_slot: # otherwise can't shift any further left, or would shift blank label
            this_item = samples[ndx]
            next_item = samples[ndx - 1]
            this_color = this_item.cget('bg')
            next_color = next_item.cget('bg')
            this_item.config(bg = next_color, text = next_color)
            next_item.config(bg = this_color, text = this_color)

    def on_right_click(self, event):
        "delete a chip's current color and move the next colors up"
        samples = self.return_samples
        stop = self.avail_slot - 1
        last = stop
        wid = event.widget
        ndx = int(str(wid)[-1:])  # list index of clicked
        if ndx < self.avail_slot:
            for i in range(ndx, stop):
                next_color = samples[i + 1].cget('bg')
                samples[i].config(bg = next_color, text = next_color.upper())
            samples[last].config(bg = BASE_COLOR, text = "")
            self.avail_slot -= 1

    def add_sample(self, color):
        color = color.upper()
        samples = self.return_samples
        ln = len(samples)
        if self.avail_slot >= ln: #ie if no open slots delete 1st
            for ndx in range(ln - 1):
                this_item = samples[ndx]
                next_item = samples[ndx + 1]
                next_color = next_item.cget("bg")
                this_item.config(bg = next_color, text = next_color)
            self.avail_slot -= 1
        samples[self.avail_slot].config(bg = color, text = color)
        self.avail_slot += 1

    def return_colors(self):
        clist = []
        if self.avail_slot > 0 :
            for ndx in range(0, self.avail_slot):
                clist.append(self.return_samples[ndx].cget('bg'))
        return clist

def askColors():
    "put a function-face on app"
    color_list = []
    PickaColor(color_list)
    return color_list

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    print askColors()
    root.mainloop()
