import screen_brightness_control as sbc
import time
from tkinter import *
from utility import *
import threading
import json
from tkinter.font import Font
from time import strftime

def fadeBrightness(fadeTo, interval = 0.5, increment = 1):
    current = sbc.get_brightness()[0]
    if fadeTo == current:
        return False
    if fadeTo < current:increment = -increment

    def fadingProcess():
        for i in range(current, fadeTo, increment):
            sbc.set_brightness(i)
            time.sleep(interval)
        return True

    t1 = threading.Thread(target = fadingProcess)
    t1.start()
    return t1

def adjustBrightness():
    brightness = sum(bounds)/2
    sbc.set_brightness(brightness)
    brightnessShow["text"] = f"{brightness}%"

    if brightnessCheckCompleted():
        return endBrightnessCheck()
    
    return brightness

def brightnessCheckCompleted():
    return bounds[1] - bounds[0] < 5
    
def restart():
    bounds[0], bounds[1] = [5, 95]
    adjustBrightness()

def endBrightnessCheck():
    brightness = round(sum(bounds)/2, 2)
    endScreen = Frame(win, bg = "black")
    endScreen.place(x = 0,  y = 0, width = wu*100, height = hu*100)
    title = Label(endScreen, text = "Test Completed", font = ("", calculateFontSize(wu*100, hu*25)), fg = "white", bg = "black")
    title.place(x = 0, y = 0, height = hu*25, width = wu*100)

    description = f"""
    The screen brightness test is now completed.
    your average brightness is now set to {brightness}%. 
    you can retake the test now or go back to the home 
    screen. Remember you can always take the test and 
    change your average brightness later.
    """

    showDescription = Label(endScreen, text = description, font = ("", int(calculateFontSize(wu*100, hu*55)/2)), justify = "left")
    showDescription.place(x = 0, y = hu*25, width = wu*100, height = 55*hu)

    # Write the data in a json file

    dataToWrite = {"ScreenControl":{
                "averageBrightness":str(brightness),
                "controllingBrightness":True,
                "currentBrightness":str(brightness),
                "startTime":"08:00",
                "endTime":"22:00"
                }}

    modifyUserActivity(dataToWrite)
    

    def restartQuiz():
        restart()
        endScreen.place_forget()

    buttonsWidth, buttonsHeight = 30*wu, 10*hu
    backButton = assistButton(endScreen, "Go Back", win.quit, buttonsWidth, buttonsHeight)
    restartButton = assistButton(endScreen, "Restart The quiz", restartQuiz, buttonsWidth, buttonsHeight)

    backButton.place(x  = 10*wu, width = buttonsWidth, y = 85*hu, height = buttonsHeight)
    restartButton.place(x  = 60*wu, width = buttonsWidth, y = 85*hu, height = buttonsHeight)

def about(mainRoot = None, wu = None , hu = None):

    aboutScreen = Frame(mainRoot, bg = "black")
    aboutScreen.place(x = 0,  y = 0, width = wu*100, height = hu*100)
    title = Label(aboutScreen, text = "About This Test", font = ("", calculateFontSize(wu*100, hu*25)), fg = "white", bg = "black")
    title.place(x = 0, y = 0, height = hu*25, width = wu*100)

    description = f"""
    Everyone has different screens, different lighting and different eye strain levels etc. So, there is a test which is done 
    in order to find the most optimal average screen brightness for you. REMEMBER THAT THIS IS ONLY THE 
    AVERAGE BRIGHTNESS, so the brightness will still be regulated by PAFAT in order to give you the best 
    experience, like dimming the lights on nights for better sleep etc. However, this test will give PAFAT a baseline of
    your favorable brightness. It works by setting the brightness at 50% and then you select if the brightness is too dim
    or too bright. Based on that PAFAT changes the brightness until you come up with your optimal brightness. If you 
    feel that a certain brightness is perfect then you can finalize the brightness or you could keep clicking if the 
    brightness is too dim or too bright. After a few clicks PAFAT will understand what your optimal brightness is(even if 
    you haven't finalized it by clicking the finalize button). It does this because getting to extreme precision is not 
    required. It just wants to know a rough estimate of a brightness that you are comfortable with. Once PAFAT thinks 
    that it is done then it automatically stops the test and finalizes the result. Remember that you can always take this 
    test and change your average brightness whenever you want. It also requires your morning and night time in order to know 
    when to start dimming the lights etc. It sets a default morning and night time however you can change it any time you want.
    If you don't want to use this feature then you can turn it off any time.
    """

    showDescription = Label(aboutScreen, text = description, font = ("", int(calculateFontSize(wu*90, hu*50)/3)), justify = "left")
    showDescription.place(x = 5*wu, y = hu*20, width = wu*90, height = 50*hu)

    backButton = assistButton(aboutScreen, "Quit and go back", aboutScreen.place_forget, 70*wu, hu*15)
    backButton.place(x = 15*wu, width = 70*wu, y = 75*hu, height = 15*hu)
    
