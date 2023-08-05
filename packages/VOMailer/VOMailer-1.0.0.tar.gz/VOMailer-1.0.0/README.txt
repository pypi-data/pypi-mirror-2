Welcome to the VO Mailer README.txt

This package is targeted towards organizational members of Volunteer Ottawa.

The purpose of the script is to accept a VO formatted volunteer application e-mail as input to a python script. This script will parse out the important information, store that information in a structured file and then respond with a pre-composed e-mail. The goal is to free up valubale volunteer time taken to respond to volunteer applications. This time can be allocated to other organizational tasks or just general volunteering.

Currently you have to edit a fair bit of the code, so we suggest you either look for a technical volunteer in your organization, or contact the local python programming community, or contact Computers for Communities directly and we can work something out.

You can download the python pagacke here: 
http://dev.computersforcommunities.ca/public/vomailer/index.htm

This page may grow in time. However, for now we will keep it simple with a link. Documentation is included with the code.

In the future we will add the following resources:

    * README.txt
    * Documentation
    
    
INSTALLATION:
you will need to install this on either a 
dedicated desktop that accepts e-mails from Volunteer Ottawa 
or 
on a server that accepts incoming e-mails from volunteer Ottawa.

1. You need python installed (http://python.org)
2. install vomailer: ./setup install 

USAGE:
    
There are multiple methods of use for this module.

1. Pass a formated e-mail as standard input using a pipe from a command line

Example:
($ denotes a command prompt)

$   sample.mail |


2. Pass an e-mail as a pipe input from an application

Example: 
As an e-mial filter from an email client program such as Evolution (link)

3. from another module
Example:
This is illustrated by the test.py script for running the scripts.

