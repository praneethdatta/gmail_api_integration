from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import config

# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

# Initialize service as a global variable
service = None
def initialize_service():
    global service
    creds = None
    # Store token as pickle to reuse it
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(config.CLIENT_SECRET_FILE, config.SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)


# Fetch mails service
def fetch_emails():
    global service
    if service is None:
        initialize_service()

    result = service.users().messages().list(userId='me', maxResults=config.EMAILS_LIMIT).execute() # restricting the number of emails to 10 - we can remove this; default is 100
    messages = result.get('messages', [])

    emails = []
    if messages:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = {
                'id': message['id'],
                'from': None,
                'subject': None,
                'message': None,
                'received_at': None
            }
            headers = msg['payload']['headers']
            for header in headers:
                if header['name'] == 'From':
                    email_data['from'] = header['value']
                elif header['name'] == 'Subject':
                    email_data['subject'] = header['value']
                elif header['name'] == 'Date':
                    email_data['received_at'] = header['value']

            email_data['message'] = msg['snippet']
            emails.append(email_data)

    return emails


# Marks email as read service
def mark_email_as_read(email_id):
    global service
    if service is None:
        initialize_service()
    print("inside mark_email_as_read")
    service.users().messages().modify(userId='me', id=email_id, body={'removeLabelIds': ['UNREAD']}).execute()


# Mark email as unread service
def mark_email_as_unread(email_id):
    global service
    if service is None:
        initialize_service()
    print("inside mark_email_as_unread")
    service.users().messages().modify(userId='me', id=email_id, body={'addLabelIds': ['UNREAD']}).execute()


# Mark email to folder service
def move_email_to_folder(email_id, folder_name):
    global service
    if service is None:
        initialize_service()
    label_response = service.users().labels().list(userId='me').execute()
    labels = label_response.get('labels', [])

    label_id = None

    # Print the list of available labels
    # CHAT
    # SENT
    # INBOX
    # IMPORTANT
    # TRASH
    # DRAFT
    # SPAM
    # CATEGORY_FORUMS
    # CATEGORY_UPDATES
    # CATEGORY_PERSONAL
    # CATEGORY_PROMOTIONS
    # CATEGORY_SOCIAL
    # STARRED
    # UNREAD
    # print("List of labels:")
    # for lbl in labels:
        # print(lbl['name'])

    for lbl in labels:
        if lbl['name'] == folder_name:
            label_id = lbl['id']
            break

    if label_id is None:
        raise ValueError(f"Folder '{folder_name}' not found.")

    service.users().messages().modify(
        userId='me',
        id=email_id,
        body={'removeLabelIds': ['INBOX'], 'addLabelIds': [label_id]}
    ).execute()