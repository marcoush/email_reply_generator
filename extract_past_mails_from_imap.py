import imaplib
import email
from email.header import decode_header
import csv
import os


# ---- configuration ----
IMAP_SERVER = "imapserver.net"
IMAP_PORT = 993
USERNAME = "abc@abc.com"
PASSWORD = "password"
KEYWORDS = ["application", "Application", "invitation", "Invitation"]
script_dir = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(script_dir, "past_emails_raw.csv")

# ---- connect ----
imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
imap.login(USERNAME, PASSWORD)
imap.select("INBOX")  # you can select other folders

# ---- search for all emails from this sender ----
status, messages = imap.search(None, f'FROM "{USERNAME}"')
email_ids = messages[0].split()

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "subject", "from", "to", "body"])

    for eid in email_ids:
        res, msg_data = imap.fetch(eid, "(RFC822)")
        if res != "OK":
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # decode subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8", errors="ignore")

                # from / to
                from_ = msg.get("From")
                to_ = msg.get("To")

                # get body (plain text or fallback to html)
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        disp = str(part.get("Content-Disposition"))
                        if ctype == "text/plain" and "attachment" not in disp:
                            body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                            break
                        elif ctype == "text/html" and "attachment" not in disp and not body:
                            body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                else:
                    body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

                # filter by keywords
                text = (subject or "").lower() + " " + (body or "").lower()
                if any(k.lower() in text for k in KEYWORDS):
                    writer.writerow([msg.get("Date"), subject, from_, to_, body])

imap.logout()
print("IMAP export finished.")