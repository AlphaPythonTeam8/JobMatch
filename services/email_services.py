import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve Mailtrap credentials from environment variables
MAILTRAP_USERNAME = os.getenv('MAILTRAP_USERNAME')
MAILTRAP_PASSWORD = os.getenv('MAILTRAP_PASSWORD')

def send_verification_email(email_to, token):
    # SMTP settings from Mailtrap
    smtp_server = 'sandbox.smtp.mailtrap.io'
    smtp_port = 2525
    
    # Email content
    sender_email = "from@example.com"  # This can be any email address for testing
    subject = "Verify your email"
    body = f"""\
Subject: {subject}

Hi,
Please click on the link below to verify your email address:
http://127.0.0.1:8000/verify_email?token={token}
"""

    # Create the email message
    message = MIMEText(body)
    message['From'] = sender_email
    message['To'] = email_to
    message['Subject'] = subject

    # Send the email via Mailtrap's SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.login(MAILTRAP_USERNAME, MAILTRAP_PASSWORD)
        server.sendmail(sender_email, [email_to], message.as_string())
    
    return f"Verification email sent to {email_to}"
