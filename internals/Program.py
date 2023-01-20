from __future__ import annotations
from .LED_data import *

# Whether the program is running.
is_running: bool = True
# The current animation used by the strip
animation: Animation = KillAnimation()

color: RGB = RGB(255,0,0)
is_interrupted: bool = False
interrupt: InterruptAnimation = FlashAnimation()

flash_color: RGB = RGB(255,255,255)
performing_recursion: bool = False
recursive_command: str = ""
performing_next_command: bool = False
next_command: str = ""
is_paused: bool = False
time_to_unpause: int = 0