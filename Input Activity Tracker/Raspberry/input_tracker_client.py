import tkinter as tk
import socket
import threading

def fetch_info_from_server(host, port):
    message_terminator = "@@@"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            chunks = []
            while True:
                chunk = s.recv(4096).decode("utf-8")  # Using a larger buffer for demonstration
                if message_terminator in chunk:
                    chunks.append(chunk[:chunk.find(message_terminator)])
                    break
                chunks.append(chunk)
            message = "".join(chunks)
            return message.split("\n")
    except Exception as e:
        return [f"Error: {e}"]

def update_text():
    global feedback_label, advice_text
    feedback, advice = fetch_info_from_server(server_host, port)
    feedback_label.config(text=feedback)
    
    # Update advice text with centered alignment
    advice_text.configure(state="normal")
    advice_text.delete("1.0", tk.END)
    advice_text.insert("1.0", advice)
    advice_text.tag_add('center', "1.0", "end")  # Apply the 'center' tag to newly inserted text
    advice_text.configure(state="disabled")
    
    root.after(1000, update_text)

def create_transparent_window():
    global root, feedback_label, advice_text
    root = tk.Tk()
    root.title("")

    # Remove window border and title bar and set the window position
    window_height = 60
    x_offset = 23
    y_offset = 480 - window_height
    root.geometry(f"+{x_offset}+{y_offset}")

    root.overrideredirect(True)

    # Feedback Label
    feedback_label = tk.Label(root, text="Fetching feedback...", font=('Helvetica', 12), fg="red")
    feedback_label.pack()
    feedback_label.pack(pady=(5, 0))  # Add padding at the top of the feedback label

    # Advice Text Widget
    advice_text = tk.Text(root, height=2, width=81, font=('Helvetica', 12), fg="green",
                          bg=root.cget("background"), bd=0, wrap="word")
    advice_text.tag_configure('center', justify='center')  # Configure a tag for centered text
    advice_text.insert("1.0", "Fetching advice...")
    advice_text.tag_add('center', "1.0", "end")
    advice_text.configure(state="disabled")
    advice_text.pack(pady=(5, 0))
    update_text()

    root.mainloop()

if __name__ == "__main__":
    server_host = 'DESKTOP-EOA4FK6'  # Replace with the server's IP address
    port = 5069  # The port number should match the server's port
    # Run the create_transparent_window function to start the GUI
    create_transparent_window()
