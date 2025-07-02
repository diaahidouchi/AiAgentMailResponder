import imaplib

IMAP_SERVER = "imap.gmail.com"
EMAIL = "diaaadiaa34@gmail.com"
PASSWORD = "diaa2004"

try:

    mail = imaplib.IMAP4_SSL(IMAP_SERVER, 993)
    mail.login(EMAIL, PASSWORD)
    print("Connected successfully.")
except imaplib.IMAP4.error as e:
    
    print(f"IMAP error: {e}")
except Exception as ex:
    print(f"Other error: {ex}")
