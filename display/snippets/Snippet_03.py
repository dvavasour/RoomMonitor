#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne


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

    drawTopLeft(temperature)
    drawTopRight(humidity)
    drawBottomLeft(pressure)
    drawBottomRight(resistance)
    HelloWorld()

if __name__ == '__main__':
    main()
