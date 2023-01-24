"""Namespace of all valid command names"""
from __future__ import annotations
from typing_extensions import Final
from types import SimpleNamespace

ALTERNATING:    Final[list[str]] = ["alt"]
COLOR:          Final[list[str]] = ["color"]
EXIT:           Final[list[str]] = ["exit", "leave", "shutdown", "stop"]
FLASH:          Final[list[str]] = ["flash", "blink"]
FILL:           Final[list[str]] = ["fill", "on"]
KILL:           Final[list[str]] = ["off", "kill"]
PAUSE:          Final[list[str]] = ["pause"]
PULSE:          Final[list[str]] = ["pulse"]
TRAFFIC:        Final[list[str]] = ["cars", "traffic"]
WAVE:           Final[list[str]] = ["wave"]

COLOR_PARAMETER:        Final[str] = "-c"
RECURSION_PARAMETER:    Final[str] = "-e"
KILL_PARAMETER:         Final[str] = "-k"
FUTURE_PARAMETER:       Final[str] = "-n"
PAUSE_PARAMETER:        Final[str] = "-p"
TRANSITION_PARAMETER:   Final[str] = "-t"