from dotenv import load_dotenv


import os

import psutil #library to access system and hardware information
import smtplib #library to send emails using SMTP
from email.mime.text import MIMEText # library to create email mesages
load_dotenv()

app_password = os.getenv("EMAIL_APP_PASSWORD")
sender_email = "tloutumelo676@gmail.com"
receiver_email = "220128591@student.uj.ac.za"
smtp_server = "smtp.gmail.com"
smtp_port = 465

# --- Disk Usage Configuration ---
threshold = 10  # Alert will be sent when disk space *used* reaches 5%


# --- Function to send email ---
def send_email(subject, body):
    #sends an email with the specified subject and body."""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Set up a secure SMTP server connection
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Email sent successfully!")

    except smtplib.SMTPException as e:
        print(f"Error: Unable to send email. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")







# --- Function to check disk usage ---
def check_disk_usage():
    """Checks disk usage and sends an email if the threshold is exceeded."""
    try:
        disk_usage = psutil.disk_usage('/')  # Get disk usage statistics for the root directory
        used_disk_percent = disk_usage.percent

        print(f"Current disk usage is {used_disk_percent}%")

        if used_disk_percent > threshold:
            # Create the email subject and body
            subject = "Disk Space Alert"
            body = f"Disk usage has exceeded the threshold. Current usage is {used_disk_percent}%."

            # Send the email alert
            send_email(subject, body)

    except Exception as e:
        print(f"Error checking disk usage: {e}")


# --- Main execution block ---
if __name__ == "__main__":
    check_disk_usage()