# -*- coding: latin-1 -*-
"""
*******************************************************************************
** Script Name: imap_email.py
** Author(s):   Terrence Beach (tjbeachjr@gmail.com)
*******************************************************************************

** Description:

*******************************************************************************
"""
import common
import imaplib
import logging

###############################################################################
# Mailbox object - Connects via IMAP
###############################################################################

class Mailbox(object):

    def __init__(self, host = "", port = 143, username = "", password = "", ssl = False, folder = "INBOX"):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__ssl = ssl
        self.__logged_in = False
        self.__log = common.setup_logger("Mailbox")
        if self.__login():
            self.__logged_in = True
            self.switchFolder(folder)
            
    def __del__(self):
        if self.__logged_in:
            self.__logout()
        
    def __login(self):
        try:
            if self.__ssl:
                self.__log.debug("Logging into IMAP server %s:%i using SSL" % (self.__host, self.__port))
                self.__server = imaplib.IMAP4_SSL(self.__host, self.__port)
            else:
                self.__log.debug("Logging into IMAP server %s:%i" % (self.__host, self.__port))
                self.__server = imaplib.IMAP4(self.__host, self.__port)
        except:
            self.__log.error("Unable to connect to IMAP server %s:%i" % (self.__host, self.__port))
            return False
        try:
            self.__server.login(self.__username, self.__password)
        except:
            self.__log.error("Unable to login to IMAP server using provided credentials")
            return False
        return True
            
    def __logout(self):
        self.__log.debug("Logging out from IMAP server %s:%i" % (self.__host, self.__port))
        self.__server.close()
        self.__server.logout()
        self.__logged_in = False
    
    def loggedIn(self):
        return self.__logged_in
    
    def getMessages(self, criterion):
        self.__log.debug("Search folder '%s' for '%s' messages" % (self.__folder, criterion))
        code, data = self.__server.search(None, criterion)
        if code == "OK":
            messages = data[0].split()
            self.__log.debug("Found %i messages in folder '%s' using criteria '%s'" % (len(messages), self.__folder, criterion))
            return messages
        else:
            self.__log.error("Unable to search folder '%s'" % self.__folder)
            raise RuntimeError, "Failed to get messages from folder \"%s\"" % self.__folder    

    def getNewMessages(self):
        return self.getMessages("UnSeen")

    def switchFolder(self, folder):
        self.__log.debug("Opening folder '%s'" % folder)
        self.__folder = folder
        code, temp = self.__server.select(self.__folder)
        if code != "OK":
            self.__log.error("Unable to open folder '%s'" % folder)
            raise RuntimeError, "Failed to select folder \"%s\"" % self.__folder
        
    def downloadSingleEmail(self, message):
        code, data = self.__server.fetch(message, "(RFC822)")
        if code == "OK":
            return data[0][1]
        else:
            raise RuntimeError, "could not retrieve msgid %r" % msgid
    
    def markAsRead(self, message):
        self.__log.debug("Marking message %s in folder '%s' as read" % (self.__folder, message))
        self.__server.store(message, "+FLAGS", "\Seen")
        
    def markAllAsRead(self):
        messages = self.getMessages("UnSeen")
        for message in messages:
            self.markAsRead(message)


        
