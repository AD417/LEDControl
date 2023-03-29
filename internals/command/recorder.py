from __future__ import annotations

import os

commands: list[str] = []

output_relative_file: str = "../../etc/recording.txt"

def _get_output_file() -> str:
    """Determine where the commands are being stored."""
    full_file_path = os.path.dirname(__file__)
    full_file_path = os.path.abspath(
        os.path.join(full_file_path, output_relative_file)
    )
    return full_file_path

def add(command: str):
    """Append a new command to the list of commands executed."""
    commands.append(command)

def save_commands():
    full_file_path = _get_output_file()

    with open(full_file_path, "a") as file:
        file.write("\n\n")
        file.write("\n".join(commands))
