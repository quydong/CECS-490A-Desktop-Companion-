import tkinter as tk
import socket
import threading
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
def get_server_ip():
    # Attempt to find the server's IP address
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS, or any other public server
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return "IP Not Found"
def adjust_volume(change):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    currentVolumeDb = volume.GetMasterVolumeLevel()
    volume.SetMasterVolumeLevel(currentVolumeDb + change, None)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 65432))  # Listen on all interfaces, port 65432
    server.listen()

    while True:
        client, address = server.accept()
        threading.Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    try:
        while True:
            command = client.recv(1024).decode()
            if command == "volume_up":
                adjust_volume(1.0)  # Increase volume
            elif command == "volume_down":
                adjust_volume(-1.0)  # Decrease volume
            elif command:
                command_display.insert(tk.END, f"Received command: {command}\n")
            else:
                break
    finally:
        client.close()

# Tkinter window setup
window = tk.Tk()
window.title("Command Receiver")

# Display the server's IP address
server_ip = get_server_ip()
ip_label = tk.Label(window, text=f"Server IP: {server_ip}")
ip_label.pack()

command_display = tk.Text(window, height=10, width=50)
command_display.pack()

# Start the server automatically
threading.Thread(target=start_server, daemon=True).start()

window.mainloop()
