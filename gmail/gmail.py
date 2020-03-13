#!/usr/bin/env python3
#==================
# gmail-controller
#==================

import pickle
import os.path
import json

import base64
from email.mime.text import MIMEText
from apiclient import errors

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Gmail:
    """
    gmail-controller
    """
    def __init__(self, setting):
        self.setting = setting
        self.scope = ['https://www.googleapis.com/auth/gmail.send']

    def send(self, to_index=None):
        """
        send gmail
        """
        token_pickle = self.setting["token_pickle"]
        credential = self.setting["credential"]

        creds = None
        if os.path.exists(token_pickle):
            with open(token_pickle, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credential, self.scope)
                creds = flow.run_local_server()

            with open(token_pickle, 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)
        message = self._create_message(to_index)
        self._send_message(service, 'me', message)

    def _create_message(self, to_index):
        """
        create mesasge
        """
        sender = self.setting["sender_address"]
        to = self.setting["to_addresses"][to_index]
        subject = self.setting["subject"]
        message_text = self.setting["message"]

        message = MIMEText(message_text)
        message['from'] = sender
        message['to'] = to
        message['subject'] = subject
        encode_message = base64.urlsafe_b64encode(message.as_bytes())

        return {'raw': encode_message.decode()}

    def _send_message(self, service, user_id, message):
        """
        send mesasge
        """
        try:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)


if __name__ == '__main__':
    setting = {
        "sender_address": "SENDER_ADDRESS",
        "to_addresses": [
            "TO_ADDRESS1",
            "TO_ADDRESS2"
        ],
        "token_pickle": "TOKEN_PICKLE",
        "credential": "CREDENTIAL",
        "subject": "SUBJECT",
        "message": "MESSAGE"
    }

    setting_file = './setting.json'

    if os.path.isfile(setting_file):
        with open(setting_file) as f:
            setting = json.load(f)

    gmail = Gmail(setting)
    gmail.send(to_index=0)
