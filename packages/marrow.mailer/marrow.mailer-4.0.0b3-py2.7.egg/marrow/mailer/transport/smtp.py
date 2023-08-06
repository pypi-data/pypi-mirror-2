# encoding: utf-8

"""Deliver messages using (E)SMTP."""

from smtplib import (SMTP, SMTP_SSL, SMTPException, SMTPRecipientsRefused,
                     SMTPSenderRefused, SMTPServerDisconnected)
import socket
import sys

from marrow.mailer.exc import (MailConfigurationException,
    TransportExhaustedException, TransportException, TransportFailedException)

from marrow.util.convert import boolean
from marrow.util.compat import native


log = __import__('logging').getLogger(__name__)



class SMTPTransport(object):
    """An (E)SMTP pipelining transport."""
    
    def __init__(self, config):
        if not 'host' in config:
            raise MailConfigurationException('No server configured for SMTP')
        
        self.host = native(config.get('host'))
        self.tls = config.get('tls', 'optional')
        self.certfile = config.get('certfile', None)
        self.keyfile = config.get('keyfile', None)
        self.port = int(config.get('port', 465 if self.tls == 'ssl' else 25))
        self.local_hostname = native(config.get('local_hostname', '')) or None
        self.username = native(config.get('username', '')) or None
        self.password = native(config.get('password', '')) or None
        self.timeout = config.get('timeout', None)
        
        if self.timeout:
            self.timeout = int(self.timeout)
        
        self.debug = boolean(config.get('debug', False))
        
        self.pipeline = config.get('pipeline', None)
        if self.pipeline is not None:
            self.pipeline = int(self.pipeline)
        
        self.connection = None
        self.sent = 0
    
    def startup(self):
        if not self.connected:
            self.connect_to_server()
    
    def shutdown(self):
        if self.connected:
            log.debug("Closing SMTP connection")
            
            try:
                try:
                    self.connection.quit()
                
                except SMTPServerDisconnected:
                    pass
                
                except (SMTPException, socket.error):
                    log.exception("Unhandled error while closing connection.")
            
            finally:
                self.connection = None
    
    def connect_to_server(self):
        if self.tls == 'ssl':
            connection = SMTP_SSL(local_hostname=self.local_hostname, keyfile=self.keyfile,
                                  certfile=self.certfile, timeout=self.timeout)
        else:
            connection = SMTP(local_hostname=self.local_hostname, timeout=self.timeout)

        log.info("Connecting to SMTP server %s:%s", self.host, self.port)
        connection.set_debuglevel(self.debug)
        connection.connect(self.host, self.port)

        # Do TLS handshake if configured
        connection.ehlo()
        if self.tls in ('required', 'optional'):
            if connection.has_extn('STARTTLS'):
                connection.starttls(self.keyfile, self.certfile)
            elif self.tls == 'required':
                raise TransportException('TLS is required but not available on the server -- aborting')

        # Authenticate to server if necessary
        if self.username and self.password:
            log.info("Authenticating as %s", self.username)
            connection.login(self.username, self.password)

        self.connection = connection
        self.sent = 0
    
    @property
    def connected(self):
        return getattr(self.connection, 'sock', None) is not None

    def deliver(self, message):
        if not self.connected:
            self.connect_to_server()
        
        try:
            self.send_with_smtp(message)
        
        finally:
            if self.pipeline is True:
                return
            
            if not self.pipeline or self.sent >= self.pipeline:
                raise TransportExhaustedException()
    
    def send_with_smtp(self, message):
        try:
            sender = bytes(message.envelope)
            recipients = message.recipients.string_addresses
            self.sent += 1
            self.connection.sendmail(sender, recipients, bytes(message))
        
        except SMTPSenderRefused:
            # The envelope sender was refused.  This is bad.
            e = sys.exc_info()[1]
            log.error("%s REFUSED %s %s", message.id, e.__class__.__name__, e)
            raise MessageFailedException(e)
        
        except SMTPRecipientsRefused:
            # All recipients were refused. Log which recipients.
            # This allows you to automatically parse your logs for bad e-mail addresses.
            e = sys.exc_info()[1]
            log.warning("%s REFUSED %s %s", message.id, e.__class__.__name__, e)
            raise MessageFailedException(e)
        
        except SMTPServerDisconnected:
            if message.retries >= 0:
                log.warning("%s DEFERRED %s", message.id, "SMTPServerDisconnected")
                message.retries -= 1
            
            raise TransportFailedException()
        
        except:
            e = sys.exc_info()[1]
            cls_name = e.__class__.__name__
            log.debug("%s EXCEPTION %s", message.id, cls_name, exc_info=True)
            
            if message.retries >= 0:
                log.warning("%s DEFERRED %s", message.id, cls_name)
                message.retries -= 1
            
            else:
                log.exception("%s REFUSED %s", message.id, cls_name)
                raise TransportFailedException()
