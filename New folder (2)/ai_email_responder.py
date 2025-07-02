import imaplib
import smtplib
import email
from email.header import decode_header
from email.message import EmailMessage
import openai
import time


GMAIL_USER = "diaaadiaa34@gmail.com"  # Replace with your Gmail address
GMAIL_APP_PASSWORD = "diaa2004"  # Replace with your Gmail App Password
OPENAI_API_KEY = "AIzaSyAxttoT4QK9gh0krLJXeFvCWGWLXLDh9Rg"  # Replace with your OpenAI API key
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

openai.api_key = OPENAI_API_KEY

def fetch_unread_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    mail.select("inbox")
    status, messages = mail.search(None, '(UNSEEN)')
    email_ids = messages[0].split()
    emails = []
    for eid in email_ids:
        status, msg_data = mail.fetch(eid, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                emails.append((eid, msg))
    mail.logout()
    return emails

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                return part.get_payload(decode=True).decode(errors='ignore')
    else:
        return msg.get_payload(decode=True).decode(errors='ignore')
    return ""

def generate_ai_reply(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an email assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content'].strip()

def send_email(to_addr, subject, body):
    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = to_addr
    msg["Subject"] = "Re: " + subject
    msg.set_content(body)
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)

def main():
    print("Checking for unread emails...")
    emails = fetch_unread_emails()
    if not emails:
        print("No unread emails found.")
        return
    for eid, msg in emails:
        from_addr = email.utils.parseaddr(msg.get("From"))[1]
        subject, encoding = decode_header(msg.get("Subject"))[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8', errors='ignore')
        body = get_email_body(msg)
        print(f"Replying to: {from_addr}, Subject: {subject}")
        ai_reply = generate_ai_reply(body)
        send_email(from_addr, subject, ai_reply)
        print("Replied.")

if __name__ == "__main__":
    main() 