from __future__ import print_function
import time
import os.path
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email import errors
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])
        if not messages:
            print("you have no messages")
        else:   
            message_count = 0
            for messages in messages:
                msg = service.users().messages().get(userId='me', id=messages['id']).execute()
                message_count = message_count + 1 
            print("you have" + str(message_count) + "unread messages.")

            new_message_choice = input("would you like to see your messages?").lower()
            if new_message_choice == "yes" or "y":
                for message in messages:
                    msg = service.users().messages().get(userId='me', id=messages['id']).execute()
                    email_data = msg['payload']['headers']
                    for values in email_data:
                        name = values["name"]
                        if name == "From":
                            from_name = values["value"]
                            print("You have a new message from:" + from_name)
                            print("    " + msg['snippet'] + "...")
                            print("\n")
                            time.sleep(1)
            else:
                print ("Good-bye.")  
                message = (service.users().messages().send(userid="me", body="body").execute())
        print("Your message has been sent, ")
    except errors.MessageError as error:
        print("An error occurred: %s" % error)  

def send_message():
    gmail_from = "shivuprasadsppatil@gmail.com"
    gmail_to= "shivuprasadsppatil@gmail.com"
    gmail_subject = "Trying new things."
    gmail_content = "Dude, let me know what this looks like in your mail please."

    message = MIMEText(gmail_content)
    message["to"] = gmail_to
    message["from"] = gmail_from
    message['subject']= gmail_subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {"raw": raw}

                   


if __name__ == '__main__':
    main()
send_message()    