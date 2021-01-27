from tkinter import *
from utility import *
from tkinter import messagebox
import time
import threading
from win10toast import ToastNotifier
toast = ToastNotifier()

def main(root, WIDTH, HEIGHT, wu, hu):

    global productiveTimeEntry, breakTimeEntry, currentStatusLabel

    root.config(bg = "black")

    heading = Label(root, text = "Notifications", font = ( "", int(calculateFontSize(WIDTH, hu*20) * 1.5)), fg = "black", bg = "#bdbdbd")
    heading.place(x = 0, y = 0, width = WIDTH, height = hu*20)

    productiveTimeLabel = Label(root, text = "Enter the amount of time(in minutes) between breaks", font = ( "", int(calculateFontSize(wu*70, hu*15) )), fg = "white", bg = "black", justify = LEFT)
    productiveTimeLabel.place(x = 5*wu, y = 25*hu, height = hu*10)

    productiveTimeEntry = Entry(root, font = ("", int(calculateFontSize(wu * 90, hu*10)*2/3)), highlightbackground="red")
    productiveTimeEntry.place(x = 5*wu, y = 35*hu, width = wu*90, height = hu*10)

    breakTimeLabel = Label(root, text = "Enter the length(in minutes) of breaks", font = ( "", int(calculateFontSize(wu*70, hu*15) )), fg = "white", bg = "black", justify = LEFT)
    breakTimeLabel.place(x = 5*wu, y = 45*hu, height = hu*10)

    breakTimeEntry = Entry(root, font = ("", int(calculateFontSize(wu * 90, hu*10)*2/3)), highlightbackground="red")
    breakTimeEntry.place(x = 5*wu, y = 55*hu, width = wu*90, height = hu*10)

    currentStatusLabel = Label(root, text = "Current Status : N/A", font = ( "", int(calculateFontSize(wu*40, hu*10) )), fg = "white", bg = "black", justify = LEFT)
    currentStatusLabel.place(x = 5*wu, y = 65*hu, height = hu*10)

    helpButton = standardButton(root, "Not Working? Click For Help", lambda : showHelp(root, WIDTH, HEIGHT), wu*50, hu*8)
    helpButton.place(x = wu*55, width = wu*40, height = hu*8, y = 65*hu)

    startButton = RoundedButton(root, "black", 25*wu, 25*hu, "Start", int(calculateFontSize(25*wu, 25*hu)*1.2), startNotifications, "#00ff6e")
    startButton.place(x = 5*wu, y = 75*hu, width = 25*wu, height = 25*hu)
    
    backButton = RoundedButton(root, "black", 30*wu, 25*hu, "Go Back", int(calculateFontSize(30*wu, 25*hu)*1.2), root.place_forget, "#00bbff")
    backButton.place(x = 35*wu, y = 75*hu, width = 30*wu, height = 25*hu)

    stopButton = RoundedButton(root, "black", 25*wu, 25*hu, "Stop", int(calculateFontSize(25*wu, 25*hu)*1.2), stopNotifications, "#00ff6e")
    stopButton.place(x = 70*wu, y = 75*hu, width = 25*wu, height = 25*hu)

    root.mainloop()

def showNotifications(title, description):
    showNotification = threading.Thread(target = lambda : toast.show_toast(title, description))
    showNotification.start()
    return showNotification

def startNotifications():

    showNotifications("Notifications On", "You will recieve notifications like this for taking breaks")

    userNotificationData = {
        "notifications":{"showNotifications":True}
    }

    modifyUserActivity(userNotificationData)

    def checkToLeave(lengthOfBreak):
        start = time.time()
        if lengthOfBreak == "":
            messagebox.showinfo("Error", "Enter a valid time")
            return True

        while time.time() - start < float(lengthOfBreak) * 60:
            time.sleep(1)
            if not getUserActivity()["notifications"]["showNotifications"]:
                return True

        return False

    def notificationCycle(productiveTime, breakTime):
        while True:
            currentStatusLabel['text'] = "Working Time"
            if checkToLeave(productiveTime):break
            showNotifications("Break Time", "It is time to take a break")

            currentStatusLabel['text'] = "Break Time"
            if checkToLeave(breakTime):break
            showNotifications("Break Over", "the break is now over, please continue your work")  
    
    notificationCycleThread = threading.Thread(target = lambda : notificationCycle(productiveTimeEntry.get(), breakTimeEntry.get()))
    notificationCycleThread.start()


def stopNotifications():
    userNotificationData = {
        "notifications":{"showNotifications":False}
    }
    modifyUserActivity(userNotificationData)

    time.sleep(3)
    showNotifications("Notifications Off", "The notifications are now turned off")

def showHelp(root, WIDTH, HEIGHT):

    wu, hu = WIDTH/100, HEIGHT/100

    aboutText = """
    This feature helps users be focused with breaks. You need to enter the time you want to be taking breaks, 
    then click start, once you click start then the program will start with the state of you working. After the 
    specified time(given by the user) it will send a notification saying that it is time to a break. Then after 
    the time of the break is over it will again sendma notification to the user to continue working. This will 
    continue indefinitely until the user stops it or closes the application.

    If you don't get any notifications after clicking start then this might be because your windows settings don't 
    allow applications to show notifications, to enable that you need to go to notifications and action settings,
    just search in the search bar of windows. Then under notifications you need to enable notifications from apps 
    and other senders. This will allow the notifications to come.

    """

    aboutScreen = Frame(root, bg = "black")
    aboutScreen.place(x = 0,  y = 0, width = WIDTH, height = HEIGHT)

    title = Label(aboutScreen, text = "Help with Notifications", font = ("", calculateFontSize(WIDTH, hu*25)), fg = "white", bg = "black")
    title.place(x = 0, y = 0, height = hu*25, width = WIDTH)

    showDescription = Label(aboutScreen, text = aboutText, font = ("", int(calculateFontSize(wu*90, hu*45)*2/5)), justify = "left")
    showDescription.place(x = 5*wu, y = hu*25, width = wu*90, height = 50*hu)

    backButton = assistButton(aboutScreen, "Go Back", aboutScreen.place_forget, 70*wu, 15*hu)
    backButton.place(x  = 15*wu, width = 70*wu, y = 80*hu, height = 15*hu)

