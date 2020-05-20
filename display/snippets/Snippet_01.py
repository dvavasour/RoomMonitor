from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne





def initialiseDisplay():
    global inkyDisplay
    inkyDisplay = InkyPHAT("red")
    inkyDisplay.set_border(inkyDisplay.WHITE)

def initialiseImage():
    global img, draw
    img = Image.new("P", (inkyDisplay.WIDTH, inkyDisplay.HEIGHT))
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

    draw.text((x, y), message, inkyDisplay.RED, font)
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
