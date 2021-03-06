from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne


# Some constants
deviceColour = "black"



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
    message = "Hello, World!"
    w, h = font.getsize(message)
    x = (inkyDisplay.WIDTH / 2) - (w / 2)
    y = (inkyDisplay.HEIGHT / 2) - (h / 2)
    # Basic stuff to position the message in the centre of the screen

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
