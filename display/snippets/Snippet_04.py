#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    # We'll fix this when I've put kosher certificates in Splunk


# Authorise search using a token
REST_authString = {'Authorization': 'Bearer eyJraWQiOiJzcGx1bmsuc2VjcmV0IiwiYWxnIjoiSFM1MTIiLCJ2ZXIiOiJ2MSIsInR0eXAiOiJzdGF0aWMifQ.eyJpc3MiOiJhZG1pbiBmcm9tIGlwLTEwLTE5Mi0wLTEwNi5ldS13ZXN0LTIuY29tcHV0ZS5pbnRlcm5hbCIsInN1YiI6ImFkbWluIiwiYXVkIjoiZnJlZCIsImlkcCI6InNwbHVuayIsImp0aSI6Ijc1OTE5MTBhZDhjOTVlZDY0MTJiNDA1MDkyOWQxYWExY2RlZTZmZDJiYTQ0ZmFlMmNiMzZmNzdlOTI4NzcyMjQiLCJpYXQiOjE1OTAxNTI2NTcsImV4cCI6MCwibmJyIjoxNTkwMTUyNjU3fQ.zDKTshlagDFD_8jFsiOkRaq6Ls1rdtjJWxeYdcK-pKIdVIZjUdj3ogz7Kl0LWOOk_Xx6FMGlA8lslROxD1sCZg'}
REST_body = {'search': 'savedsearch roomMonitor5MinuteAverages'}
REST_parameters = {'output_mode': 'json'}
REST_URL = 'https://splunk-dev.dv-aws.uk:8089/servicesNS/admin/pi_test/search/jobs/export'
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

outputTemperature = '%.2f' % float(results['temperature'])
outputHumidity = '%.2f' % float(results['humidity'])
outputPressure = '%.0f' % float(results['pressure'])
outputResistance = '%.0f' % (float(results['gas_resistance']) / 1000)
print(outputTemperature, outputHumidity, outputPressure, outputResistance)

