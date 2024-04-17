from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
from email.mime.text import MIMEText
import os

# Define the scopes for accessing Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
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
    return creds

def reply_to_specific_subject(service, subject_keyword, reply_message):
    # List messages matching the query
    results = service.users().messages().list(userId='me', q=f'subject:{subject_keyword}').execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            msg_id = msg['id']
            msg_payload = msg['payload']
            headers = msg_payload['headers']
            for header in headers:
                if header['name'] == 'From':
                    from_address = header['value']
                if header['name'] == 'Subject':
                    subject = header['value']

            # Compose the reply message
            reply = MIMEText(reply_message)
            reply['to'] = from_address
            reply['subject'] = f"Re: {subject}"

            # Create the raw message
            raw_message = base64.urlsafe_b64encode(reply.as_bytes()).decode('utf-8')
            message = {'raw': raw_message}

            # Send the reply
            service.users().messages().send(userId='me', body=message).execute()

            print("Replied to:", from_address)

def main():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    subject_keyword = 'specific subject keyword'
    reply_message = 'Your reply message here.'
    reply_to_specific_subject(service, subject_keyword, reply_message)

if __name__ == '__main__':
    main()
