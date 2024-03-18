import GUI
import reset
import time 
import threading
import json
import os
import tendo
import ctypes
import psutil
from tendo import singleton
from datetime import date
from infi.systray import SysTrayIcon
from pynput import mouse, keyboard
import socket
from threading import Thread
from GUI import generateDynamicFeedback 
# Set the working directory to the folder where this script is located
os.chdir(os.path.dirname(os.path.abspath(__file__))) 

try:
    # Attempt to ensure only one instance of the script runs at a time
    singleInstance = singleton.SingleInstance() 
except tendo.singleton.SingleInstanceException:
    # If a second instance is started, it opens the GUI window instead of exiting
    # This approach can lead to multiple stats windows being opened simultaneously, which is a known issue
    GUI.open_the_window()
    reset.reset_all()
    exit()

# Lock to prevent race conditions in multi-threaded operations
Lock = threading.Lock()  

def CheckDate():
    """
    Checks if the current system date is different from the date stored in 'Daily.json'.
    If it is, the script resets the daily tracking values and updates the date to today.
    This function runs in a loop in its own thread.
    """
    while True:
        time.sleep(100)
        with open('Daily.json', encoding='utf8') as File:
            FileData = json.load(File)
            if FileData["Date"] != str(date.today()):
                reset.reset_all()
                global daily
                daily = DailyClass()

class LifetimeClass():
    """
    Manages lifetime statistics for mouse clicks and keyboard presses.
    It loads existing data from 'Lifetime.json', or from 'Lifetime.backup' if the primary file is corrupted.
    It also provides functionality to update these statistics.
    """
    def __init__(self):
        try:
            with open("Lifetime.json") as File:
                Lifetime = json.loads(File.read())
                # Initialize variables with data from file
                self.totalLeft = Lifetime["Total Left"]
                self.totalRight = Lifetime["Total Right"]
                self.totalMiddle = Lifetime["Total Middle"]
                self.totalScrolls = Lifetime["Total Scrolls"]
                self.totalPressed = Lifetime["Total Pressed"]
                self.totalLetters = Lifetime["Total Letters"]
                # Track the last recorded values for each statistic
                self.lastLeft = self.totalLeft
                self.lastRight = self.totalRight
                self.lastMiddle = self.totalMiddle
                self.lastScrolls = self.totalScrolls
                self.lastPressed = self.totalPressed
            # Create a backup of the current state
            with open("Lifetime.backup", "w") as File:
                File.write(json.dumps(Lifetime, indent=4))
        except:
            # Handle corrupted file by loading from backup
            with open("Lifetime.backup") as File:
                Lifetime = json.loads(File.read())
            # Save the backup data back to the main file
            with open("Lifetime.json", "w") as File:
                File.write(json.dumps(Lifetime, indent=4))
            # Reload variables from the now restored file
            with open("Lifetime.json") as File:
                Lifetime = json.loads(File.read())
                self.totalLeft = Lifetime["Total Left"]
                self.totalRight = Lifetime["Total Right"]
                self.totalMiddle = Lifetime["Total Middle"]
                self.totalScrolls = Lifetime["Total Scrolls"]
                self.totalPressed = Lifetime["Total Pressed"]
                self.totalLetters = Lifetime["Total Letters"]
                self.lastLeft = self.totalLeft
                self.lastRight = self.totalRight
                self.lastMiddle = self.totalMiddle
                self.lastScrolls = self.totalScrolls
                self.lastPressed = self.totalPressed
            # Display an error message to the user about the restoration
            ctypes.windll.user32.MessageBoxW(0, u"Error: The save file seems corrupted. Loaded backup instead.", u"Error", 0)

# Variables instance for tracking lifetime statistics
Variables = LifetimeClass()

class DailyClass():
    """
    Manages daily statistics for mouse clicks and keyboard presses.
    It loads existing data from 'Daily.json', or from 'Daily.backup' if the primary file is corrupted.
    It also provides functionality to update these daily statistics.
    """
    def __init__(self):
        try:
            with open("Daily.json") as dailyFile:
                Daily = json.loads(dailyFile.read())
                # Initialize daily statistics from file
                self.dailyLeft = Daily["Daily Left"]
                self.dailyRight = Daily["Daily Right"]
                self.dailyMiddle = Daily["Daily Middle"]
                self.dailyScrolls = Daily["Daily Scrolls"]
                self.dailyPressed = Daily["Daily Pressed"]
                self.dailyLetters = Daily["Daily Letters"]
                # Track the last recorded daily values for throttling saves
                self.dailyLastLeft = self.dailyLeft
                self.dailyLastRight = self.dailyRight
                self.dailyLastMiddle = self.dailyMiddle
                self.dailyLastScrolls = self.dailyScrolls
                self.dailyLastPressed = self.dailyPressed
            # Create a daily backup of the current state
            with open("Daily.backup", "w") as dailyFile:
                dailyFile.write(json.dumps(Daily, indent=4))
        except:
            # Handle corrupted daily file by loading from backup
            with open("Daily.backup") as dailyFile:
                Daily = json.loads(dailyFile.read())
            # Save the backup data back to the main daily file
            with open("Daily.json", "w") as dailyFile:
                dailyFile.write(json.dumps(Daily, indent=4))
            # Reload daily variables from the now restored file
            with open("Daily.json") as dailyFile:
                Daily = json.loads(dailyFile.read())
                self.dailyLeft = Daily["Daily Left"]
                self.dailyRight = Daily["Daily Right"]
                self.dailyMiddle = Daily["Daily Middle"]
                self.dailyScrolls = Daily["Daily Scrolls"]
                self.dailyPressed = Daily["Daily Pressed"]
                self.dailyLetters = Daily["Daily Letters"]
                self.todayDate = Daily["Date"]
                self.dailyLastLeft = self.dailyLeft
                self.dailyLastRight = self.dailyRight
                self.dailyLastMiddle = self.dailyMiddle
                self.dailyLastScrolls = self.dailyScrolls
                self.dailyLastPressed = self.dailyPressed
                self.lastTodayDate = self.todayDate
            # Display an error message to the user about the daily restoration
            ctypes.windll.user32.MessageBoxW(0, u"Error: The save file seems corrupted. Loaded backup instead.", u"Error", 0)

