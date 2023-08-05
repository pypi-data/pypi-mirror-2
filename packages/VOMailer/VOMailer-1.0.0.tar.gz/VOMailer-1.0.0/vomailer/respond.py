#!/usr/bin/env python

from Tkinter import *
from email import *
import smtplib
from email.MIMEText import MIMEText
import ConfigParser


"""
This module is used to prepare and send emails through the functions prepMail() and sendMail() respectively.
This module should be called from the vomailer.py module directly.
 
The main() module expects three objects. These are the volunteer record dictionary, the status and response file

"""
config = ConfigParser.ConfigParser()
config.read('config.cfg')
debugLevel = config.get('setup', 'debug')

#main()

def main(vol, status, resfile):
    """
    The main() function expects a vol object which is a volunteer record dictionary object, 
    status object which is text and a resfile which is pointing to a response file  in the responses sub directory
    
    The main function executes the prepMail() function and the sendMail() function.
    """
    if debugLevel == 1:
        debug("Responding to e-mail")
    else:
        pass
    resp = prepMail(vol, resfile)
    sendMail(resp)
    print("Sent email to " + vol["name"] + " " + vol["email"] )

def prepMail (volunteer, resfile):   
    """
    This module accepts in a volunteer record 'volunteer' object and a response file path 'resfile'.
    
    Some standard out messages are written using print() functions.
    
    The end result of this function is to return a 'msg' object, which is a 
    
    """
    
    if debugLevel == 1:
        debug(str("the file to be used is: " + resfile))
    else:
        pass
        
    print("the file to be used is: " + resfile)
    
    prefab = open(resfile, "r")
    preresp = prefab.read()
    
    content ="Dear " + volunteer["name"] + ", \n\n"  + "Thanks for applying for the position of " + volunteer["position"] +"\n\n" + preresp
    
    print content
    
    #message headers
    msg = MIMEText(content)
    msg['Subject'] = config.get('organization', 'agencyname') + ': ' + volunteer["position"]
    msg['From'] = config.get('organization', 'agencyname') + ' <' + config.get('organization', 'email') + '>'
    msg['To'] = volunteer["email"]
    
    return msg




def sendMail(msg):
    """
    The sendMail() function will accept an e-mail MIME type object as input, grab a pre fabricated text file and create a standard response e-mail. 
    This e-mail message is then sent to the recipient.
    """
    
    # sample script
    SERVER = config.get('mailserver', 'server')
    PORT = config.get('mailserver', 'port')
    #login info
    USER = config.get('mailserver', 'user')
    PW = config.get('mailserver', 'password')
      
    # Send the mail
    try:
        server = smtplib.SMTP_SSL(SERVER,PORT)
        server.login(USER,PW)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()
        print("test e-mail sent")
    except smtplib.SMTPException:
        print("Error: unable to send mail")
    
    if debugLevel == 1:
        debug(str("Send Mail to" + msg["To"]))
    else:
        pass
        
def debug(msg):
    root = Tk()
    w = Label(root, text=msg)  
    w.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
    
