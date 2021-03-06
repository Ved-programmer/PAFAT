#imports
from tkinter import Tk, Frame, SUNKEN, Button
import screenControl,  musicPlayer, breaks, showAbout
from win32api import GetSystemMetrics
import ctypes
from threading import Thread

#Switching File, given the fileName
def switchFile(file):
    def main():
        deleteMe = clearRoot()
        try:
            file.main(deleteMe, WIDTH, HEIGHT, wu, hu)
            deleteMe.place_forget()
            final(root)
        except Exception as e:pass
    return main

def final(root):

    global WIDTH, HEIGHT, wu, hu
    
    # Increasing the DPI settings
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    WIDTH, HEIGHT = GetSystemMetrics(0)*2//3, GetSystemMetrics(1)*3//5
    wu = WIDTH/100
    hu = HEIGHT/100

    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.maxsize(WIDTH, HEIGHT); root.minsize(WIDTH, HEIGHT)
    root.title("Main")
    root.config(bg = "red")

    buttonWidth, buttonHeight = wu*45, hu*40
    marginX, marginY = 3*wu, 5*hu

    # containerSize = 35*hu
    # CONTROL_Y = HEIGHT - containerSize
    # marginalSpace = (containerSize - buttonHeight)/2

    startX = marginX
    endX = WIDTH - marginX - buttonWidth
    startY = marginY
    endY = HEIGHT - marginY - buttonHeight
    
    makeButton(root, "Brightness Control", switchFile(screenControl), buttonWidth, buttonHeight, startX, startY)
    makeButton(root, "About", switchFile(showAbout), buttonWidth, buttonHeight, startX, endY)
    makeButton(root, "Music Player", switchFile(musicPlayer), buttonWidth, buttonHeight, endX, endY)
    makeButton(root, "Notifications", switchFile(breaks), buttonWidth, buttonHeight, endX, startY)

    # makeButton(root, "About Me", switchFile(showAbout), WIDTH - 2 * marginX, buttonHeight, startX, CONTROL_Y + marginalSpace)

    backgroundScreenControl = Thread(target = screenControl.mainScreenBrightnessControl)
    backgroundScreenControl.daemon = True
    backgroundScreenControl.start()

    root.mainloop()

#Button Design
def makeButton(root, Text, Function, width, height, xPos, yPos):
    button = Button(root, text = Text, bg="black", fg = "yellow",
            font = f"comicsansms {int((width + height)/20)}", borderwidth = 15, relief = SUNKEN, command = Function)
    button.place(x = xPos, y = yPos, width = width, height = height)
 
def clearRoot():
    frame = Frame(root, bg = "white")
    frame.place(x = 0,  y = 0, width = WIDTH, height = HEIGHT)
    return frame


def closingSequence():
    musicPlayer.stop()
    breaks.stopNotifications()
    exit()

    
#Execution
if __name__ == "__main__":
    root = Tk()
    final(root)
    closingSequence()

