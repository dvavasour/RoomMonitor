import time
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne


# Some constants
deviceColour = "black"


# Frigged values for testing
temperature = 25.46
pressure = 1007
humidity = 40.17
resistance = 960000




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
    inkyDisplay.set_border(inkyDisplay.WHITE)
    inkyDisplay.set_border(inkyDisplay.BLACK)

def initialiseImage():
    global img, draw
    img = Image.new("P", (inkyDisplay.WIDTH, inkyDisplay.HEIGHT))
    # Need to read the docs and see what the "P" means
    draw = ImageDraw.Draw(img)

def initialiseFont():
    global font
    font = ImageFont.truetype(FredokaOne, 22)


def HelloWorld():
    print("In HelloWorld function")
    message = time.strftime("%d %B %-I:%M %p")
    w, h = font.getsize(message)
    x = (inkyDisplay.WIDTH / 2) - (w / 2)
    y = (inkyDisplay.HEIGHT / 2) - (h / 2)

    width = inkyDisplay.WIDTH
    height = inkyDisplay.HEIGHT
    print("Display Width", width, "Display Height", height, "Text Width", w, "Text Height", h)
    # Basic stuff to position the message in the centre of the screen

    draw.line((69, 36, 69, 81), 1)    # Vertical line in black
    draw.rectangle ([(10,10), (40,40)], 1) # Rectangle ([(x1, y1), (x2, y2)],colour)
    draw.rectangle ([(13,13), (37,37)], 0)
    draw.text((x, y), message, inkyDisplay.BLACK, font)
    # I think this is where you set the colour that's being displayed
    
    inkyDisplay.set_image(img)
    inkyDisplay.show()
    
    
    
def default():
    print("Hello there")

def main() :
    initialiseDisplay()
    initialiseImage()
    initialiseFont()
#    default()
    HelloWorld()

if __name__ == '__main__':
    main()
