import datetime
from get_last_entry import get_last_entry

# === Custom Exceptions ===
class DuplicateVisitorError(Exception):

    """
    Raised when the same visitor name is entered consecutively.
    """

    def __init__(self, name: str) -> None:
        self.message: str = f"{name} Sorry visitor already exists. No double entry allowed."
        super().__init__(self.message)

class VisitorIntervalError(Exception):
    """
    Raised when a visitor tries to log in before the required time interval.
    """

    def __init__(self, minutes: int) -> None:
        self.message: str = f"Visitors must wait at least {minutes} minutes before a new entry, thank you."
        super().__init__(self.message)


# === Config ===
VISITOR_FILE: str = "visitors.txt"
TIME_INTERVAL: datetime.timedelta = datetime.timedelta(minutes=5)


def add_visitor(name: str) -> None:
    """
    Adds a visitor to the visitors file after checking rules.

    Args:
        name (str): The visitor's name

    Raises:
        DuplicateVisitorError: if the last recorded visitor has the same name
        VisitorIntervalError: if last visitor was added less than TIME_INTERVAL ago
    """
    last_entry = get_last_entry()
    now: datetime.datetime = datetime.datetime.now()

    if last_entry:
        last_name, last_time = last_entry

        # Duplicate name check (case-insensitive)
        if name.strip().lower() == last_name.strip().lower():
            raise DuplicateVisitorError(name)

        # Time interval check
        if now - last_time < TIME_INTERVAL:
            raise VisitorIntervalError(TIME_INTERVAL.seconds // 60)

    # Write new visitor with timestamp
    with open(VISITOR_FILE, "a", encoding="utf-8") as file:
        file.write(f"{name} | {now.strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"Visitor '{name}' added successfully.")
