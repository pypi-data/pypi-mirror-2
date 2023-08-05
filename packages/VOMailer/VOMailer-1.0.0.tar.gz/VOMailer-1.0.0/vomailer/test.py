#!/usr/bin/env python

from Tkinter import *
from email import *
from time import *
import os
import smtplib
import vomailer
import ConfigParser

from email.MIMEText import MIMEText

"""
TO DO
* add in error handling

"""
config = ConfigParser.ConfigParser()
config.read('config.cfg')

testDir = os.getcwd() + "/tests/"

def main():
    # lists the tests to be run
    # printTests() 
    # run the tests
    runTests()
    

def runTests():
    print("running tests")
    files = os.listdir(os.getcwd() + '/tests/')
    for i in files:
        print("running test for : " + i)
        # open file
        pipe = open( testDir + i, 'r').read()
        #make email object
        msg = message_from_string(pipe)
        #process the email
        vol = vomailer.process(msg)
        # dump to a db
        testLog(vol)
        print("updating test log")
        stat, rfile = vomailer.response(vol)
        message = vomailer.respond.main(vol, stat, rfile)
        print("finished sending test email for " + i )
    print("finished tests")
    
def testLog(record):    
    #  input results to spreadsheet or DB
    # open an output file
    output = open(os.getcwd() + '/test.log','a')
    # write volunteer info in CSV form in the log 
    output.write(ctime(time()) + ", " + record['name'] + ", " + record['phone'] +", " +  record['email']  +", " + record['position']  +'\r\n' )
    output.close()     

def printTests():
    files = os.listdir(os.getcwd() + '/tests/')
    for i in files:
        print(i)
    

if __name__ == "__main__":
    main()
    