def testScreenBrightness(root, WIDTH, HEIGHT):
    
    def dimFunc():
        bounds[0] = sum(bounds)/2 + 1
        adjustBrightness()

    def brightFunc():
        bounds[1] = sum(bounds)/2 - 1
        adjustBrightness()

    global win, wu, hu, bounds, brightnessShow

    wu = WIDTH/100
    hu = HEIGHT/100
    bounds = [5, 95]

    background = "#0080ff"

    win = Frame(root, bg = background)
    win.place(x = 0, y = 0, width = WIDTH, height = HEIGHT)

    title = Label(win, text = "Screen Brightness Test", font = ("", calculateFontSize(wu*100, hu*25)), fg = "white", bg = "black")
    title.place(x = 0, y = 0, height = hu*25, width = wu*100)

    brightnessShow = Label(win, text = "50%", font = ("", calculateFontSize(WIDTH, hu*6)), bg = background, fg = "black")
    brightnessShow.place(x = 0, y = hu*30, width = WIDTH, height = hu*6)
    adjustBrightness()

    upperButtonsWidth = wu*40 ; upperButtonsHeight = hu*15
    lowerButtonsWidth = wu*90 ; lowerButtonsHeight = hu*15

    dimButton = standardButton(win, "Too Dim", dimFunc, upperButtonsWidth, upperButtonsHeight)
    brightButton = standardButton(win, "Too Bright", brightFunc, upperButtonsWidth, upperButtonsHeight)
    completedButton = standardButton(win, "Finalize Brightness", endBrightnessCheck, lowerButtonsWidth, lowerButtonsHeight)

    dimButton.place(x = wu*5, y = hu*40, width = upperButtonsWidth, height = upperButtonsHeight)
    brightButton.place(x = wu*55, y = hu*40, width = upperButtonsWidth, height = upperButtonsHeight)
    completedButton.place(x = wu*5, y = hu*60, width = lowerButtonsWidth, height = lowerButtonsHeight)

    backButton = assistButton(win, "Quit and go back", win.quit)
    restartButton = assistButton(win, "Restart Test", restart)
    aboutButton = assistButton(win, "How does this work?", lambda : about(win, wu, hu))

    backButton.place(x  = 5*wu, width = 25*wu, y = 85*hu, height = 10*hu)
    aboutButton.place(x  = 36.5*wu, width = 27*wu, y = 85*hu, height = 10*hu)
    restartButton.place(x  = 70*wu, width = 25*wu, y = 85*hu, height = 10*hu)

    win.mainloop()

def changeData(userDataLabel):
    startTime, endTime, brightnessControl = startTimeDropBox.get(), endTimeDropBox.get(), brightnessControlVar.get()
    
    dataToOverWrite = {
        "startTime":startTime, 
        "endTime":endTime,
        "controllingBrightness":bool(brightnessControl)
    }

    userActivity = getUserActivity()

    userActivity["ScreenControl"] = userActivity["ScreenControl"] | dataToOverWrite

    modifyUserActivity(userActivity)
    refreshUserActivity(userDataLabel)

def refreshUserActivity(userDataLabel):
    with open("userActivity.json", "r") as f:
        userData = dict(json.load(f))["ScreenControl"]
    
    dataToShow = f"""
    Average Brightness 
        {userData["averageBrightness"]}%
    Control Brightness
        {"on" if userData["controllingBrightness"] else "off"}
    Current Brightness 
        {userData["currentBrightness"]}%
    Start Time 
        {userData["startTime"]}
    End Time 
        {userData["endTime"]}
    """

    userDataLabel['text'] = dataToShow

