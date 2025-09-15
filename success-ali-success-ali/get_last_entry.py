import os
import datetime
from typing import Optional, Tuple

VISITOR_FILE: str = "visitors.txt"

def get_last_entry() -> Optional[Tuple[str, datetime.datetime]]:
    """
    Reads the last line in the visitors file if it exists.

    Returns:
        tuple: (visitor_name, timestamp) if file has entries
        None: if file does not exist or is empty
    """
    if not os.path.exists(VISITOR_FILE):
        return None  # No file yet, no entry

    with open(VISITOR_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if not lines:
            return None  # Empty file, no entry
        last_line: str = lines[-1].strip()
        name, timestamp_str = last_line.split(" | ")
        timestamp: datetime.datetime = datetime.datetime.strptime(
            timestamp_str, "%Y-%m-%d %H:%M:%S"
        )
        return name, timestamp
