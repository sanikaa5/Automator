import os
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow


# Function to create the Gmail service
def create_gmail_service():
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    creds = None

    # Check if token file exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
           flow = InstalledAppFlow.from_client_secrets_file(r"credentials_file_path.json", SCOPES)
           #credentials_file_path.json= insert json file of credentials path
           creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)
    return service

# Function to send email to multiple recipients
def send_email_to_multiple_recipients(service, sender, recipients, subject, message_text, sheets_link):
    message = create_message_with_attachment(sender, recipients, subject, message_text, sheets_link)
    send_message(service, 'me', message)

# Function to create an email message with attachment
def create_message_with_attachment(sender, to, subject, message_text, sheets_link):
    message = MIMEMultipart()
    message['to'] = ', '.join(to)
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    sheets_msg = MIMEText("You can access the Google Sheets here: " + sheets_link)
    message.attach(sheets_msg)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

# Function to send a message
def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print("Message sent successfully!")
    except Exception as e:
        print("An error occurred:", e)

# Usage
if __name__ == "__main__":
    # Create the Gmail service
    gmail_service = create_gmail_service()

    # Example: Sending automatic email to various recipients with a message and Google Sheets link
    sender = "sender@gmail.com"
    recipients = ["receiver@gmail.com", "receiver@gmail.com"]  # Add more recipients as needed
    subject = "Automatic Email with Google Sheets Link"
    message_text = "Hello,\n\nPlease find the details in the attached google sheets link below."
    sheets_link = "google sheets link"
    send_email_to_multiple_recipients(gmail_service, sender, recipients, subject, message_text, sheets_link)
