import pygame
import pycreate2
import time
from init import port


# Initialize pygame for joystick control
pygame.init()
pygame.joystick.init()

# Ensure at least one joystick is connected
if pygame.joystick.get_count() == 0:
    print("No joystick detected")
    pygame.quit()
    exit()

# Use the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Setup connection to Roomba

baud = {
    'default': 115200,
    'alt': 19200  # Modify as per your Roomba model
}

# Create a Create2 object
bot = pycreate2.Create2(port, baud['default'])
bot.start()
bot.safe()

try:
    while True:
        # Process pygame events
        pygame.event.pump()

        # Get joystick axes for forward/backward and left/right
        forward_backward = joystick.get_axis(1)  # Usually, the Y axis of the left stick
        turn = joystick.get_axis(0)  # Usually, the X axis of the left stick

        # Scale joystick values to Roomba speed
        # Forward/backward value needs to be inverted depending on joystick configuration
        speed = -forward_backward * 500  # Scale to max speed of Roomba
        rotation = turn * 200  # Scale turning speed

        # Send commands to Roomba
        bot.drive_direct(int(speed + rotation), int(speed - rotation))

        # Delay to make it smoother
        time.sleep(0.1)

except KeyboardInterrupt:
    # Stop the robot
    bot.drive_stop()

finally:
    # Clean up on exit
    pygame.quit()
    bot.close()

