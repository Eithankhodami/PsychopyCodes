"""
Author: Khodami MA
Mohammadahsan.khodami@phd.unipd.it
ahsan.khodami@gmail.com
eithankhodami.github.io

Date: 12 Jan 23

DCMA:
    I have adapted this code from SR-Research examples provided in 
    https://www.sr-research.com/support/thread-7525.html
    and simplified code for those who like to directly without problem of changing implement it in their work
    
    P1:
        all libraries are related to Eye-tracker and not others, so if you need you have to import libraries for yor code
    P2:
        this code works with One Image "fixTarget.bmp" in images folder
        and 3 audio files:
            error.wav
            qbeep.wav
            type.wav
        you can download whole folder and use them and put them inside your main experiment folder
    P3:
        Also you need "EyeLinkCoreGraphicsPsychoPy.py" file which has to be in the same directory of your experiment work.

For more information, please visit https://sr-research.com/support
"""

import pylink
import time
import os
import sys
from psychopy import core, gui, visual, data
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from string import ascii_letters, digits
from PIL import Image

use_retina = False
dummy_mode = False
edf_fname = 'TEST'

dlg_title = 'Enter EDF File Name'
dlg_prompt = 'Use participant Initials and Task Name [Ex: EKTTF].'

while True:
    dlg = gui.Dlg(dlg_title)
    dlg.addText(dlg_prompt)
    dlg.addField('File Name:', edf_fname)
    ok_data = dlg.show()
    if dlg.OK:
        print('EDF data filename: {}'.format(ok_data[0]))
    else:
        print('user cancelled')
        core.quit()
        sys.exit()

    tmp_str = dlg.data[0]
    edf_fname = tmp_str.rstrip().split('.')[0]
    allowed_char = ascii_letters + digits + '_'
    if not all([c in allowed_char for c in edf_fname]):
        print('ERROR: Invalid EDF filename')
    elif len(edf_fname) > 8:
        print('ERROR: EDF filename should not exceed 8 characters')
    else:
        break

results_folder = 'EyeTrackingResults'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

time_str = time.strftime("_%Y_%m_%d_%H_%M", time.localtime())
session_identifier = edf_fname + time_str

session_folder = os.path.join(results_folder, session_identifier)
if not os.path.exists(session_folder):
    os.makedirs(session_folder)

if dummy_mode:
    el_tracker = pylink.EyeLink(None)
else:
    try:
        el_tracker = pylink.EyeLink("100.1.1.1")
    except RuntimeError as error:
        dlg = gui.Dlg("Dummy Mode?")
        dlg.addText("Couldn't connect to tracker at 100.1.1.1\n\ncontinue in Dummy Mode?")
        ok_data = dlg.show()
        if dlg.OK:
            dummy_mode = True
            el_tracker = pylink.EyeLink(None)
        else:
            print('user cancelled')
            core.quit()
            sys.exit()

# Calibration and Validation Methods
def calibrate_eyelink(el_tracker, win):
    el_tracker.setOfflineMode()
    genv = EyeLinkCoreGraphicsPsychoPy(el_tracker, win)
    pylink.openGraphicsEx(genv)

    el_tracker.sendCommand("calibration_type = HV9")
    el_tracker.sendCommand("button_function 5 'accept_target_fixation'")

    genv.setCalibrationColors((-1, -1, -1), tuple(win.color))
    genv.setTargetType('picture')
    genv.setPictureTarget(os.path.join('images', 'fixTarget.bmp'))

    if not dummy_mode:
        el_tracker.doTrackerSetup()

# Start Eye Tracker Recording (Right Eye Only)
def start_recording(el_tracker):
    el_tracker.setOfflineMode()

    # Specify the types of eye data to be recorded and sent
    file_sample_data = "RIGHT,GAZE,AREA,GAZERES,PUPIL,STATUS,HTARGET,FIXATION,SACCADE,BLINK"
    link_sample_data = "RIGHT,GAZE,AREA,GAZERES,PUPIL,STATUS,HTARGET,FIXATION,SACCADE,BLINK"

    el_tracker.sendCommand("file_sample_data = " + file_sample_data)
    el_tracker.sendCommand("link_sample_data = " + link_sample_data)

    el_tracker.startRecording(1, 1, 1, 1)
    pylink.pumpDelay(100)
    el_tracker.sendMessage("EYE_USED 1 RIGHT")

# Stop Eye Tracker Recording
def stop_recording(el_tracker):
    pylink.pumpDelay(100)
    el_tracker.stopRecording()

# Save Data and Close Connection
def save_and_close(el_tracker):
    el_tracker.setOfflineMode()
    pylink.msecDelay(500)
    el_tracker.closeDataFile()
    local_edf = os.path.join(session_folder, session_identifier + '.EDF')
    el_tracker.receiveDataFile(edf_fname + '.EDF', local_edf)
    el_tracker.close()

# PsychoPy Window Setup
win = visual.Window(fullscr=True)  # Create a window

# Calibrate the Eye Tracker
calibrate_eyelink(el_tracker, win)

# Start Recording Eye Data (Right Eye Only)
start_recording(el_tracker)
"""
you can put your experiment code here, 
remember to activate eyetracker for trial by trial, you have to put it in your loop at the begining using 

start_recording(el_tracker)

and at the end using 

stop_recording(el_tracker)

in such situation you record just during trials and not welcome screen or anything else

=== Otherwise:
    if you have plan to record everything or specific portion just use start and stop recording at those points you like to have data

"""

# Save the data and close the connection
save_and_close(el_tracker)

# Close the PsychoPy window
win.close()
