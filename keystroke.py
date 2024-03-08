from pynput import keyboard, mouse

# Global counters
keystrokes = 0
mouse_clicks = 0

# Keyboard event listener callback
def on_key_press(key):
    global keystrokes
    keystrokes += 1
    print(f"Keystrokes: {keystrokes}")

# Mouse event listener callback
def on_click(x, y, button, pressed):
    global mouse_clicks
    if pressed:
        mouse_clicks += 1
        print(f"Mouse Clicks: {mouse_clicks}")

# Start listening to keyboard events
keyboard_listener = keyboard.Listener(on_press=on_key_press)
keyboard_listener.start()

# Start listening to mouse events
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()