def updateActionInputs():
    data = dict(getUserActivity())["ScreenControl"]

    startTimeIdx = times.index(data["startTime"])
    endTimeIdx = times.index(data["endTime"])
    
    startTimeDropBox.current(startTimeIdx)
    endTimeDropBox.current(endTimeIdx)

    brightnessControlVar.set(int(data["controllingBrightness"]))

def showAndControlData(root, WIDTH, HEIGHT, wu, hu):

    def retakeQuiz():
        try:
            temp = Frame(root, bg = "white")
            temp.place(x = 0,  y = 0, width = WIDTH, height = HEIGHT)
            testScreenBrightness(temp, WIDTH, HEIGHT)
            temp.place_forget()
            showAndControlData(root, WIDTH, HEIGHT, wu, hu)
        except Exception:pass
    
    global startTimeDropBox, endTimeDropBox, brightnessControlVar, times

    root.config(bg = "black")
    

    heading = Label(root, text = "Screen Control", font = ( "", int(calculateFontSize(WIDTH, hu*20) * 1.5)), fg = "black", bg = "#bdbdbd")
    heading.place(x = 0, y = 0, width = WIDTH, height = hu*20)

    userDataLabel = Label(root, font = ("", calculateFontSize(30*wu, 70*hu)),  bg = "#a8ceff", justify = "left")
    userDataLabel.place(x = 2*wu, y = 25*hu, height = 70*hu, width = 30*wu)

    refreshUserActivity(userDataLabel)

    #AF stands for Action Frame
    AFWIDTH = 63*wu
    AFHEIGHT = 70*hu

    afwu = AFWIDTH/100
    afhu = AFHEIGHT/100

    actionFrameBackground = "#00dea6"

    actionFrame = Frame(root, bg = actionFrameBackground)
    actionFrame.place(x = 35*wu, y = 25*hu, height = AFHEIGHT, width = AFWIDTH)

    times = [f"{i if i >= 10 else f'0{i}'}:{j if j != 0 else '00'}" for i in range(0, 24) for j in range(0, 60, 15)]
    dropBoxWidth, dropBoxHeight = afwu * 90, afhu*10

    actionHeading = Label(actionFrame, text = "Change Settings", font = ("", calculateFontSize(afwu*100, afhu*10)))
    actionHeading.place(x = 0, y = 0, width = 100*afwu, height = 10*afhu)

    dropBoxHeading = Label(actionFrame, text = """Change your morning and night time by the dropbox below""", font = ("", int(calculateFontSize(afwu*100, afhu*5)/2)))
    dropBoxHeading.place(x = 0, y = 15*afhu, width = 100*afwu, height = 5*afhu)

    startTimeDropBox = createDropBox(actionFrame, times, "Blue", "Black", calculateFontSize(dropBoxWidth, dropBoxHeight))
    startTimeDropBox.place(x = afwu*5, y = afhu*25, width = dropBoxWidth, height = dropBoxHeight)

    endTimeDropBox = createDropBox(actionFrame, times, "Blue", "Black", calculateFontSize(dropBoxWidth, dropBoxHeight))
    endTimeDropBox.place(x = afwu*5, y = afhu*40, width = dropBoxWidth, height = dropBoxHeight)

    actionHeading = Label(actionFrame, text = "Control Brightness :", font = ("", int(calculateFontSize(afwu*25, afhu*10)*2.3)), bg = actionFrameBackground, fg = "dark blue", justify = "left")
    actionHeading.place(x = afwu*5, y = 55*afhu, width = 25*afwu, height = 10*afhu)

    brightnessControlVar, brightnessControlCheckBox = createSlidingCheckButton(actionFrame, afwu * 20, afhu*10, 0)
    brightnessControlCheckBox.place(y = 55*afhu, x = afwu*31, height = afhu*10)

    submitButton = standardButton(actionFrame, "Submit", lambda : changeData(userDataLabel), fontSize = calculateFontSize(afwu*35, afhu*10)*2)
    submitButton.place(y = 55*afhu, x = 60*afwu, width = afwu*35, height = afhu * 10)

    backButton = RoundedButton(actionFrame, actionFrameBackground, afwu*25, afhu*25, "Go Back", calculateFontSize(afwu*25, afhu*25)*2, root.place_forget)
    backButton.place(x = 5*afwu, y = 70*afhu)

    backButton = RoundedButton(actionFrame, actionFrameBackground, afwu*30, afhu*25, "Retake The Quiz", calculateFontSize(afwu*25, afhu*25)*2, retakeQuiz)
    backButton.place(x = 35*afwu, y = 70*afhu)

    aboutButton = RoundedButton(actionFrame, actionFrameBackground, afwu*25, afhu*25, "How it Works", calculateFontSize(afwu*25, afhu*25)*2, lambda : about(root, wu, hu))
    aboutButton.place(x = 70*afwu, y = 70*afhu)

    font = Font(family = "Helvetica", size = int(calculateFontSize(dropBoxWidth, dropBoxHeight) * 2 / 3))
    root.option_add("*TCombobox*Listbox*Font", font)

    updateActionInputs()

    root.mainloop()

