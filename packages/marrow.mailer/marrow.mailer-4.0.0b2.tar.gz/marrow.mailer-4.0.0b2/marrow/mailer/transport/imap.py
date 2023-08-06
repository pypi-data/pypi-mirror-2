# encoding: utf-8

import imaplib

from datetime import datetime

from marrow.mailer.exc import TransportException, DeliveryFailedException


__all__ = ['IMAPTransport']

log = __import__('logging').getLogger(__name__)



class IMAPTransport(object):
    def __init__(self, config):
        if not 'host' in config:
            raise MailConfigurationException('No server configured for IMAP.')
        
        self.host = config.get('host', None)
        self.ssl = config.get('ssl', False)
        self.port = config.get('port', 993 if self.ssl else 143)
        self.username = config.get('username', None)
        self.password = config.get('password', None)
        self.folder = config.get('folder', "INBOX")
    
    def startup(self):
        Protocol = imaplib.IMAP4_SSL if self.ssl else imaplib.IMAP4
        self.connection = Protocol(self.host, self.port)
        
        if self.username:
            result = self.connection.login(self.username, self.password)
            
            if result[0] != b'OK':
                raise TransportException("Unable to authenticate with IMAP server.")
    
    def deliver(self, message):
        result = self.connection.append(
                self.folder,
                '', # TODO: Set message urgency / flagged state.
                message.date.timetuple() if message.date else datetime.now(),
                bytes(message)
            )
        
        if result[0] != b'OK':
            raise DeliveryFailedException(message, "\n".join(result[1]))
    
    def shutdown(self):
        self.connection.logout()
