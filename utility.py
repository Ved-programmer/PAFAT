from tkinter import *
import tkinter as tk
from tkinter import ttk
import os, json


def createDropBox(master, dropBoxData, fg, bg, fontSize):
    ttk.Style().configure("style1.TCombobox", foreground = fg, background = bg)
    dropBox = ttk.Combobox(master, values = dropBoxData, style = "style1.TCombobox", font = ("", fontSize), width = 60)
    return dropBox

def createSlidingCheckButton(master, width, height, default):
    global on_image, off_image

    on_image = tk.PhotoImage(width=0, height=0)
    off_image = tk.PhotoImage(width=0, height=0)

    on_image.width, on_image.height = int(width), int(height)
    off_image.width, off_image.height = int(width), int(height)

    off_image.put(("red",), to=(0, 1, int(width / 2) + 1, int(height) - 1))
    on_image.put(("green",), to=(int(width / 2) + 1, 1, int(width) - 1, int(height) - 1))
    
    var = tk.IntVar(value=default)
    cb = tk.Checkbutton(master, image = on_image, selectimage = off_image, indicatoron=False, onvalue=0, offvalue=1, variable=var)

    return [var, cb]

def calculateFontSize(width, height):
    fontSize = int((width*1.15 + height*1.3) / 40)
    return fontSize

def standardButton(master, textToDisplay, func, width = 600, height = 600, bg = "black", fg = "yellow", fontSize = None):
    if fontSize is None:
        fontSize = calculateFontSize(width, height) 
    button = Button(master, text = textToDisplay, font  = ("", fontSize), bg = bg, fg = fg, command = func)
    return button

def assistButton(master, textToDisplay, func, width = 500, height = 500, bg = "red", fg = "black"):
    fontSize = calculateFontSize(width, height)
    button = Button(master, text = textToDisplay, font  = ("", fontSize), bg = bg, fg = fg, command = func)
    return button

class RoundedButton(tk.Canvas):
    def __init__(self, parent, bg, width, height, text, fontsize, command=None, color = "red", padding = 0, cornerradius = None):
        height = width if height == None else height
        cornerradius = min(width, height) / 2 if cornerradius == None else cornerradius

        tk.Canvas.__init__(self, parent, borderwidth=0, 
            relief="flat", highlightthickness=0, bg=bg)
        self.command = command

        if cornerradius > 0.5*width:
            print("Error: cornerradius is greater than width.")
            return None

        if cornerradius > 0.5*height:
            print("Error: cornerradius is greater than height.")
            return None

        rad = 2*cornerradius
        def shape():
            self.create_polygon((padding,height-cornerradius-padding,padding,cornerradius+padding,padding+cornerradius,padding,width-padding-cornerradius,padding,width-padding,cornerradius+padding,width-padding,height-cornerradius-padding,width-padding-cornerradius,height-padding,padding+cornerradius,height-padding), fill=color, outline=color)
            self.create_arc((padding,padding+rad,padding+rad,padding), start=90, extent=90, fill=color, outline=color)
            self.create_arc((width-padding-rad,padding,width-padding,padding+rad), start=0, extent=90, fill=color, outline=color)
            self.create_arc((width-padding,height-rad-padding,width-padding-rad,height-padding), start=270, extent=90, fill=color, outline=color)
            self.create_arc((padding,height-padding-rad,padding+rad,height-padding), start=180, extent=90, fill=color, outline=color)

        id = shape()
        (x0,y0,x1,y1)  = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)

        self.create_text(width/2, height/2, text=text, font = ("", fontsize))

        self.configure(width=width, height=height)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        # print(event)
        self.configure(relief="sunken")

    def _on_release(self, event):
        # print(event)
        self.configure(relief="raised")
        if self.command is not None:
            self.command()
    

def modifyUserActivity(dataToWrite):

    if not getUserActivity():
        with open("userActivity.json", "w") as f:
            f.write(json.dumps(dataToWrite, indent = 4))
    
    with open("userActivity.json") as f:
        
        modifiedData = json.load(f) | dataToWrite

        
    with open("userActivity.json", "w") as f:
        f.write(json.dumps(modifiedData, indent = 4))

def getUserActivity():
    currentPath = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(currentPath, "userActivity.json")):
        return False
    
    with open("userActivity.json") as f:
        data = dict(json.load(f))
    
    return data
    
