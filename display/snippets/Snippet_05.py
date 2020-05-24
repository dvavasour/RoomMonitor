#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import os.path




def readConfig(conf_filename \
              ):
    script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))
    config_filepath = os.path.join(script_dirpath, conf_filename)

    config = ConfigParser.ConfigParser()
    config.read(config_filepath)
    return(config)

def main():
    conf_stanza = 'REST-stuff'
    conf_filename = 'Snippet.conf'
    
    config = readConfig(conf_filename)

    savedSearch = config.get(conf_stanza, 'savedSearch')
    print(savedSearch)

if __name__=='__main__':
     main()
