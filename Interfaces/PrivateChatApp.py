import tkinter as tk
from tkinter import scrolledtext

class PrivateChatApp(tk.Tk):
    def __init__(self, username, target_username, private_chat_client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.private_chat_client = private_chat_client
        self.title(f"Chat with {target_username}")
        self.username = username

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

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.display_message(f"{self.username}: {message}", sent=True)
            # Call the send_message method of the PrivateChatClient to send the message via gRPC
            self.private_chat_client.send_message(message)

            self.message_entry.delete(0, tk.END)

    def receive_message(self, message):
        self.display_message(message, sent=False)

    def display_message(self, message, sent=True):
        tag = "sent" if sent else "received"
        # Insert the message with the corresponding tag
        self.chat_history.insert(tk.END, message + '\n', tag)
        self.chat_history.see(tk.END)