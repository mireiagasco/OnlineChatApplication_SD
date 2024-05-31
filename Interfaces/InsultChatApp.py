import queue
import tkinter as tk
import threading
from functools import partial
from threading import Condition
import RabbitMQ.RabbitMQbroker


class InsultChatApp:
    def __init__(self, username, client_id):
        self.username = username
        self.client_id = client_id
        self.insults = queue.Queue()
        self.condition = Condition()  # Create a Condition object
        self.queue_name = f"insult_queue_{self.client_id}"

        self.root = tk.Tk()
        self.root.title("Insult Chat App")

        self.chat_display = tk.Text(self.root, height=20, width=50)
        self.chat_display.pack()

        self.insult_entry = tk.Entry(self.root, width=50)
        self.insult_entry.pack()
        self.insult_entry.bind("<Return>", self.send_insult)

        self.send_button = tk.Button(self.root, text="Send Insult", command=self.send_insult)
        self.send_button.pack()

        receive_insult_partial = partial(RabbitMQ.RabbitMQbroker.receive_insult, self.insults, self.condition)
        threading.Thread(target=receive_insult_partial, daemon=True).start()

        # Start a thread to handle insults when added to the queue
        threading.Thread(target=self.receive_insults, daemon=True).start()

    def send_insult(self, event=None):
        insult = self.insult_entry.get()
        if insult:
            RabbitMQ.RabbitMQbroker.send_insult(insult)
            self.insult_entry.delete(0, tk.END)

    def receive_insults(self):
        while True:
            with self.condition:
                self.condition.wait()  # Wait until notified
            if not self.insults.empty():
                insult = self.insults.get()
                self.display_insult(insult)

    def display_insult(self, message):
        self.chat_display.insert(tk.END, f"Insult received: {message}\n")
        self.chat_display.see(tk.END)

    def start(self):
        self.root.mainloop()
