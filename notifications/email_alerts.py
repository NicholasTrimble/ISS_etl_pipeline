import smtplib
from email.message import EmailMessage

# Config
SENDER_EMAIL = "your_email@example.com"
SENDER_APP_PASSWORD = "YOUR_APP_PASSWORD"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

def send_email_notification(to_email, subject_text, body_text):
    """Send email to a single recipient."""

    msg = EmailMessage()
    msg.set_content(body_text)
    msg['Subject'] = subject_text
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            smtp.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as error:
        print(f"Failed to send to {to_email}: {error}")

def send_emails_to_users(user_list, subject_text, body_text_template, app_url="http://yourapp.com"):
    """Send emails to multiple users with unsubscribe link."""

    for user in user_list:
        email = user["email"]
        name = user.get("name", "User")
        unsubscribe_link = f"{app_url}/unsubscribe?email={email}"
        body_text = body_text_template.format(name=name) + f"\n\nTo unsubscribe, click here: {unsubscribe_link}"
        send_email_notification(email, subject_text, body_text)
