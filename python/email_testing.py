# Python version check (optional)
# python3 --version

import smtplib
from email.message import EmailMessage


print("\n=== SMTP EMAIL SENDER ===\n")

# USER INPUTS WITH EXAMPLES

smtp_host = input("SMTP Host (e.g. smtp.gmail.com): ")
smtp_port = int(input("SMTP Port (e.g. 587 for Gmail TLS): "))

smtp_user = input("Your Email (Sender Email e.g. example@gmail.com): ")
smtp_password = input("Your Email Password / App Password (e.g. 16-digit Gmail App Password): ")

receiver_email = input("Receiver Email (e.g. friend@gmail.com): ")

subject = input("Email Subject (e.g. Test Email): ")
body = input("Email Message (e.g. Hello, this is a test email sent): ")


# CREATE EMAIL
msg = EmailMessage()
msg["Subject"] = subject
msg["From"] = smtp_user
msg["To"] = receiver_email
msg.set_content(body)


# SEND EMAIL
try:
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

    print("\n✅ Email sent successfully!")

except Exception as e:
    print(f"\n❌ Failed to send email: {e}")