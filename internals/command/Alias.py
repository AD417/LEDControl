"""Processing environment to store, retrieve, and add aliases."""
from __future__ import annotations

import os.path

Aliases: dict[str, list[str]] = {}
alias_relative_file: str = "../../config/alias.txt"

def alias_exists_for(name: str):
    return name in Aliases.keys()

def command_for_alias(name: str):
    return Aliases[name].copy()

def create_alias(name: str, command: list[str]):
    """Create a new alias. \n
    Parameters:
    `name`: the name of the alias
    `command`: the command that the alias runs"""

    if len(name) == 0: raise ValueError("Malformed or missing name: %r" % name)
    if len(command) == 0: raise ValueError("Malformed or missing command: %r" % command)

    Aliases[name] = command

def _get_alias_file() -> str:
    """Determine where the aliases are being stored."""
    full_file_path = os.path.dirname(__file__)
    full_file_path = os.path.abspath(
        os.path.join(full_file_path, alias_relative_file)
    )
    return full_file_path

def load_aliases():
    """Load the current alias data from its file."""
    full_file_path = _get_alias_file()

    with open(full_file_path, "r") as f:
        for line in f.readlines():
            if len(line) == 0: continue
            alias_name, command = line.strip(" \n").split(" ", 1)
            create_alias(alias_name, command.split())


def save_aliases(): 
    """Save the current alias data to the file."""

    alias_file_data = ""

    for key, value in Aliases.items():
        alias_file_data += "%s %s\n" % (key, " ".join(value))

    full_file_path = _get_alias_file()

    with open(full_file_path, "w") as f:
        f.write(alias_file_data)



load_aliases()