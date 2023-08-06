# encoding: utf-8

import mailbox


__all__ = ['MailboxTransport']

log = __import__('logging').getLogger(__name__)



class MailboxTransport(object):
    """A classic UNIX mailbox on-disk file delivery transport.
    
    Due to the file locking inherent in this format, using a background
    delivery mechanism (such as a Futures thread pool) makes no sense.
    """
    
    def __init__(self, config):
        self.box = None
        self.filename = config.get('file', None)
        
        if not self.filename:
            raise ValueError("You must specify an mbox file name to write messages to.")
    
    def startup(self):
        self.box = mailbox.mbox(self.filename)
    
    def deliver(self, message):
        self.box.lock()
        self.box.add(mailbox.mboxMessage(bytes(message)))
        self.box.unlock()
    
    def shutdown(self):
        self.box.close()
        self.box = None
