import imaplib
import email
from email.header import decode_header
import time
from datetime import datetime
import os 
from dotenv import load_dotenv 
import json

# Load environment variables from .env file
load_dotenv()

# Email account credentials
EMAIL = os.getenv("EMAIL")  # Replace with your email
PASSWORD = os.getenv("PASSWORD")  # Replace with your app-specific password
IMAP_SERVER = os.getenv("IMAP_SERVER")  # Default to Gmail IMAP server

# Logging to a file 
LOG_FILE = "email_agent.log" 
def log_message(message):
    """Log messages to a file."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")     

def decode_subject(subject):
    """Decode email subject with proper encoding."""
    decoded_subject = decode_header(subject)[0][0]
    if isinstance(decoded_subject, bytes):
        try:
            return decoded_subject.decode()
        except:
            return decoded_subject.decode("utf-8", errors="ignore")
    return decoded_subject

def fetch_top_emails(num_emails=5):
    """Fetch details of the top N emails from the inbox."""
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("INBOX")

        # Search for all emails in the inbox
        _, message_numbers = mail.search(None, "ALL")
        message_numbers = message_numbers[0].split()[-num_emails:]  # Get the latest N emails

        emails = []
        for num in message_numbers:
            # Fetch email by ID
            _, msg_data = mail.fetch(num, "(RFC822)")
            email_body = msg_data[0][1]
            msg = email.message_from_bytes(email_body)

            # Extract email details
            sender = msg.get("From")
            receiver = msg.get("To")
            subject = decode_subject(msg.get("Subject"))
            date_str = msg.get("Date")

            # Parse date and time
            try:
                email_date = email.utils.parsedate_to_datetime(date_str)
                formatted_date = email_date.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_date = "Unknown Date"

            emails.append({
                "sender": sender,
                "receiver": receiver,
                "subject": subject,
                "date": formatted_date
            })

        mail.logout()
        return emails

    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []

def email_agent():
    """Main function to run the email agent every 10 seconds."""
    JSON_FILE = "email_fetches.json"
    while True:
        fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nFetching emails at {fetch_time}")
        emails = fetch_top_emails(num_emails=5)
        
        if emails:
            for i, email in enumerate(emails, 1):
                print(f"\nEmail {i}:")
                print(f"Date: {email['date']}")
                print(f"Sender: {email['sender']}")
                print(f"Receiver: {email['receiver']}")
                print(f"Subject: {email['subject']}")
            
            # Prepare data to append to JSON file
            fetch_data = {
                "fetch_time": fetch_time,
                "emails": emails
            }
            
            # Read existing JSON file or initialize empty list
            try:
                if os.path.exists(JSON_FILE):
                    with open(JSON_FILE, "r", encoding="utf-8") as json_file:
                        data = json.load(json_file)
                else:
                    data = []
            except json.JSONDecodeError:
                data = []
            
            # Append new fetch data
            data.append(fetch_data)
            
            # Write back to JSON file
            with open(JSON_FILE, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)
            
            log_message(f"Appended email data to {JSON_FILE}")
        else:
            print("No emails fetched or an error occurred.")

        time.sleep(10)  # Wait for 10 seconds before the next fetch

if __name__ == "__main__":
    email_agent()