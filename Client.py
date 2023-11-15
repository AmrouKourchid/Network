import socket
import tkinter as tk

def submit_answer():
    answer = answer_var.get()
    client.sendall(answer.encode())
    receive_question()

def receive_question():
    question = client.recv(1024).decode()
    if "Your final score is" in question or "Time is up!" in question:
        question_label.config(text=question)
        answer_entry.config(state='disabled')
        submit_button.config(state='disabled')
    else:
        question_label.config(text=question)
        answer_var.set('')

# Client setup
host = '192.168.48.35'  # Replace with the server's IP address
port = 65432
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Create the main window
root = tk.Tk()
root.title("Quiz Game Client")

# Create and place the widgets
question_label = tk.Label(root, text="", wraplength=300)
question_label.pack(pady=20)

answer_var = tk.StringVar()
answer_entry = tk.Entry(root, textvariable=answer_var)
answer_entry.pack(pady=10)

submit_button = tk.Button(root, text="Submit", command=submit_answer)
submit_button.pack(pady=10)

# Receive the first question
receive_question()

# Run the main loop
root.mainloop()

# Close the client connection when the UI is closed
client.close()