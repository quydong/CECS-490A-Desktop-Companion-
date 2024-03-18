import json
from datetime import date
from string import ascii_lowercase

def reset_daily_data():
    """
    Resets all daily tracking values to zero and updates the date to today.
    This includes mouse clicks (left, right, middle), scrolls, key presses,
    and initializes a count of 0 for each letter in the alphabet.
    Both the primary and backup daily data files are updated.
    """
    # Initialize the structure with zeros for all counts and today's date
    new_data = {
        "Daily Left": 0,
        "Daily Right": 0,
        "Daily Middle": 0,
        "Daily Scrolls": 0,
        "Daily Pressed": 0,
        "Daily Letters": {letter: 0 for letter in ascii_lowercase},
        "Date": str(date.today())
    }

    # Write the reset data to the daily JSON file and its backup
    with open('Daily.json', 'w', encoding='utf8') as file:
        json.dump(new_data, file, indent=4)
    with open('Daily.backup', 'w', encoding='utf8') as backup_file:
        json.dump(new_data, backup_file, indent=4)

def reset_lifetime_data():
    """
    Resets all lifetime tracking values to zero.
    This includes mouse clicks (left, right, middle), scrolls, key presses,
    and initializes a count of 0 for each letter in the alphabet.
    Both the primary and backup lifetime data files are updated.
    """
    # Initialize the structure with zeros for all counts
    new_data = {
        "Total Left": 0,
        "Total Right": 0,
        "Total Middle": 0,
        "Total Scrolls": 0,
        "Total Pressed": 0,
        "Total Letters": {letter: 0 for letter in ascii_lowercase}
    }

    # Write the reset data to the lifetime JSON file and its backup
    with open('Lifetime.json', 'w', encoding='utf8') as file:
        json.dump(new_data, file, indent=4)
    with open('Lifetime.backup', 'w', encoding='utf8') as backup_file:
        json.dump(new_data, backup_file, indent=4)

def reset_all():
    """
    Resets both daily and lifetime data to their initial states.
    After resetting, it prints a confirmation message.
    """
    reset_daily_data()
    reset_lifetime_data()
    print("All data has been reset.")

if __name__ == "__main__":
    reset_all()
