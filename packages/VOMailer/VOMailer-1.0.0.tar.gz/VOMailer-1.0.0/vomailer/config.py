#!/usr/bin/env python

"""
This module will be used to parse the config file and pass parameters around
"""
import ConfigParser


def main():
    config()
    pass
    
    
def config():
    cfg = []
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
    installdir = config.get('setup','installdir')
    cfg['installdir'] = 
    return installdir

if __name__ == "__main__":
    main()
