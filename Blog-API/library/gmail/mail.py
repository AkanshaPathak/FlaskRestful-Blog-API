from __future__ import print_function
import httplib2
from apiclient import discovery
from oauth2client import tools
from library.gmail import sendemail
import argparse
import os
import os
from oauth2client.file import Storage
from oauth2client import client

try:

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

from library.gmail import auth


def get_labels():
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


SCOPES = 'https://mail.google.com/'
cwd_dir = os.getcwd()
CLIENT_SECRET_FILE = os.path.join(cwd_dir, 'library/gmail/client_secret.json')
APPLICATION_NAME = 'Gmail API Python Quickstart'
authInst = auth.auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.get_credentials()

http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)


def mail_otp(receiver, pin_code, username):
    send_inst = sendemail.SendEmail(service)
    message = send_inst.create_otp('your-email@gmail.com', receiver, 'your-organisation OTP Assistant',
                                   pin_code, username)
    send_inst.send_message('me', message)


def mail_info(receiver, user):
    send_inst = sendemail.SendEmail(service)
    message = send_inst.create_message('your-email@gmail.com', receiver,
                                       'We will contact you soon', user)
    send_inst.send_message('me', message)


def mail_me(name, sender, mobile, message):
    send_inst = sendemail.SendEmail(service)
    message = send_inst.create_message_for_me('your-email@gmail.com', 'your-email@gmail.com',
                                              'someone want to contact', name, sender,
                                              mobile, message)
    send_inst.send_message('me', message)
