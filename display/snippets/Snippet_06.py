#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib3
import json
import ConfigParser
import os
import os.path


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    # We'll fix this when I've put kosher certificates in Splunk


def readConfig(conf_filename \
              ):
    script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))
    config_filepath = os.path.join(script_dirpath, conf_filename)

    config = ConfigParser.ConfigParser()
    config.read(config_filepath)
    return(config)


def readData(conf_filename, \
             conf_stanza
            ):
     # Authorise search using a token
      
     config = readConfig(conf_filename)
     REST_authString = {}
     REST_body = {}
     REST_parameters = {}
     REST_authString['Authorization'] = config.get(conf_stanza, 'Authorization')
     REST_body['search']  = config.get(conf_stanza, 'search')
     REST_parameters['output_mode'] = config.get(conf_stanza, 'output_mode')
     REST_URL = config.get(conf_stanza, 'REST_URL')

     print("REST URL is: ", REST_URL)
     print("REST parameters is: ", REST_parameters)
     print("REST Authorization is; ", REST_authString)
     print("REST Body is: ", REST_body)
     
     
     REST_output = requests.post(REST_URL, params=REST_parameters, data=REST_body, verify=False, headers=REST_authString)
     print(REST_output.text)


     results = {}   # Empty dictionary for data
     rows = REST_output.text.split('\n')    # Splunk returns broken JSON so we have to parse it a row at a time
     for row in rows:
          if row:    # Split leaves and empty row so we must guard against that
               fred = json.loads(row)
               results[fred['result']['metric_name']] = fred['result']['int_avg']    # So we create a dictionary with the results in. If only Splunk would return decent JSON...
               # print(fred['result']['metric_name'])
               # print('row: ',row)
     print(results)
     return(results)


def formatResults(conf_filename, \
                  conf_stanza
                 ):
    results = readData(conf_filename, \
                       conf_stanza
                      )
    # Calls the readData() function and returns the results in a dictionary "results"
    formattedResults = {}
    outputTemperature = '%.2f' % float(results['temperature'])
    outputHumidity = '%.2f' % float(results['humidity'])
    outputPressure = '%.0f' % float(results['pressure'])
    outputResistance = '%.0f' % (float(results['gas_resistance']) / 1000)
     
    formattedResults['temperature'] = outputTemperature
    formattedResults['humidity'] = outputHumidity
    formattedResults['pressure'] = outputPressure
    formattedResults['gas_resistance'] = outputResistance
    #print(outputTemperature, outputHumidity, outputPressure, outputResistance)
    return(formattedResults)

def main():
     conf_filename = 'Snippet.conf'
     conf_stanza = 'REST-stuff'
     
     formattedResults = formatResults(conf_filename, \
                                      conf_stanza
                                     )

     print(formattedResults)


if __name__=='__main__':
     main()
