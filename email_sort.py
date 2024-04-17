from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os


# Define the subjects to search for
specific_subjects = ["Subject1","Subject2"]#add all subjects

def create_gmail_service():
    # OAuth 2.0 scopes required for accessing Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

    # Check if token file exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'credentials_path.json', SCOPES)#add credentials json file path obtained from google console 
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)
    return service

def search_emails(service, query):
    try:
        # Search for emails matching the query
        response = service.users().messages().list(userId='me', q=query).execute()
        messages = response.get('messages', [])

        if messages:
            return messages
        else:
            print("No emails found.")
            return []
    except Exception as e:
        print("An error occurred:", e)
        return []

def get_email_content(service, message_id):
    try:
        # Retrieve the email message
        message = service.users().messages().get(userId='me', id=message_id).execute()
        
        # Extract subject and body from the email message
        headers = message['payload']['headers']
        subject = next(item['value'] for item in headers if item['name'] == 'Subject')
        body = message['snippet']  # Using 'snippet' for simplicity, you may retrieve the full body if needed
        
        return subject, body
    except Exception as e:
        print("An error occurred while retrieving email content:", e)
        return None, None

def main():
    service = create_gmail_service()
    
    # Search for emails with specific subjects
    all_matching_emails = []
    for subject in specific_subjects:
        query = f"subject:{subject}"
        messages = search_emails(service, query)
        
        # Retrieve content for each matching email
        for message in messages:
            message_id = message['id']
            subject, body = get_email_content(service, message_id)
            if subject and body:
                all_matching_emails.append({"subject": subject, "body": body})

    # Print or process the matching emails
    for email in all_matching_emails:
        print("Subject:", email["subject"])
        print("Body:", email["body"])
        print()  # Add a newline between emails

if __name__ == "__main__":
    main()
