from Tkinter import *
import colorservices as cs

class test(Toplevel):
    
    def __init__(self, root = None):
        Toplevel.__init__(self, root)
        self.hue = 180
        self.sat = 50
        self.val = 50
        self.bind("<Right>", self.on_arrow_key)
        self.bind("<Left>", self.on_arrow_key)
        self.bind("<Up>", self.on_arrow_key)
        self.bind("<Down>", self.on_arrow_key)
        self.bind("<Control-Right>", self.on_control_arrow)
        self.bind("<Control-Left>", self.on_control_arrow)
        self.local_hue = 0
        self.local_val = 0
        
    def on_control_arrow(self,  event):
        "helper for changing value of swatch color"
        key = event.keysym
        if key == "Right":
            self.on_arrow_key("Control-Right")
        if key == "Left":
            self.on_arrow_key("Control-Left")

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
        print self.local_hue,  self.local_val
        print "key",  key,    self.hue , self.sat , self.val
        self.set_color((self.hue , self.sat , self.val))
        
    def set_color(self, arg):
        if isinstance(arg, Event): #ie an event
            canv, item = self.get_canvas_item(arg)
            color = canv.itemcget(item, 'fill')
        elif isinstance(arg, tuple):
            color = cs.getRGB(arg)
        else:
            color = arg
#        if color:
        color = color.upper()
        cs.getHSV(color)
        if self.val < 60:
            text_color = '#FFFFFF'
        else:
            text_color = '#000000'
        self.config(bg = color)


root = Tk()
root.withdraw()
test()
root.mainloop()
