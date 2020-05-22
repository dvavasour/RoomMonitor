#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import os.path

conf_stanza = 'REST-stuff'
conf_filename = 'Snippet.conf'

script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))
config_filepath = os.path.join(script_dirpath, conf_filename)

config = ConfigParser.ConfigParser()
config.read(config_filepath)

savedSearch = config.get(conf_stanza, 'savedSearch')

print(savedSearch)
