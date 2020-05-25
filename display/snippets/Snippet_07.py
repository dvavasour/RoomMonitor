#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib3
import json
import ConfigParser
import os
import os.path

import time
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    # We'll fix this when I've put kosher certificates in Splunk



# Some constants
deviceColour = "black"
totalWidth = 212
totalHeight = 104


# Frigged values for testing
temperature = "25.46"
pressure = "1007"
humidity = "40.17"
resistance = "960"
degrees = u"\u00B0"
ohms = u"\u2126"


temperature = "T: " + temperature + degrees + "C"
pressure = "P: " + pressure + "mB"
humidity = "H: " + humidity + "%"
resistance = "R: " + resistance + "K" + ohms

boxBorderWidth = 2
textBorderWidth = 5

topLeftX = 15
topLeftY = 15
topRightX = 202
topRightY = 10
bottomLeftX = 10
bottomLeftY = 94
bottomRightX = 202
bottomRightY = 94

centreVertical = totalWidth / 2
centreHorizontal = totalHeight / 2
outerCentreTuple = (centreVertical, centreHorizontal)




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

def initialiseDisplay():
    """

    Basic setup of display

    Inputs: None
    Return Values: None
    Global Objects Created: inkyDisplay (instance of inkyPHAT)

    """
    global inkyDisplay
    inkyDisplay = InkyPHAT(deviceColour)
    # I think we do this here.
    # inkyDisplay.set_border(inkyDisplay.WHITE)
    inkyDisplay.set_border(inkyDisplay.BLACK)

def initialiseImage():
    global img, draw
    img = Image.new("P", (inkyDisplay.WIDTH, inkyDisplay.HEIGHT))
    # Need to read the docs and see what the "P" means
    draw = ImageDraw.Draw(img)

def initialiseFont():
    global font
#    font = ImageFont.truetype(FredokaOne, 22)
    font = ImageFont.truetype("DejaVuSansCondensed.ttf", 16)

def drawTopLeft(message):
    messageWidth, messageHeight = font.getsize(message)
    topLeftX = centreVertical - messageWidth - (2 * boxBorderWidth) - (2 * textBorderWidth)
    topLeftY = centreHorizontal - messageHeight - (2 * boxBorderWidth) - (2 * textBorderWidth)
    messageTopLeftX = centreVertical - (messageWidth ) - boxBorderWidth - textBorderWidth
    messageTopLeftY = centreHorizontal - (messageHeight ) - boxBorderWidth - textBorderWidth
    messageTopLeftTuple = (messageTopLeftX, messageTopLeftY)

    outerTLTuple = (topLeftX, topLeftY)
    innerCentreTupleTL = (centreVertical - boxBorderWidth, centreHorizontal - boxBorderWidth)
    innerTLTuple = (topLeftX + boxBorderWidth, topLeftY + boxBorderWidth)
    draw.rectangle ([outerTLTuple, outerCentreTuple], 1)
    draw.rectangle ([innerTLTuple, innerCentreTupleTL], 0)

    draw.text((messageTopLeftTuple), message, inkyDisplay.BLACK, font)
    
def drawTopRight(message):
    messageWidth, messageHeight = font.getsize(message)
    topRightX = centreVertical + messageWidth + (2 * boxBorderWidth) + (2 * textBorderWidth)
    topRightY = centreHorizontal - messageHeight - (2 * boxBorderWidth) - (2 * textBorderWidth)
    messageTopLeftX = centreVertical + boxBorderWidth + textBorderWidth
    messageTopLeftY = centreHorizontal - (messageHeight ) - boxBorderWidth - textBorderWidth
    messageTopLeftTuple = (messageTopLeftX, messageTopLeftY)

    outerTRTuple = (topRightX, topRightY)
    innerCentreTupleTR = (centreVertical + boxBorderWidth, centreHorizontal - boxBorderWidth)
    innerTRTuple = (topRightX - boxBorderWidth, topRightY + boxBorderWidth)
    draw.rectangle ([outerTRTuple, outerCentreTuple], 1)
    draw.rectangle ([innerTRTuple, innerCentreTupleTR], 0)

    draw.text((messageTopLeftTuple), message, inkyDisplay.BLACK, font)

