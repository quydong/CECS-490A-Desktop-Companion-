import tkinter as tk
import socket
import threading

# Global variable to store the Windows PC IP
windows_ip = None

# Function to discover Windows PC
def find_windows_pc():
    global windows_ip
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.sendto(b"DISCOVER_WINDOWS_PC_REQUEST", ('<broadcast>', 44555))
            sock.settimeout(10)  # Increased timeout
            data, addr = sock.recvfrom(1024)
            windows_ip = addr[0]
            print(f"Discovered Windows PC IP: {windows_ip}")
            ip_label.config(text="Windows PC IP: " + windows_ip)
    except socket.timeout:
        print("Discovery timed out. Windows PC not found.")
        ip_label.config(text="Discovery timed out. Try manual entry.")
    except Exception as e:
        print(f"Error during discovery: {e}")
        ip_label.config(text=f"Error: {e}")

def send_volume_command(volume_command):
    global windows_ip
    if windows_ip:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((windows_ip, 65432))
                s.sendall(volume_command.encode())
                result_label.config(text=f"{volume_command} command sent")
        except Exception as e:
            result_label.config(text=f"Error: {e}")
# Function to send command
def send_command():
    global windows_ip
    if not windows_ip:
        windows_ip = ip_entry.get()  # Use manually entered IP if discovery failed

    command = command_entry.get()
    if windows_ip:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((windows_ip, 65432))
                s.sendall(command.encode())
                result_label.config(text="Command sent")
        except Exception as e:
            result_label.config(text=f"Error: {e}")
    else:
        result_label.config(text="No Windows PC IP available. Enter manually or restart app.")

# Set up the tkinter window
window = tk.Tk()
window.title("Command Sender")

ip_label = tk.Label(window, text="Discovering Windows PC IP...")
ip_label.pack()

tk.Label(window, text="Manual IP Entry (if needed):").pack()
ip_entry = tk.Entry(window, width=50)
ip_entry.pack()

volume_up_button = tk.Button(window, text="Volume Up", command=lambda: send_volume_command("volume_up"))
volume_up_button.pack()

volume_down_button = tk.Button(window, text="Volume Down", command=lambda: send_volume_command("volume_down"))
volume_down_button.pack()
tk.Label(window, text="Enter Command:").pack()
command_entry = tk.Entry(window, width=50)
command_entry.pack()

send_button = tk.Button(window, text="Send Command", command=send_command)
send_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

# Start IP discovery in a separate thread on application start
threading.Thread(target=find_windows_pc, daemon=True).start()

window.mainloop()

