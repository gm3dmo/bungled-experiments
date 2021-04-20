#!/usr/bin/env python

import string
import smtpd
import asyncore
import datetime
import base64
import email
 
"""
Stub email server to listen on a port and print the messages it
receives. Useful for troubleshooting problems with things that send mail.

##How to use it?
Set the email server and listen port to the hostname where you are running this script.
Run this script and watch it receiving mail.

Set decode_payload to False if you don't want the body.

Useful for scooping up password reset links.
"""

listen_port = 10025
listen_address = '0.0.0.0'
decode_payload = True
 
class CustomSMTPServer(smtpd.SMTPServer):
    mail_count = 0
    def process_message(self, peer, mailfrom, rcpttos, data):
        received_time = datetime.datetime.now()
        message_lines = data.split('\n')
        for line in message_lines:
            if line.startswith('Subject:'):
                CustomSMTPServer.mail_count = CustomSMTPServer.mail_count + 1
                pieces = line.split(' ')
                status = line
                print('| {counter:10} | {component} | {status} | {rt}' .format(counter=CustomSMTPServer.mail_count, component=pieces[1], status=status, rt=received_time))
                if decode_payload:
                    print('===========================')
                    raw_email_string = data.decode('utf-8')
                    msg = email.message_from_string(raw_email_string)
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print ('From : ' + email_from + '\n')
                    print ('Subject : ' + email_subject + '\n')
                    print(msg.get_payload(decode=True))
                    print('===========================')
        return
 
server = CustomSMTPServer((listen_address, listen_port), None)
asyncore.loop()
