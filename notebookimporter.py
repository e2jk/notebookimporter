#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This file is part of Notebook Importer.
#
#    Notebook Importer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Notebook Importer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Notebook Importer.  If not, see <http://www.gnu.org/licenses/>.

import sys
import csv
import smtplib
from email.MIMEText import MIMEText

# Adapt the following 3 variables to your situation
GMAIL_LOGIN = "myemail@gmail.com"
GMAIL_PASSWORD = "password"
# Find your Evernote email at https://www.evernote.com/Settings.action
EVERNOTE_EMAIL = "username.5199b42@m.evernote.com"

def parseData(filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        try:
            header = None
            content = []
            for row in reader:
                if not header:
                    header = row
                else:
                    # Do not allow newlines in the title
                    row[0] = " - ".join(row[0].splitlines())
                    content.append(row)
            return (header, content)
        except csv.Error as e:
            sys.exit("File %s, line %d: %s" % (filename, reader.line_num, e))

def printData(header, content, startOffset, numToDisplay):
    for row in content[startOffset:startOffset+numToDisplay]:
        colnum = 0
        for col in row:
            print "%-13s: %s" % (header[colnum], col)
            colnum += 1
        print

def formatEmail(row):
    """Determine subject and body of the email to be sent"""
    subject = row[0]
    if row[3]:
        # Notebook name
        subject += " @%s" % row[3]
    if row[2]:
        # Labels
        #TODO: handle multiple tags
        subject += " #%s" % row[2]
    message = row[1]
    return (subject, message)
 
def sendEmail(subject, message):
    """
    Based on http://halotis.com/2009/07/11/sending-email-from-python-using-gmail/
    """
    msg = MIMEText(message, "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = GMAIL_LOGIN
    msg['To'] = EVERNOTE_EMAIL
 
    server = smtplib.SMTP('smtp.gmail.com', 587) #port 465 or 587
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(GMAIL_LOGIN, GMAIL_PASSWORD)
    server.sendmail(GMAIL_LOGIN, EVERNOTE_EMAIL, msg.as_string())
    server.close()

def emailData(content, startOffset, numToSend):
    """
    Skip all emails that have any text in the 4th column ("Do not upload")
    Try to send as many notes as requested, but do not send more than the
    maximum allowed by your account:
    * Non-premium Evernote accounts: 50 emails per day
    * Premium Evernote accounts: 200 emails per day
    """
    
    # Determine how many emails can be sent
    numCanBeSent = 0
    for row in content[startOffset:]:
        if not row[4]:
            numCanBeSent += 1
            if numCanBeSent == numToSend:
                break
    maxToSend = 50 # Limit the number of emails that can be sent
    numWillBeSent = min(numCanBeSent, maxToSend)
    if numWillBeSent < numCanBeSent:
        print "WARNING: A total of %d notes are ready to be sent, but due to Evernote limitations only %d will be sent:" % (numCanBeSent, numWillBeSent)
    else:
        print "%d notes will be sent:" % numWillBeSent
    
    # Send the emails
    numEmailsSent = 0
    for row in content[startOffset:]:
        if not row[4]:
            (subject, message) = formatEmail(row)
            print "%3d%% - %s" % (float(100*numEmailsSent/numWillBeSent), subject)
            sendEmail(subject, message)
            numEmailsSent += 1
            if numEmailsSent == numWillBeSent:
                break
    print "100%\n"
    print "Note: in case you have more notes to send later (due to the limit of %d emails per day), don't forget to update your .csv file and indicate in the 5th column (\"Do not upload\") that these notes that have just been sent do not need to be sent again." % maxToSend

def defaults(content, startOffset, num):
    if startOffset==None or num==None:
        return (0, len(content))
    else:
        return (startOffset, num)

if __name__ == '__main__':
    filename = sys.argv[1]
    
    # Retrieve the data from the CSV file
    (header, content) = parseData(filename)
    if ['Title', 'Content', 'Labels', 'Notebook', 'Do not upload'] != header:
        # The first line should contain the 5 headers, nothing different
        sys.exit("File is not valid")
    
    # How many notes to process (leave to None to process all)
    # Note that if the number to process is smaller than the total number of
    # notes, the list displayed by printData might be different than the list
    # of notes that will be sent by email.
    # This is due to the fact that the display function shows X number of notes
    # (including the notes that should not be sent), while the email process
    # skips those unwanted notes but will still send the same X number of notes.
    startOffset = numToProcess = None
    #startOffset = 185
    #numToProcess = 3
    (startOffset, numToProcess) = defaults(content, startOffset, numToProcess)
    
    printData(header, content, startOffset, numToProcess)
    emailData(content, startOffset, numToProcess)

