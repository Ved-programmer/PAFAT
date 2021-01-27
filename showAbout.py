from win32com.client import Dispatch
from tkinter import *
from utility import assistButton, calculateFontSize
from PIL import ImageTk, Image  
import threading
import pythoncom

engine = Dispatch('SAPI.SpVoice')

displayAbout = """
Hi, my name is PAFAT, which stands for Personal Assistant for a timathon.
I am made by Ved Rathi.

I am made to help people who spend a lot of time on computers. I can do 
various tasks like: adjusting the screen light for the best performance, playing songs, 
asking to take breaks at pre defined times, collect and show statistics like how much 
time spent productively per day or how many times break taken etc.

NOTE: All the features would only work if the application is on, so you would need to 
keep the application running for the entire day.
"""

# My name is Ved Rathi but since the voice can't pronounce me correctly I have written wayed which when spoken sounds like my name.
speakingAbout = " ".join(displayAbout.replace("Ved", "Wayed").splitlines())
def toSpeak():
    pythoncom.CoInitialize()
    engine.speak(speakingAbout)

startSpeaking = threading.Thread(target = toSpeak)
startSpeaking.denom = 1

def speak():
    startSpeaking.start()


def main(root, WIDTH, HEIGHT, wu, hu):
    aboutScreen = Frame(root, bg = "black")
    aboutScreen.place(x = 0,  y = 0, width = WIDTH, height = HEIGHT)

    title = Label(aboutScreen, text = "About This Test", font = ("", calculateFontSize(WIDTH, hu*25)), fg = "white", bg = "black")
    title.place(x = 0, y = 0, height = hu*25, width = WIDTH)

    showDescription = Label(aboutScreen, text = displayAbout, font = ("", int(calculateFontSize(wu*90, hu*45)*7/15)), justify = "left")
    showDescription.place(x = 5*wu, y = hu*25, width = wu*90, height = 50*hu)

    backButton = assistButton(aboutScreen, "Go Back", root.quit, 70*wu, 15*hu)
    backButton.place(x  = 15*wu, width = 70*wu, y = 80*hu, height = 15*hu)

    speakButtonSize = int(wu*5)
    adjustedImage = Image.open("button.png").resize((speakButtonSize, speakButtonSize), Image.ANTIALIAS)
    finalImage = ImageTk.PhotoImage(adjustedImage)

    speakButton  = Button(aboutScreen, image = finalImage, command = speak)
    speakButton.place(x = wu, y = 8*hu, width = speakButtonSize, height = speakButtonSize)

    root.mainloop()


# root = Tk()
# global WIDTH, HEIGHT, wu, hu
# ctypes.windll.shcore.SetProcessDpiAwareness(2)
# WIDTH, HEIGHT = 2000, 1250
# wu = WIDTH/100
# hu = HEIGHT/100
# root.geometry(f"{WIDTH}x{HEIGHT}")
# root.maxsize(WIDTH, HEIGHT); root.minsize(WIDTH, HEIGHT)
# root.title("Main")
# root.config(bg = "red")

# main(root, WIDTH, HEIGHT, wu, hu)
# root.mainloop()
