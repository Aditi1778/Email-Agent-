# Email-Agent 

A Python-based email agent that fetches details (date, time, sender, receiver, and subject) of the top 5 emails from an inbox every 10 seconds using the IMAP protocol. The fetched data is printed to the console, logged to a file, and appended to a single JSON file for persistent storage.
Features

Fetches the latest 5 emails from the inbox every 10 seconds.
Extracts email details: date, sender, receiver, and subject.
Stores fetch results in a single JSON file (email_fetches.json) with timestamps.
Logs operations to email_agent.log.
Uses environment variables for secure email credentials.
Handles email subject decoding and connection errors gracefully.

Prerequisites

Python 3.6+
An email account with IMAP enabled (e.g., Gmail with an app-specific password).
Required Python packages:
imaplib (standard library)
email (standard library)
python-dotenv (for environment variables)
json (standard library)



Setup

Clone the Repository:
git clone https://github.com/your-username/email-agent.git
cd email-agent


Install Dependencies:
pip install python-dotenv


Configure Environment Variables:

Create a .env file in the project root:EMAIL=your_email@gmail.com
PASSWORD=your_app_specific_password
IMAP_SERVER=imap.gmail.com


For Gmail, generate an app-specific password:
Go to Google Account > Security > 2-Step Verification > App passwords.
Create a new app password for "Mail".


For other providers, update IMAP_SERVER (e.g., imap-mail.outlook.com for Outlook).


Enable IMAP:

For Gmail: Settings > See all settings > Forwarding and POP/IMAP > Enable IMAP.



Usage

Run the script:
python email_agent.py


The agent will:

Fetch the top 5 emails every 10 seconds.
Print email details (date, sender, receiver, subject) to the console.
Append fetch results to email_fetches.json.
Log operations to email_agent.log.


Stop the script with Ctrl+C.


File Structure

email_agent.py: Main script for fetching and storing email data.
.env: Environment variables (not tracked in Git; create locally).
email_fetches.json: Output file storing all email fetch results in JSON format.
email_agent.log: Log file for script operations.
README.md: This file.

JSON Output Format
The email_fetches.json file contains a list of fetch objects:
[
    {
        "fetch_time": "2025-06-18 10:37:00",
        "emails": [
            {
                "sender": "sender1@example.com",
                "receiver": "your_email@gmail.com",
                "subject": "Meeting Update",
                "date": "2025-06-18 10:30:00"
            },
            ...
        ]
    },
    ...
]

Notes

Ensure the script has write permissions for email_fetches.json and email_agent.log.
The JSON file grows with each fetch. Consider implementing cleanup for large files.
For non-Gmail providers, verify the IMAP server address and port.

Contributing

Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit changes (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a pull request.
