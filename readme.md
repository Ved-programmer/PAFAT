<!-- markdownlint-disable-file -->

<!-- PAFAT -->
<center>

# <font size="7"> **PAFAT** - *Personal Assistant For A Timathon* </font>

<br />


<font size="5"> Features - Brightness Controlling, Music Playing and Notifying For Breaks. </font>

</center>

<br>

<hr width = 50% >

<br>
<br>

* ## Notes 


    * Note that All the features would only work if the user has the application running, although many features can run at the same time,however, they can only work if the application is on.

    * Windows 10 and python 3.9.0(or above) is recommended to run PAFAT

<br>

* ## Brightness Control

    * Take a test to determine optimal brightness of the user. The brightness level starts at 50% and then adjusted by the user. The test ends when either the user finalizes a brightness or adjusts the brightness enough for PAFAT to get a good idea of the optimal brightness for the user.

    * PAFAT has a default start and end time of 8:00 and 22:00 respectively. These settings can be changed by the user after taking the test. There are different lighting conditions which are suitable for different times of the day. So PAFAT needs to know what the waking time and sleeping time of the user is in order to optimally control the screen brightness. 

    * Users can toggle(turn off or on) this setting if they want to. The test requires the user to be present and taking the test. However, once PAFAT has the average brightness, start time and end time then it can start to control the optimal brightness for the user. PAFAT does this asynchronously, so the user just needs to keep the application running, then the user can minimize the GUI and do other tasks on his/her machine. The brightness would be controlled by PAFAT. However, some users might want to use the other features but not want this feature. In this case the users can toggle this setting. If the setting is turned off then PAFAT would not control the brightness, this is the brightnessControlPermission setting

    * The Screen Brightness Control Feature stores 5 different types of data. The start time, end time, average brightness, brightnessControlPermission and current brightness. 

<br>

* ## Music Player

    * The user enters a path to a folder on their machine which should contain audio files(only .mp3 files are supported). 

    * Once the user enters the path and clicks on the play button, PAFAT collects all the MP3 files in the Folder

    * After collecting all the MP3 files PAFAT start playing each song. After the completion of the songs, PAFAT again recollects all the song files in the folder and starts playing them. PAFAT recollectes all the MP3 files in the folder because the user could have added more MP3 files in the folder. 

    * This process continues indefintely until the user pressed the stop button. 

<br>

* ## Break Notifications

    * The user enters the amount of time(in minutes) between breaks and the length of each break(also in minutes).

    * The user then clicks on the start button. This shows a notification to the user that the process has started.

    * There are two states, one if the productive state in which the user is not in a break and is working, the other state is the break state in which a break is going on and the user is not working. The length of each state are the values entered by the user.

    * Once the user starts the the process, the first state will be the productive state. The productive state will last as long as the user's entered time between the breaks. 

    * Once the productive state ends, the user will get a notification saying that it is time to take a break. This is when the break state starts, this state lasts as long as the user's entered time for the length of the break. Once this is over, the user will get a notification saying that the break it over and they should start working and then the productive state will start. This cycle will continue until the user manually stops the process by clicking on the stop button.

<br>
<hr>
<br>

> <font size = "5"> This project was made by Ved Rathi for a Timathon hosted by Tim. </font>

<br><br>

*-Thank You*
