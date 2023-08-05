#!/usr/bin/env python

from Tkinter import *
from email import *
from time import *
import os
import sys
import csv
import respond
import ConfigParser, os

"""
This is the vomailer main module. This module is the starting point for the vomailer tool. It will accept an e-mail address as standard input and process it.

This module is designed to handle e-mail based application from Volunteer Ottawa. To receive volunteer applications you must belong to Volunteer Ottawa. http://www.volunteerottawa.ca/vo-clean/index.php?/eng/membership_services/become_a_member

This module was originaly created for use by Computers for Communities (http://computersforcommunities.ca), a member of volunteer Ottawa.

"""

workingdir = os.getcwd()

config = ConfigParser.ConfigParser()
config.read('config.cfg')
debugLevel = config.get('setup', 'debug')




def main():
    """
    This is the main module called when an e-mail is piped to the script as standard input
    """
    if debugLevel == 1 :
        debug("Mail Processing script started")
    else:
        pass
    
    #read the piped e-mail
    pipe = sys.stdin.read()
    #make email object
    msg = message_from_string(pipe)
    #process the email
    vol = process(msg)
    # dump to a db
    catalogue(vol)
    stat, rfile = response(vol)
    message = respond.main(vol, stat, rfile)
    

def process(mailmsg):
    """
    The process() function accepts a raw e-mail message as input and returns a dictionary object of Volunteer.
    
    The volunteer dictionary has the following attributes:
    * name
    * email
    * position
    * phone
    * notes
    
    These are all extracted from the submitted e-mail. Note the 'notes' section is often blank
    """
    msg=mailmsg
    #pick out From field
    frm = msg["From"]  
    #get the payload content
    content = msg.get_payload()
    #change the string into a list. Split on line breaks
    lst=content.split('<br>')
    #pick out the position they are applying for
    head_len = len(lst[0].strip())  # find the length of the header paragraph, strip the white space
    pos = lst[0][53:(head_len-1)] 
    # pick out who sent the VO application
    name = lst[1][6:].strip()
    # pick out the email
    addr = lst[2][6:].strip()
    # phone number
    phone = lst[3][6:].strip()
    # notes if any
    notes = lst[4]
    #build dictionary
    volunteer= {'name':name, 'email':addr, 'position':pos, 'phone':phone, 'notes':notes}
    #print volunteer["position"]
    if debugLevel == 1:
        debug(str(volunteer["name"] + " " + volunteer["email"]))
    else:
        pass
    return volunteer
    

def catalogue(record):
    """
    The catalogue() function accepts a volunteer record object 'record'. This is the dictionary created in the process() function.
    
    The volunteer record dictionary has the following attributes:
    * name
    * email
    * position
    * phone
    * notes
    
    This writes this captured information to a log file log.csv in the logs sub directory
    """    
    #  input results to spreadsheet or DB
    # open an output file
    output = open(workingdir + '/logs/log.csv','a')
    # write volunteer info in CSV form  
    output.write(ctime(time()) + ", " + record['name'] + ", " + record['phone'] +", " +  record['email']  +", " + record['position'] + '\r\n' )
    output.close()
    
    if debugLevel == 1:
        debug(str(ctime(time()) + ", " + record['name'] + " has just been cataloged"))
    else:
        pass

def response(volunteer):
    """
    The response() function accepts a volunteer record as input and returns a 'status' object as well as a'respfile' object
    
    The status indicates if the position if FULL or OPEN.
    
    The respfile points to a pre-canned text e-mail response files in the responses sub directory.
    """   
    # send the person who requested to apply the appropriate info (smtp)
    respdir = workingdir + "/responses/"
        
    if volunteer["position"] == "Communications Coordinator":
        status= "full"
        respfile = NONE 

    elif volunteer["position"] == "Administrative Assistant": 
        status= "full"
        respfile = NONE 

    elif volunteer["position"] == "Web Designer":
        status= "open"
        resfile = respdir + "Web Designer.txt"

    elif volunteer["position"] == "Web Master": 
        status= "open"
        resfile = respdir + "Web Master.txt"

    elif volunteer["position"] == "Computer Transportation":
        status= "open"
        resfile = respdir + "Computer Transportation.txt"

    elif volunteer["position"] == "Computer Refurbishing and Software Installation":
        status= "open"
        resfile = respdir + "Computer Refurbishing and Software Installation.txt"

    elif volunteer["position"] == "Volunteer Recruiter":
        status= "open"
        resfile = respdir + "Volunteer Recruiter.txt"

    elif volunteer["position"] == "Welcoming Committee":
        status= "open"
        resfile = respdir + "Welcoming Committee.txt"    

    elif volunteer["position"] == "Computer Lab coordinator":
        status= "open"
        resfile = respdir + "Computer Lab coordinator.txt"

    elif volunteer["position"] == "System Administrator":
        status= "open"
        resfile = respdir + "System Administrator.txt"

    elif volunteer["position"] == "Computer Lab Mentor":
        status= "open"
        resfile = respdir + "Computer Lab Mentor.txt"

    elif volunteer["position"] == "Graphic Artist":
        status= "open"
        resfile = respdir + "Graphic Artist.txt"

    elif volunteer["position"] == "Fundraising and Grant coordinator":
        status= "open"
        resfile = respdir + "Fundraising and Grant coordinator.txt"

    elif volunteer["position"] == "Partnership Coordinator":
        status= "open"
        resfile = respdir + "Partnership Coordinator.txt"

    else:
        status = "NULL"
        resfile = "NULL"

    
    if debugLevel == 1:
        debug(str(volunteer["position"] + ' is ' + status +': ' + volunteer["name"] + " " + volunteer["email"]))
    else:
        pass
        
    return [status,resfile]
    
    

def markResponse():
    """
    This function is currently empty
    """
    # mark original message as read and replied
    # this can be handled with most email programs. Hint, position after pipping the script
    pass
    
def debug(msg):
    root = Tk()
    w = Label(root, text=msg)  
    w.pack()
    root.mainloop()

if __name__ == "__main__":
    """
    This if statement evaluates if the script is called from the command line or directly through a double click.
    """
    main()
