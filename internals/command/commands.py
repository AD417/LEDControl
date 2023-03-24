"""Namespace of all built-in valid command names"""
from __future__ import annotations

from typing_extensions import Final

ALIAS:          Final[list[str]] = ["alias"]
ALTERNATING:    Final[list[str]] = ["alt"]
COLOR:          Final[list[str]] = ["color"]
ECHO:           Final[list[str]] = ["echo", "#", "//"]
EXIT:           Final[list[str]] = ["exit", "leave", "shutdown", "stop"]
FILL:           Final[list[str]] = ["fill", "on"]
FIREWORKS:      Final[list[str]] = ["fireworks"]
FLASH:          Final[list[str]] = ["flash", "blink"]
KILL:           Final[list[str]] = ["off", "kill"]
OUT_STATE:      Final[list[str]] = ["outstate", "setout", "out"]
PAUSE:          Final[list[str]] = ["pause"]
PULSE:          Final[list[str]] = ["pulse"]
STATUS:         Final[list[str]] = ["status"]
TRAFFIC:        Final[list[str]] = ["cars", "traffic"]
WAVE:           Final[list[str]] = ["wave"]