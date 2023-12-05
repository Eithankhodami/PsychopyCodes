# Import necessary libraries
from psychopy import visual, core

# Create a window
win = visual.Window(
    size=[1760, 990], fullscr=True, screen=1,
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
    units='deg'
)

total_duration = 180  # 3 minutes in seconds
progress_bar = visual.TextStim(win, text='-' * total_duration, color='yellow', pos=(-5, -1), height=0.4)  # Increase the height to 0.2
timer = core.Clock()
progress_bar.draw()
win.flip()
update_interval = 1
seconds_elapsed = 0
while seconds_elapsed < total_duration:
    progress_text = '|' * seconds_elapsed + '-' * (total_duration - seconds_elapsed)
    progress_bar.setText(progress_text)
    progress_bar.draw()
    win.flip()
    core.wait(update_interval)
    seconds_elapsed += update_interval
core.wait(total_duration - seconds_elapsed)
win.close()
