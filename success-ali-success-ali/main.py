import os
import datetime


# === Custom Exceptions ===
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        self.message = f"{name} visitor already exists. No back-to-back entry allowed."
        super().__init__(self.message)


class VisitorIntervalError(Exception):
    def __init__(self, minutes):
        self.message = f"Visitors must wait at least {minutes} minutes before a new entry."
        super().__init__(self.message)


# === Config ===
VISITOR_FILE = "visitors.txt"
TIME_INTERVAL = datetime.timedelta(minutes=5)


# === Helper 1: Get Last Entry ===
def get_last_entry():
    """
    Reads the last line in the visitor file (if exists).
    Returns tuple (name, timestamp) or None if file empty.
    """
    if not os.path.exists(VISITOR_FILE):
        return None

    with open(VISITOR_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if not lines:
            return None
        last_line = lines[-1].strip()
        name, timestamp = last_line.split(" | ")
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return name, timestamp


# === Helper 2: Add Visitor ===
def add_visitor(name):
    """
    Adds a visitor after checking for duplicates and time intervals.
    Raises DuplicateVisitorError or VisitorIntervalError if validation fails.
    """
    last_entry = get_last_entry()
    now = datetime.datetime.now()

    if last_entry:
        last_name, last_time = last_entry

        # Duplicate name check
        if name.strip().lower() == last_name.strip().lower():
            raise DuplicateVisitorError(name)

        # Time interval check
        if now - last_time < TIME_INTERVAL:
            raise VisitorIntervalError(TIME_INTERVAL.seconds // 60)

    # Write visitor with timestamp
    with open(VISITOR_FILE, "a", encoding="utf-8") as file:
        file.write(f"{name} | {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"Visitor '{name}' added successfully.")


# === Main Program ===
def main():
    print("=== Visitor Registration ===")
    try:
        name = input("Enter visitor's name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        add_visitor(name)
    except DuplicateVisitorError as e:
        print("Error:", e)
    except VisitorIntervalError as e:
        print("Error:", e)
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    main()
