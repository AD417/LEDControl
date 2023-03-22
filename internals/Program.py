"""Program namespace containing typed global variables for use across the program."""
from __future__ import annotations

from datetime import datetime

from .LED_data import *

dry_run: bool = False
is_running: bool = True
animation: Animation = KillAnimation()

color: RGB = RGB(255,255,255)
is_interrupted: bool = False
# interrupt: InterruptAnimation = FlashAnimation()

flash_color: RGB = RGB(255,255,255)
performing_recursion: bool = False
recursive_command: str = ""
performing_next_command: bool = False
next_command: str = ""
is_paused: bool = False
time_to_unpause: datetime = datetime.now()

# The active strips. 1-7 are all binary for the shops; 0 is for fireworks. 
active_strips: int = 7

command_queue: list[str] = []
file_loaded: bool = False

logger: str = ""