def calculateCurrentInterval(percentageIntervals):
    currentTimeInMinutes = int(strftime("%H")) * 60 + int(strftime("%M"))
    if currentTimeInMinutes < percentageIntervals[0] or currentTimeInMinutes > percentageIntervals[-1]:
        return None

    bounds = []

    for i in range(1, 10):
        if percentageIntervals[i - 1] <= currentTimeInMinutes <= percentageIntervals[i]:
            bounds = [i - 1, i]

    calculateBoundDistances = lambda x : abs(percentageIntervals[x] - currentTimeInMinutes)
    boundsDistances = [calculateBoundDistances(x) for x in bounds]

    return bounds[boundsDistances.index(min(boundsDistances))]

def setCurrentBrightness(averageBrightness, interval):
    brightnessRange = 5
    brightnessRanges = [i for i in range(averageBrightness - brightnessRange, averageBrightness + brightnessRange, 1)]

    intervalToBrightness = {
        1:10,
        2:7,
        3:5,
        4:5,
        5:9,
        6:7,
        7:4,
        8:6,
        9:4,
        10:2
    }
    currentBrightnessPercentage = brightnessRanges[intervalToBrightness[interval + 1] - 1]

    userActivity = getUserActivity()
    userActivity["ScreenControl"]["currentBrightness"] = str(currentBrightnessPercentage)
    modifyUserActivity(userActivity)
    return fadeBrightness(currentBrightnessPercentage, 1)



def calculatePercentageIntervals(startTime, endTime):
    startTimeInMinutes, endTimeInMinutes = [
        int(startTime[:startTime.find(":")]) * 60 + int(startTime[startTime.find(":") + 1:]),
        int(endTime[:endTime.find(":")]) * 60 + int(endTime[endTime.find(":") + 1:])
    ]

    timeToAlterBrightness = endTimeInMinutes - startTimeInMinutes

    percentageIntervals = []
    percentageInterval = timeToAlterBrightness // 10

    for partition in range(10):
        percentageIntervals.append(percentageInterval * partition + startTimeInMinutes)
    
    return percentageIntervals

def mainScreenBrightnessControl():
    while True:
        try:
            data = getUserActivity()["ScreenControl"] 
            if not data["controllingBrightness"]:
                time.sleep(10)
            percentageIntervals = calculatePercentageIntervals(data["startTime"], data["endTime"])
            timeToWait = (percentageIntervals[1] - percentageIntervals[0]) * 2
            currentPercentageInterval = calculateCurrentInterval(percentageIntervals)
            if currentPercentageInterval is None:
                averageBrightness = int(float(data["averageBrightness"]))
                fadeBrightness(averageBrightness, 1)
                time.sleep(timeToWait)

            setCurrentBrightness(int(float(data["averageBrightness"])), currentPercentageInterval)


            time.sleep(timeToWait)
            # print("h", timeToWait)

        except Exception as e:
            time.sleep(10)


def main(root, WIDTH, HEIGHT, wu, hu):
    takeScreenTest = True
    if getUserActivity():
        with open("userActivity.json", "r") as f:
            dataOfActivity = json.load(f)
            takeScreenTest = not "ScreenControl" in dataOfActivity

    if takeScreenTest:
        testScreenBrightness(root, WIDTH, HEIGHT)
    else:
        showAndControlData(root, WIDTH, HEIGHT, wu, hu)

    root.place_forget()


# import ctypes
# ctypes.windll.shcore.SetProcessDpiAwareness(2)
# root  = Tk()
# root.geometry("2500x1500");root.title("H")
# testScreenBrightness(root, 2500, 1500)
# root.mainloop()

# mainScreenBrightnessControl()
