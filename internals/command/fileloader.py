from __future__ import annotations

from .. import Program

def load_file(filepath: str):
    command_queue: list[str] = []
    with open(filepath) as f:
        for line in f.readlines():

            if "#" in line: 
                line, _ = line.split("#", 1)
            line = line.strip("\n ")

            if len(line) == 0: continue
            
            command_queue.append(line)
    
    if len(command_queue) > 0:
        Program.command_queue = command_queue
        Program.file_loaded = True