# Initialize daily statistics
daily = DailyClass()

def Quit(systray):
    """
    Terminates the application and all running threads.
    This function is triggered when the user chooses to quit from the system tray icon.
    """
    os._exit(1)  # Exits the script with status 1, effectively stopping all threads

def ShowWindow(systray):
    """
    Opens the GUI window to display statistics.
    This function is triggered from the system tray menu.
    """
    GUI.open_the_window()

def Save():
    """
    Saves the lifetime statistics to 'Lifetime.json'.
    Uses a lock to prevent concurrent access and potential data corruption.
    """
    with Lock:
        with open("Lifetime.json", "w") as File:
            Lifetime = {
                "Total Left": Variables.totalLeft,
                "Total Right": Variables.totalRight,
                "Total Middle": Variables.totalMiddle,
                "Total Scrolls": Variables.totalScrolls,
                "Total Pressed": Variables.totalPressed,
                "Total Letters": Variables.totalLetters
            }
            File.write(json.dumps(Lifetime, indent=4))

def Dsav():
    """
    Saves the daily statistics to 'Daily.json'.
    Uses a lock to prevent concurrent access and potential data corruption.
    """
    with Lock:
        with open("Daily.json", "w") as dailyFile:
            Daily = {
                "Daily Left": daily.dailyLeft,
                "Daily Right": daily.dailyRight,
                "Daily Middle": daily.dailyMiddle,
                "Daily Scrolls": daily.dailyScrolls,
                "Daily Pressed": daily.dailyPressed,
                "Daily Letters": daily.dailyLetters,
                "Date": str(date.today())
            }
            dailyFile.write(json.dumps(Daily, indent=4))

def InitializeMouse():
    """
    Initializes mouse event listeners for clicks and scrolls.
    Updates statistics on mouse events and saves the updated stats.
    """
    def OnClick(x, y, button, pressed):
        if pressed:
            if button == button.left:
                Variables.totalLeft += 1
                daily.dailyLeft += 1
                Save()
                Dsav()
            elif button == button.right:
                Variables.totalRight += 1
                daily.dailyRight += 1
                Save()
                Dsav()
            elif button == button.middle:
                Variables.totalMiddle += 1
                daily.dailyMiddle += 1
                Save()
                Dsav()

    def OnScroll(x, y, dx, dy):
        Variables.totalScrolls += 1
        daily.dailyScrolls += 1
        Save()
        Dsav()

    # Start mouse listener in its own thread
    with mouse.Listener(on_click=OnClick, on_scroll=OnScroll) as listener:
        listener.join()

def InitializeKeyboard():
    """
    Initializes keyboard event listeners for key releases.
    Updates statistics on key press events and saves the updated stats.
    """
    def OnRelease(key):
        Variables.totalPressed += 1
        daily.dailyPressed += 1
        # Increment letter count for specific keys if applicable
        key = str(key).lower()
        if len(key) == 3 and key[1].isalpha():
            Variables.totalLetters[key[1]] = Variables.totalLetters.get(key[1], 0) + 1
            daily.dailyLetters[key[1]] = daily.dailyLetters.get(key[1], 0) + 1
        Save()
        Dsav()

    # Start keyboard listener in its own thread
    with keyboard.Listener(on_release=OnRelease) as listener:
        listener.join()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", 5069))  # Use port 5069 
    server_socket.listen(1)
    print("Feedback server running and waiting for connections...")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} established.")
        with open('Daily.json', encoding='utf8') as File:
            FileData = json.load(File)
        # The feedback and advice strings need to be updated based on the GUI logic
        try:
            # You would update these messages based on the current GUI feedback and advice
            feedback_message, advice_message = GUI.generateDynamicFeedback(FileData)
            message_terminator = "@@@"
            full_message = f"Feedback: {feedback_message}\nAdvice: {advice_message}{message_terminator}"
            client_socket.sendall(full_message.encode("utf-8"))
            print(full_message)
        except Exception as e:
            print(f"Error sending message: {e}")
        
        client_socket.close()
# Define system tray options and start the tray icon
menu_options = (("Show Result", None, ShowWindow),)
systray = SysTrayIcon("Health_tracker.ico", "Input Activity Tracker", menu_options, on_quit=Quit)
systray.start()

# Initialize and start threads for mouse and keyboard monitoring, and date checking
MouseThread = threading.Thread(target=InitializeMouse)
KeyboardThread = threading.Thread(target=InitializeKeyboard)
DateCheckerThread = threading.Thread(target=CheckDate)
# Start the feedback server in a separate thread
Thread(target=start_server, daemon=True).start()
MouseThread.start()
KeyboardThread.start()
DateCheckerThread.start()
# Join threads to ensure they complete
MouseThread.join()
KeyboardThread.join()
