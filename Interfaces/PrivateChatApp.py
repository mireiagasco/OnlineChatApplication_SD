import time
import tkinter as tk
from tkinter import scrolledtext


class PrivateChatApp(tk.Tk):
    def __init__(self, username, target_username, private_chat_client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.private_chat_client = private_chat_client
        self.title(f"Chat with {target_username}")
        self.username = username
        self.target_username = target_username

        # Create scrolled text widget to display messages
        self.chat_history = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.chat_history.pack(expand=True, fill=tk.BOTH)

        # Create entry widget to type messages
        self.message_entry = tk.Entry(self)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Create send button
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        # Apply formatting to tags
        self.chat_history.tag_config("sent", justify="right")
        self.chat_history.tag_config("received", justify="left")
        self.chat_history.tag_config("disconnect", justify="center")

        # Bind the window close event to a function
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.display_message(f"{self.username}: {message}", status='sent')
            # Call the send_message method of the PrivateChatClient to send the message via gRPC
            self.private_chat_client.send_message(message)

            self.message_entry.delete(0, tk.END)

    def receive_message(self, message=None, disconnect=False):
        if disconnect:
            self.display_message(f"User {self.target_username} disconnected", status='disconnect')
            self.display_message("Disconnecting...", status='disconnect')
            time.sleep(3)
            self.on_close()
        else:
            self.display_message(f"{self.target_username}: {message.content}", status='received')

    def display_message(self, message, status):
        tag = None

        if status == 'sent':
            tag = "sent"
        if status == 'received':
            tag = "received"
        if status == 'disconnect':
            tag = "disconnect"

        # Insert the message with the corresponding tag
        self.chat_history.insert(tk.END, message + '\n', tag)
        self.chat_history.see(tk.END)

    def on_close(self):
        self.private_chat_client.disconnect()
        self.destroy()
