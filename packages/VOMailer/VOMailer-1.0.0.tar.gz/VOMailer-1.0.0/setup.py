#!/usr/bin/env python

from distutils.core import setup
setup(
    name = "VOMailer",    
    packages = ["vomailer"],
    package_data={'vomailer': ['tests/*.mail', 'logs/*.*', 'responses/*.txt']},    
    version = "1.0.0",    
    description = "Volunteer Ottawa Email Application Processor",    
    author = "Dave Sampson",    
    author_email = "computers.communities@gmail.com",    
    url = "http://packages.python.org/VOMailer/",    
    download_url = "http://pypi.python.org/packages/source/V/VOMailer/VOMailer-1.0.0.tar.gz",    
    keywords = ["email", "csv", "volunteer", "application"],    
    classifiers = [        
    "Programming Language :: Python",        
    "Programming Language :: Python :: 2.6",        
    "Development Status :: 4 - Beta",        
    "Environment :: Other Environment",        
    "Intended Audience :: Developers",        
    "Intended Audience :: Other Audience",       
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",        
    "Natural Language :: English",        
    "Operating System :: OS Independent",        
    "Operating System :: POSIX :: Linux",        
    "Topic :: Communications :: Email",        
    "Topic :: Software Development :: Libraries :: Python Modules",        
    "Topic :: Text Processing :: Linguistic",        
    "Topic :: Education",        
    "Topic :: Utilities"        
    ],    
    long_description = """\
    Volunteer Ottawa Email Application Processor
    -------------------------------------

    Features:
    ---------
    * accepts email as stdin
    * captures volunteer information
    * populates a CSV file with volunteer information
    * matches possition applied for with pre-composed email response
    * sends email to applicant

    """
    )
