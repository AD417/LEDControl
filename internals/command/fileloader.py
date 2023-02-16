from __future__ import annotations

from .. import Program

def load_file(filepath: str):
    with open(filepath) as f:
        Program.command_queue = [x for x in f.readlines() if x.strip("\n ") != ""]
    
    if len(Program.command_queue) > 0:
        Program.file_loaded = True

def file_summary():
    summary = ""
    while True:
        if "#" not in Program.command_queue[0]: break
        potential_command, comment = Program.command_queue[0].split("#", 1)
        if len(potential_command.strip("\n ")) != 0: break
        summary += "--- " + comment.strip("# ")
        Program.command_queue.pop(0)

    return summary


def load_next_command():
    Program.logger = ""
    while len(Program.command_queue) > 0:
        potential_next_command = Program.command_queue.pop(0)
        comment = ""

        if "#" in potential_next_command: 
            potential_next_command, comment = potential_next_command.split("#", 1)

        potential_next_command = potential_next_command.strip("\n ")
        comment = comment.strip("\n #")

        if len(comment) > 0: Program.logger += "--- " + comment + "\n"
        if len(potential_next_command) > 0: 
            Program.logger += "Executing command: " + potential_next_command
            print(Program.logger)
            return potential_next_command

    Program.logger += "There are no more commands to execute! Exiting now."
    print(Program.logger)
    # We are out of stuff to do.
    return "exit"