def drawBottomLeft(message):
    messageWidth, messageHeight = font.getsize(message)
    bottomLeftX = centreVertical - messageWidth - (2 * boxBorderWidth) - (2 * textBorderWidth)
    bottomLeftY = centreHorizontal + messageHeight + (2 * boxBorderWidth) + (2 * textBorderWidth)
    messageTopLeftX = centreVertical - messageWidth - boxBorderWidth - textBorderWidth
    messageTopLeftY = centreHorizontal + boxBorderWidth + textBorderWidth
    messageTopLeftTuple = (messageTopLeftX, messageTopLeftY)
    
    outerBLTuple = (bottomLeftX, bottomLeftY)
    innerCentreTupleBL = (centreVertical - boxBorderWidth, centreHorizontal + boxBorderWidth)
    innerBLTuple = (bottomLeftX + boxBorderWidth, bottomLeftY - boxBorderWidth)
    draw.rectangle ([outerBLTuple, outerCentreTuple], 1)
    draw.rectangle ([innerBLTuple, innerCentreTupleBL], 0)

    draw.text((messageTopLeftTuple), message, inkyDisplay.BLACK, font)
    
    
def drawBottomRight(message):
    messageWidth, messageHeight = font.getsize(message)
    bottomRightX = centreVertical + messageWidth + (2 * boxBorderWidth) + (2 * textBorderWidth)
    bottomRightY = centreHorizontal + messageHeight + (2 * boxBorderWidth) + (2 * textBorderWidth)
    messageTopLeftX = centreVertical + boxBorderWidth + textBorderWidth
    messageTopLeftY = centreHorizontal + boxBorderWidth + textBorderWidth
    messageTopLeftTuple = (messageTopLeftX, messageTopLeftY)

    outerBRTuple = (bottomRightX, bottomRightY)
    innerCentreTupleBR = (centreVertical + boxBorderWidth, centreHorizontal + boxBorderWidth)
    innerBRTuple = (bottomRightX - boxBorderWidth, bottomRightY - boxBorderWidth)
    draw.rectangle ([outerBRTuple, outerCentreTuple], 1)
    draw.rectangle ([innerBRTuple, innerCentreTupleBR], 0)

    draw.text((messageTopLeftTuple), message, inkyDisplay.BLACK, font)
    

    
def HelloWorld():
    print("In HelloWorld function")
#    message = time.strftime("%d %B %-I:%M %p")
    message = temperature
    w, h = font.getsize(message)
    x = (inkyDisplay.WIDTH / 2) - (w / 2)
    y = (inkyDisplay.HEIGHT / 2) - (h / 2)
    width = inkyDisplay.WIDTH
    height = inkyDisplay.HEIGHT
    print("Display Width", width, "Display Height", height, "Text Width", w, "Text Height", h)
    # Basic stuff to position the message in the centre of the screen

#    draw.line((69, 36, 69, 81), 1)    # Vertical line in black
#    draw.rectangle ([(10,10), (40,40)], 1) # Rectangle ([(x1, y1), (x2, y2)],colour)
#    draw.rectangle ([(13,13), (37,37)], 0)

    # draw.text((x, y), message, inkyDisplay.BLACK, font)
    # I think this is where you set the colour that's being displayed
    
    inkyDisplay.set_image(img)
    inkyDisplay.show()
    
    
    
def default():
    print("Hello there")

def main() :
    initialiseDisplay()
    initialiseImage()
    initialiseFont()
    # default()

    conf_filename = 'Snippet.conf'
    conf_stanza = 'REST-stuff'

    formattedResults = formatResults(conf_filename, \
                                     conf_stanza
                                    )
    print(formattedResults)
    
    drawTopLeft("T: " + formattedResults['temperature'] + degrees + "C")
    drawTopRight("H: " + formattedResults['humidity'] + "%")
    drawBottomLeft("P: " + formattedResults['pressure'] + "mB")
    drawBottomRight("R: " + formattedResults['gas_resistance'] + "K" + ohms)
    HelloWorld()

if __name__ == '__main__':
    main()
