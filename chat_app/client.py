import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog

HOST = "127.0.0.1"  # Change to server LAN IP
PORT = 5000


class ChatClient:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Python LAN Chat")

        self.chat_area = scrolledtext.ScrolledText(self.window, state='disabled')
        self.chat_area.pack(padx=10, pady=10)

        self.msg_entry = tk.Entry(self.window)
        self.msg_entry.pack(fill=tk.X, padx=10)
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_btn.pack(pady=5)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        self.username = tk.simpledialog.askstring(
            "Username", "Enter your name:"
        )

        self.client.send(self.username.encode())


        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.window.mainloop()

    def send_message(self, event=None):
        msg = self.msg_entry.get()
        self.msg_entry.delete(0, tk.END)

        if msg:
            self.client.send(msg.encode())
            if msg == "/exit":
                self.client.close()
                self.window.destroy()

    def receive_messages(self):
        while True:
            try:
                msg = self.client.recv(1024).decode()
                self.chat_area.config(state='normal')
                self.chat_area.insert(tk.END, msg + "\n")
                self.chat_area.config(state='disabled')
                self.chat_area.yview(tk.END)
            except:
                break


ChatClient()
