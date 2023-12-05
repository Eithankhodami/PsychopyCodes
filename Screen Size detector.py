"""
Author: Khodami
DCMA: This code is part of course of teaching Psychopy design for psychologists using Coder "Not editor"
The code is working if you have Psychopy installed

this code sets up a Psychopy experiment where it creates a fullscreen visual window, displays a message with information about the screen's dimensions in pixel
"""


from psychopy import visual, core, event


win = visual.Window(monitor="testMonitor", units="pix", fullscr=True)


#detect screen size
pixel_width = win.size[0]
pixel_height = win.size[1]

#show a message

message = visual.TextStim(win, text=f'your monitor is {pixel_width}px as width and {pixel_height}px as height', color="black", height=40)
message.draw()

win.flip()

#wait for a key press
event.waitKeys()

win.close()
core.quit()
