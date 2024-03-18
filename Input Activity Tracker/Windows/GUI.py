import reset
import PySimpleGUI as gui
import json
import time
import threading
import os


# Set the theme for PySimpleGUI
gui.theme('Black')

# Flag to track if the window is already open to prevent multiple instances
is_opened = False

def generateDynamicFeedback(dailyData):
        feedback = ""
        advice = ""
        # Correcting the key names according to your JSON structure
        if dailyData['Daily Pressed'] > (dailyData['Daily Left'] + dailyData['Daily Right']):
            feedback += "You're focusing more on typing today. "
            advice += "Consider using ergonomic keyboards or wrist rests to reduce strain."
        else:
            feedback += "Your mouse activity is high. "
            advice += "Explore and memorize keyboard shortcuts for your most-used applications to reduce mouse usage."    
        # Add health tips based on activity
        return feedback,advice


def open_the_window():
    global is_opened

    # Check if the window is already open to prevent multiple instances
    if not is_opened:
        # Mark the window as open
        is_opened = True
    
        # Read data from JSON files
        # This operation loads the current state of lifetime and daily metrics
        with open("Lifetime.json") as File:
            Lifetime = json.loads(File.read())
            totalLeft = Lifetime["Total Left"]
            totalRight = Lifetime["Total Right"]
            totalMiddle = Lifetime["Total Middle"]
            totalScrolls = Lifetime["Total Scrolls"]
            totalPressed = Lifetime["Total Pressed"]
            totalLetters = Lifetime["Total Letters"]

        with open("Daily.json") as DFile:
            Daily = json.loads(DFile.read())
            dailyLeft = Daily["Daily Left"]
            dailyRight = Daily["Daily Right"]
            dailyMiddle = Daily["Daily Middle"]
            dailyScrolls = Daily["Daily Scrolls"]
            dailyPressed = Daily["Daily Pressed"]
            dailyLetters = Daily["Daily Letters"]

        # Define the layout of the GUI
        # This layout includes statistics for both lifetime and daily metrics
        col1 = [
            [gui.Image("Mouse.png",pad=(35,15),size=(50,50))], 
            [gui.Text("Total Left Clicks: "+"{:,}".format(totalLeft), key="_TotalLeft_", size=(18,1))],
            [gui.Text("Total Right Clicks: "+"{:,}".format(totalRight), key="_TotalRight_", size=(18,1))],
            [gui.Text("Total Middle Clicks: "+"{:,}".format(totalMiddle), key="_TotalMiddle_", size=(18,1))],
            [gui.Text("Total Scrolls: "+"{:,}".format(totalScrolls), key="_TotalScrolls_", size=(18,1))],
            [gui.Text(pad=(None, 2))],
            [gui.Text("Daily Left Clicks: " + "{:,}".format(dailyLeft), key="_DailyLeft_", size=(18, 1))],
            [gui.Text("Daily Right Clicks:  " + "{:,}".format(dailyRight), key="_DailyRight_", size=(18, 1))],
            [gui.Text("Daily Middle Clicks: " + "{:,}".format(dailyMiddle), key="_DailyMiddle_", size=(18, 1))],
            [gui.Text("Daily Scrolls: " + "{:,}".format(dailyScrolls), key="_DailyScrolls_", size=(18, 1))]
        ]
        col2 = [
            [gui.Image("Keyboard.png",pad=(80,15),size=(50,50))],
            [gui.Text("Total Keystrokes: "+"{:,}".format(totalPressed), key="_TotalPressed_", size=(21,1))],
            [gui.Text("Most Pressed Key:  " + (max(totalLetters, key=totalLetters.get, default='N/A') if totalLetters else "N/A").upper(), key="_TotalLetters_", size=(21,1))],
            [gui.Text("Daily Keystrokes:  "+"{:,}".format(dailyPressed), key="_DailyPressed_", size=(21,1))],
            [gui.Text("Daily Most Pressed Key: "+(max(totalLetters, key=totalLetters.get, default='N/A') if totalLetters else "N/A").upper(), key="_DailyLetters_", size=(21,1))],
            [gui.Text(pad=(None, 2))],
            [gui.Text("Feedback: ", key="_Feedback_", size=(21, 2),text_color='red')], 
            [gui.Text("Advice: ", key="_Advice_", size=(21, 3),text_color='green')]         
        ]

        layout = [
            [gui.Column(col1, element_justification='l', justification="left"), gui.Column(col2, element_justification='r', justification="right", pad=(0,0))]
        ]

        # Initialize and display the window with the defined layout
        window = gui.Window('Input Activity Tracker', layout, use_default_focus=False, finalize=True, icon="Health_tracker.ico", location=(None, None),grab_anywhere=True)

        def update_the_window():
            # Continuously update the window with new data at fixed intervals
            StartTime = time.time()  # Record the start time for interval tracking
            while is_opened:
                if time.time() - StartTime >= 0.01:  # Update every 0.1 seconds
                    StartTime = time.time()  # Reset the start time
                    try:
                        # Attempt to re-read the data from JSON files and update GUI elements
                        with open("Lifetime.json") as File:
                            Lifetime = json.loads(File.read())
                            totalLeft = Lifetime["Total Left"]
                            totalRight = Lifetime["Total Right"]
                            totalMiddle = Lifetime["Total Middle"]
                            totalScrolls = Lifetime["Total Scrolls"]
                            totalPressed = Lifetime["Total Pressed"]
                            totalLetters = Lifetime["Total Letters"]

                        with open("Daily.json") as File:
                            Daily = json.loads(File.read())
                            dailyLeft = Daily["Daily Left"]
                            dailyRight = Daily["Daily Right"]
                            dailyMiddle = Daily["Daily Middle"]
                            dailyScrolls = Daily["Daily Scrolls"]
                            dailyLetters = Daily["Daily Letters"]
                            dailyPressed = Daily["Daily Pressed"]

                        # Update the window elements with the new data
                        window["_TotalPressed_"].update("Total Keystrokes: "+"{:,}".format(totalPressed))
                        window["_TotalLeft_"].update("Total Left Clicks: "+"{:,}".format(totalLeft))
                        window["_TotalMiddle_"].update("Total Middle Clicks: "+"{:,}".format(totalMiddle))
                        window["_TotalRight_"].update("Total Right Clicks: "+"{:,}".format(totalRight))
                        window["_TotalScrolls_"].update("Total Scrolls: "+"{:,}".format(totalScrolls))
                        window["_TotalLetters_"].update("Most Pressed Key:  "+max(totalLetters, key=totalLetters.get).upper())
                        window["_DailyPressed_"].update("Daily Keystrokes:  " + "{:,}".format(dailyPressed))
                        window["_DailyLeft_"].update("Daily Left Clicks: "+"{:,}".format(dailyLeft))
                        window["_DailyMiddle_"].update("Daily Middle Clicks: "+"{:,}".format(dailyMiddle))
                        window["_DailyRight_"].update("Daily Right Clicks:  "+"{:,}".format(dailyRight))
                        window["_DailyScrolls_"].update("Daily Scrolls: "+"{:,}".format(dailyScrolls))
                        window["_DailyLetters_"].update("Daily Most Pressed Key: "+max(dailyLetters, key=dailyLetters.get).upper())
                        feedback_message, advice_message = generateDynamicFeedback(Daily)
                        window["_Feedback_"].update("Feedback: " + feedback_message)
                        window["_Advice_"].update("Advice: " + advice_message)
                    except json.JSONDecodeError:
                        # Handle potential JSON decoding errors gracefully
                        pass

                
        # Start a separate thread to update the window, allowing the main thread to remain responsive
        update_the_window_thread = threading.Thread(target=update_the_window, daemon=True)
        update_the_window_thread.start()


        # Main loop to keep the window open and responsive until the user chooses to close it
        while True:
            event, values = window.read()
            if event == gui.WIN_CLOSED:
                # Close the window and clean up resources if the user closes the window
                is_opened = False
                break
        window.close()
