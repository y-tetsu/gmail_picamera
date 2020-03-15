#!/usr/bin/env python3
#==================
# gmail-controller
#==================

import pickle
import os.path
import json

import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from apiclient import errors

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from httplib2 import Http
from oauth2client import file, client, tools


class Gmail:
    """
    gmail-controller
    """
    def __init__(self, setting):
        self.setting = setting

    def send(self, to_index=None, attachment=None, filename=None):
        """
        send gmail
        """
        if to_index is not None:
            scope = ['https://www.googleapis.com/auth/gmail.send']
            token_pickle = './token.pickle'
            credential = self.setting["credential"]
            creds = None

            if os.path.exists(token_pickle):
                with open(token_pickle, 'rb') as token:
                    creds = pickle.load(token)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(credential, scope)
                    creds = flow.run_local_server()

                with open(token_pickle, 'wb') as token:
                    pickle.dump(creds, token)

            service = build('gmail', 'v1', credentials=creds)
            message = self._create_message(to_index, attachment, filename)
            self._send_message(service, 'me', message)

    def receive(self, from_address=None):
        """
        receive gmail
        """
        message = ""

        if from_address is not None:
            scope = ['https://www.googleapis.com/auth/gmail.readonly']
            token = './token.json'
            credential = self.setting["credential"]

            store = file.Storage(token)
            creds = store.get()

            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets(credential, scope)
                creds = tools.run_flow(flow, store)

            service = build('gmail', 'v1', http=creds.authorize(Http()))
            date, message = self._get_message(service, from_address)

        return date, message

    def _create_message(self, to_index, attachment, filename):
        """
        create mesasge
        """
        sender = self.setting["sender_address"]
        to = self.setting["user_addresses"][to_index]
        subject = self.setting["subject"]
        message_text = self.setting["message"]

        if str(attachment).endswith('.mp4'):
            message = MIMEMultipart()
            message['from'] = sender
            message['to'] = to
            message['subject'] = subject

            msg_txt = MIMEText(message_text)
            message.attach(msg_txt)

            try:
                msg = MIMEBase('video', 'mp4')
                file_location = os.path.abspath(attachment)
                fattachment = open(file_location, "rb")
                msg.set_payload((fattachment).read())
                encoders.encode_base64(msg)
                msg.add_header("Content-Disposition", "attachment", filename=filename)
                message.attach(msg)
            except:
                print("There is no file here")
        else:
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

    def _get_message(self, service, from_address):
        """
        get mesasge
        """
        message = ""
        messages = service.users().messages()
        msg_list = messages.list(userId='me', maxResults=20).execute()

        # get first message
        for msg in msg_list['messages']:
            topid = msg['id']
            msg = messages.get(userId='me', id=topid).execute()
            headers = msg['payload']['headers']
            date = ""

            for header in headers:
                if header['name'] == 'Date':
                    date = header['value']
                if header['name'] == 'From':
                    if header['value'] == "<" + from_address + ">":
                        print(header['value'])
                        print(date, msg['snippet'])
                        message = msg['snippet']
                        break

            if message:
                break

            date = ""

        return date, message


if __name__ == '__main__':
    setting = {
        "sender_address": "SENDER_ADDRESS",
        "user_addresses": [
            "USER_ADDRESS1",
            "USER_ADDRESS2"
        ],
        "credential": "CREDENTIAL",
        "subject": "SUBJECT",
        "message": "MESSAGE"
    }

    setting_file = './setting.json'

    if os.path.isfile(setting_file):
        with open(setting_file) as f:
            setting = json.load(f)

    gmail = Gmail(setting)

    for index, user_address in enumerate(gmail.setting["user_addresses"]):
        date, message = gmail.receive(user_address)
        if message:
            gmail.send(to_index=0)
