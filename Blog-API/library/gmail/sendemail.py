from __future__ import print_function

from apiclient import errors

from oauth2client import tools

import base64
import argparse
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import mimetypes
from oauth2client.file import Storage
from oauth2client import client
import httplib2
import os

try:
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class SendEmail:
    def __init__(self, service):
        self.service = service

    @staticmethod
    def create_otp(sender, to, subject, message_text, username=None):
        message = MIMEMultipart("alternative")
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        # Create the plain-text and HTML version of your message
        text = f"""\
        Hi {username},
        Please verify your email address
        OTP: {message_text}
        your-organisation-url"""
        html = f"""\
        <html>
          <body>
            <p>Hi {username},<br><br>
               Please verify your email address<br>
                <h4>To authenticate, please use the following One Time Password (OTP):<h4>
                <br>
                <h2> OTP: {message_text} </h2>
               <a href="your-website-url"><h2>your-organisation</h2></a>
            </p>
            <p>
            Do not share this OTP with anyone. your-organisation takes your account security very 
            seriously. your-organisation Customer Service will never ask you to disclose or 
            verify your your-organisation password, OTP and any information. 
            If you receive a suspicious email with a link to update your account 
            information, do not click on the link—instead,report the email to your-organisation 
            for investigation. 
            <br><br>
            We hope to see you again soon.
            </p>
          </body>
        </html>
        """
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        return {'raw': raw}
        # return {'raw': base64.urlsafe_b64encode(message.as_bytes())}

    @staticmethod
    def create_message(sender, to, subject, user):
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        # Create the plain-text and HTML version of your message
        text = f"""\
              Hi {user},
                Thank you for showing interest in us,
                we will contact you soon and answer your queries
              """
        html = f"""\
              <html>
                <body>
                  <p>Hi {user},<br><br>
                      <p>Thank you for showing interest in our website.<br/>
                        we will contact you soon and try to resolve your queries.</br>
                        you can visit our blog section to explore articles related to tech.
                        <br>
                        <h3>If you want to be a programmer then visit our bootcamp section<h3>
                  <br><br>
                  We hope to see you again soon.
                  </p>
                </body>
              </html>
              """
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        return {'raw': raw}
        # return {'raw': base64.urlsafe_b64encode(message.as_bytes())}

    @staticmethod
    def create_message_for_me(sender, to, subject, user, email, mobile, containt):
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        # Create the plain-text and HTML version of your message
        text = f"""\
              MR, {user},
              want to contact us.
              Details are mentioned below:
              
              User: {user}
              Email: {email}
              Mobile: {mobile}
              Message: {containt}
              """
        html = f"""\
              <html>
                <body>
                  <p>Hi Admin,<br><br>
                      <p>Mr, {user} want to connect us.<br><br>
                      <h4>Details are mentioned below:</h4>
                      <h2> User: {user}<br>
                          Email: {email}<br>
                          Mobile: {mobile}<br>
                          Message: {containt}<br>
                      </h2>
                </body>
              </html>
              """
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        return {'raw': raw}
        # return {'raw': base64.urlsafe_b64encode(message.as_bytes())}

    @staticmethod
    def create_message_with_attachment(sender, to, subject, message_text, file):
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        msg = MIMEText(message_text)
        message.attach(msg)

        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(file, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(file, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(file, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(file, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def send_message(self, user_id, message):
        """Send an email message.

      Args:
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

      Returns:
        Sent Message.
      """
        try:
            message = (self.service.users().messages().send(userId=user_id, body=message)
                       .execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
