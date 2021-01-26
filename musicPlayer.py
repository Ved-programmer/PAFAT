from tkinter import *
from utility import *
import os
from tkinter import messagebox
import threading
from os import listdir
from os.path import isfile, join
from pygame import mixer  # Load the popular external library
import time
from mutagen.mp3 import MP3
def main(root, WIDTH, HEIGHT, wu, hu):
    global songFolderEntry, currentFolderLabel, currentSongLabel

    root.config(bg = "black")

    heading = Label(root, text = "Music Player", font = ( "", int(calculateFontSize(WIDTH, hu*20) * 1.5)), fg = "black", bg = "#bdbdbd")
    heading.place(x = 0, y = 0, width = WIDTH, height = hu*20)

    instruction = Label(root, text = "Enter the path to your music folder below.", font = ( "", int(calculateFontSize(wu*70, hu*15) )), fg = "white", bg = "black", justify = LEFT)
    instruction.place(x = 5*wu, y = 25*hu, height = hu*15)

    songFolderEntry = Entry(root, font = ("", int(calculateFontSize(wu * 90, hu*10)*2/3)), highlightbackground="red")
    songFolderEntry.place(x = 5*wu, y = 45*hu, width = wu*90, height = hu*10)

    currentFolderLabel = Label(root, text = "Current Playing Folder : N/A", font = ( "", int(calculateFontSize(wu*50, hu*10) )), fg = "white", bg = "black", justify = LEFT)
    currentFolderLabel.place(x = 5*wu, y = 55*hu, height = hu*10)

    currentSongLabel = Label(root, text = "Current Playing Song : N/A", font = ( "", int(calculateFontSize(wu*50, hu*10) )), fg = "white", bg = "black", justify = LEFT)
    currentSongLabel.place(x = 5*wu, y = 65*hu, height = hu*10)

    playButton = RoundedButton(root, "black", 25*wu, 25*hu, "Play", int(calculateFontSize(25*wu, 25*hu)*1.2), playSongs, "#00ff6e")
    playButton.place(x = 5*wu, y = 75*hu, width = 25*wu, height = 25*hu)
    
    playButton = RoundedButton(root, "black", 30*wu, 25*hu, "Go Back", int(calculateFontSize(30*wu, 25*hu)*1.2), root.place_forget, "#00bbff")
    playButton.place(x = 35*wu, y = 75*hu, width = 30*wu, height = 25*hu)

    playButton = RoundedButton(root, "black", 25*wu, 25*hu, "Stop", int(calculateFontSize(25*wu, 25*hu)*1.2), stop, "#00ff6e")
    playButton.place(x = 70*wu, y = 75*hu, width = 25*wu, height = 25*hu)

    userActivity = getUserActivity()
    if userActivity is not None:
        if "musicPlayer" in userActivity:
            currentFolderLabel['text'] = f"Current Playing Folder : {userActivity['musicPlayer']['currentFolder']}"
            currentSongLabel['text'] = f"Current Playing Song : {userActivity['musicPlayer']['currentSong']}"
    root.mainloop()

def stop():

    modifyUserActivity({
                "musicPlayer":{"playingSongs":False}
                })

    try:
        currentFolderLabel["text"] = f"Current Playing Folder : N/A"
        currentSongLabel["text"] = f"Current Playing Folder : N/A"
    except Exception:
        pass


def playSongs():

    songFolderPath = songFolderEntry.get()

    if not os.path.exists(songFolderPath):
        messagebox.showerror("Path Location Error", "The path entered is not a valid path.")
        return
    
    def play(songFolderPath):
        modifyUserActivity({
                "musicPlayer":{
                    "playingSongs":True,
                    "currentFolder": songFolderPath
                    }
            })

        currentFolderLabel["text"] = f"Current Playing Folder : {songFolderPath}"
        
        mixer.init()
        while True:
            files = [join(songFolderPath, f) for f in listdir(songFolderPath) if isfile(join(songFolderPath, f))]
            musicFiles = [file for file in files if file.endswith(".mp3")]
            if len(musicFiles) == 0:
                messagebox.showerror("No Song Found", "There were no mp3 files found in the path entered.")
                return
            continueToPlaySong = True

            for musicFile in musicFiles:
                musicFileAddedActivity = getUserActivity()
                musicFileAddedActivity["musicPlayer"]["currentSong"] = musicFile
                modifyUserActivity(musicFileAddedActivity)

                mixer.music.load(musicFile)
                mixer.music.play()
                audio = MP3(musicFile)
                lengthOfMusic = int(audio.info.length) # In Seconds
                start = time.time()
                currentSongLabel["text"] = f"Current Playing Song : {musicFile}"

                while time.time() - start < lengthOfMusic:
                    userActivity = getUserActivity()["musicPlayer"]
                    if not userActivity["playingSongs"]:
                        continueToPlaySong = False
                    if not continueToPlaySong:
                        break
                    time.sleep(0.05)
                
                if not continueToPlaySong:
                    break
            if not continueToPlaySong:
                break
            
        mixer.quit()
            
    playThread = threading.Thread(target = lambda : play(songFolderPath))
    playThread.daemon = True
    playThread.start()


