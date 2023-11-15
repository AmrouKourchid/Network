import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Server setup
host = '192.168.51.153'
port = 65432
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# List of questions and answers for the quiz
questions_and_answers = [
    ("What is the capital of France?", "Paris"),
    ("What is 3 times 3?", "9"),
    ("What is the name of our galaxy?", "Milky Way")
]

# GUI setup
root = tk.Tk()
root.title("Quiz Game Server")

frame = tk.Frame(root)
frame.pack()

txt_clients = scrolledtext.ScrolledText(frame, height=10, width=100)
txt_clients.pack()
txt_clients.insert(tk.END, "Connected Clients:\n")
txt_clients.config(state=tk.DISABLED)

txt_log = scrolledtext.ScrolledText(frame, height=10, width=100)
txt_log.pack()
txt_log.insert(tk.END, "Game Log:\n")
txt_log.config(state=tk.DISABLED)

# Function to update GUI text
def update_text(widget, text):
    widget.config(state=tk.NORMAL)
    widget.insert(tk.END, text + "\n")
    widget.config(state=tk.DISABLED)

# Client handler function
def handle_client(conn, addr):
    update_text(txt_log, f"New connection from {addr}")

    conn.sendall("Please enter your username: ".encode())
    username = conn.recv(1024).decode().strip()

    update_text(txt_clients, f"User connected with username: {username}")

    score = 0  # Initialize

    # Send questions to the client
    for question, correct_answer in questions_and_answers:
        conn.sendall(question.encode())
        client_answer = conn.recv(1024).decode().lower()

        if client_answer == correct_answer.lower():
            score += 1  # Increment score if the answer is correct
            conn.sendall("Correct!".encode())
            update_text(txt_log, f"{username} answered correctly.")
        else:
            conn.sendall("Incorrect!".encode())
            update_text(txt_log, f"{username} answered incorrectly.")

    # Send the final score to the client
    conn.sendall(f"Your final score is {score}/{len(questions_and_answers)}".encode())
    conn.close()

    # Update the client list and log
    update_text(txt_clients, f"{username} finished with a score of {score}")
    update_text(txt_log, f"{username} disconnected.")

# Main server loop
def start_server():
    update_text(txt_log, "Server is running and waiting for connections...")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        update_text(txt_log, f"Active connections: {threading.activeCount() - 1}")

# Run the server in a separate thread so that it doesn’t block the GUI
threading.Thread(target=start_server).start()

root.mainloop()
