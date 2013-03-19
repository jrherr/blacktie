#*****************************************************************************
#  misc.py (part of the blacktie package)
#
#  (c) 2013 - Augustine Dunn
#  James Laboratory
#  Department of Biochemistry and Molecular Biology
#  University of California Irvine
#  wadunn83@gmail.com
#
#  Licenced under the GNU General Public License 3.0 license.
#******************************************************************************

"""
####################
misc.py
####################
Code facilitating random aspects of this package.
"""

import sys
import inspect
import smtplib
import base64
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText



class Bunch(dict):
    """
    A dict like class to facilitate setting and access to tree-like data.  Allows access to dictionary keys through 'dot' notation: "yourDict.key = value".
    """
    def __init__(self, *args, **kwds):
        super(Bunch,self).__init__(*args,**kwds)
        self.__dict__ = self

def bunchify(dict_tree):
    """
    Traverses a dictionary tree and converts all sub-dictionaries to Bunch() objects.
    """
    for k,v in dict_tree.iteritems():
        if type(v) == type({}):
            dict_tree[k] = bunchify(dict_tree[k])
    return Bunch(dict_tree)


def whoami():
    """
    Returns the name of the currently active function.
    """
    return inspect.stack()[1][3]


def email_notification(sender,to,subject,txt,pw):
    """
    *GIVEN*:
        * ``sender`` = email address of sender
        * ``to`` = email addres of recipient
        * ``subject`` = subject text
        * ``txt`` = body text
        * ``pw`` = password of ``sender`` 
    *DOES*:
        * Sends email to recipient using GMAIL only for now.
        * TODO: make this adjustable for other emails
    *RETURNS*:
        * ``None``
    """
    # TODO: make this adjustable for other emails
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(txt))
    
    server = smtplib.SMTP("smtp.gmail.com", 587)    
    
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender,pw)
        server.sendmail(sender,to,msg.as_string())
        server.close()
    except (smtplib.SMTPAuthenticationError,
            smtplib.SMTPConnectError,
            smtplib.SMTPDataError,
            smtplib.SMTPException,
            smtplib.SMTPHeloError,
            smtplib.SMTPRecipientsRefused,
            smtplib.SMTPResponseException,
            smtplib.SMTPSenderRefused,
            smtplib.SMTPServerDisconnected) as e:
        
        sys.stderr.write("Warning: %s was caught while trying to send your mail.\nSubject:%s\n" % (e.__class__.__name__,subject))

        server.rset()
        
        
    
def get_time():
    """
    Return system time formatted as 'YYYY:MM:DD-hh:mm:ss'.
    """
    t = time.localtime()
    return time.strftime('%Y.%m.%d-%H:%M:%S',t)
        
    

    