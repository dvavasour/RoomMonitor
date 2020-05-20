from inky import InkyPHAT






def initialise ():
    inky_display = InkyPHAT("red")
    inky_display.set_border(inky_display.WHITE)

def default ():
    print("Hello there")

def main() :
    initialise()
    default()

if __name__ == '__main__':
    main()
