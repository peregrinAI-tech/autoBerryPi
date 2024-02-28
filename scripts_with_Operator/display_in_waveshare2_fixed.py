# filename: display_in_waveshare2_fixed.py

import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Add the lib directory to the system path
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4

def draw_text(text):
    # Initialize the e-Paper display
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    # Create a new image to draw on
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    # Define the font
    font15 = ImageFont.truetype(os.path.join("waveshare/pic", 'Font.ttc'), 17)

    # Define the maximum width and height
    max_width = 33
    max_height = 100

    # Split the text into lines of maximum width
    lines = textwrap.wrap(text, max_width)

    # Initialize the current height
    current_height = 0

    # Iterate over the lines
    for i in range(len(lines)):
        # If the current height is greater than the maximum height, display an asterisk and wait for 5 minutes
        if current_height > max_height:
            draw.text((33, max_height + 1), "*", font=font15, fill=0)
            epd.display(epd.getbuffer(image))
            time.sleep(5)
            
            # Clear the display and reset the current height
            epd.init()
            epd.Clear(0xFF)
            current_height = 0

            # Redraw the current line on the new image
            image = Image.new('1', (epd.height, epd.width), 255)
            draw = ImageDraw.Draw(image)
            draw.text((0, current_height), lines[i], font=font15, fill=0)
            current_height += 15
            continue

        # Draw the line on the image
        draw.text((0, current_height), lines[i], font=font15, fill=0)

        # Increase the current height
        current_height += 15

    # Display the image on the e-Paper display
    epd.display(epd.getbuffer(image))

    # Wait for a bit before clearing the display
    time.sleep(5)

    # Clear the display
    epd.Clear(0xFF)

    # Put the e-Paper display to sleep
    epd.sleep()

# Call the function with the text you want to display
#draw_text("This is a very long text that will be split into multiple lines. It is longer than 27 characters, so it will be displayed on more than one line. After the maximum height is reached, an asterisk will be displayed and the display will be cleared after 5 minutes.")
