from __future__ import annotations

def try_num(value: str) -> int:
    try: 
        return float(value)
    except ValueError: 
        return 0