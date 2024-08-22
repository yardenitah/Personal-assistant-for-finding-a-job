import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
from DBManager import DBManager

load_dotenv()


class EmailManager:
    def __init__(self):
        self.email_user = os.getenv('EMAIL')
        self.email_pass = os.getenv('EMAIL_PASSWORD')
        self.imap_server = "imap.gmail.com"

        # Debugging prints
        print(f"EMAIL_USER: {self.email_user}")
        print(f"EMAIL_PASS: {self.email_pass}")

        self.mail = None

    def connect(self):
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_user, self.email_pass)
            print("Connected to the email server successfully.")
        except Exception as e:
            print(f"Failed to connect to the email server: {e}")

    def disconnect(self):
        if self.mail:
            self.mail.logout()
            print("Disconnected from the email server.")

    def search_emails(self, subject=None, from_email=None, since=None):
        try:
            self.mail.select("inbox")
            search_criteria = []

            if subject:
                search_criteria.append(f'SUBJECT "{subject}"')
            if from_email:
                search_criteria.append(f'FROM "{from_email}"')
            if since:
                search_criteria.append(f'SINCE "{since}"')

            search_query = " ".join(search_criteria)
            status, messages = self.mail.search(None, search_query)

            email_ids = messages[0].split()
            return email_ids

        except Exception as e:
            print(f"An error occurred while searching for emails: {e}")
            return []

    def fetch_email(self, email_id):
        try:
            status, msg_data = self.mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if "attachment" not in content_disposition:
                                if content_type == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    return subject, body
                    else:
                        body = msg.get_payload(decode=True).decode()
                        return subject, body

        except Exception as e:
            print(f"An error occurred while fetching the email: {e}")
            return None, None

    def process_emails(self, email_ids):
        db_manager = DBManager()

        for email_id in email_ids:
            subject, body = self.fetch_email(email_id)
            if subject and body:
                print(f"Subject: {subject}")
                print(f"Body: {body}\n")

                # You can add logic to extract the company name and response from the email
                company_name = self.extract_company_name(subject, body)
                response = self.determine_response(subject, body)

                if company_name and response:
                    db_manager.edit_line_by_company_name(company_name, answer=response)

    def extract_company_name(self, subject, body):
        # Implement your logic to extract company name from the subject or body
        # This is a placeholder implementation
        return "Company ABC"

    def determine_response(self, subject, body):
        # Implement your logic to determine if the response is positive or negative
        # This is a placeholder implementation
        if "interview" in body.lower() or "congratulations" in body.lower():
            return "yes"
        else:
            return "no"

    def check_for_new_responses(self):
        self.connect()
        email_ids = self.search_emails(since="01-Jan-2024")  # Adjust the date as needed
        if email_ids:
            self.process_emails(email_ids)
        self.disconnect()
