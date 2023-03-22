"""Namespace of all built-in valid command names"""
from __future__ import annotations

from typing_extensions import Final

ALIAS:          Final[list[str]] = ["alias"]
ALTERNATING:    Final[list[str]] = ["alt"]
COLOR:          Final[list[str]] = ["color"]
ECHO:           Final[list[str]] = ["echo", "#", "//"]
EXIT:           Final[list[str]] = ["exit", "leave", "shutdown", "stop"]
FLASH:          Final[list[str]] = ["flash", "blink"]
FILL:           Final[list[str]] = ["fill", "on"]
KILL:           Final[list[str]] = ["off", "kill"]
OUT_STATE:      Final[list[str]] = ["outstate", "setout", "out"]
PAUSE:          Final[list[str]] = ["pause"]
PULSE:          Final[list[str]] = ["pulse"]
STATUS:         Final[list[str]] = ["status"]
TRAFFIC:        Final[list[str]] = ["cars", "traffic"]
WAVE:           Final[list[str]] = ["wave"]

COLOR_PARAMETER:        Final[str] = "-c"
ECHO_PARAMETER:         Final[str] = "#"
FUTURE_PARAMETER:       Final[str] = "-n"
KILL_PARAMETER:         Final[str] = "-k"
PAUSE_PARAMETER:        Final[str] = "-p"
RECURSION_PARAMETER:    Final[str] = "-e"
TRANSITION_PARAMETER:   Final[str] = "-t"