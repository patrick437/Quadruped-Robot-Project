#!/usr/bin/env python3

from __future__ import print_function
import rospy
from sensor_msgs.msg import Joy
import sys, select, termios, tty

msg = """
Reading from the keyboard and publishing to Joy!
---------------------------
Movement:
   w : Forward (Axis 1)
   s : Backward (Axis 1)
   a : Left (Axis 0)
   d : Right (Axis 0)

Rotation and Height:
   i : Rotate left (Axis 2)
   k : Rotate right (Axis 2)
   j : Increase height (Axis 4)
   l : Decrease height (Axis 4)

Buttons (Number Keys):
   1 : Button 0
   2 : Button 1
   3 : Button 2
   4 : Button 3
   5 : Button 4
   6 : Button 5
   7 : Button 6
   8 : Button 7

CTRL-C to quit
"""

# Key bindings for movement, rotation, and height
moveBindings = {
    'w': (0, 0, 0, 1),  # Forward (Axis 1)
    's': (0, 0, 0, -1),  # Backward (Axis 1)
    'a': (1, 0, 0, 0),  # Left (Axis 0)
    'd': (-1, 0, 0, 0),   # Right (Axis 0)
    'i': (0, 1, 0, 0),   # Rotate left (Axis 2)
    'k': (0, -1, 0, 0),  # Rotate right (Axis 2)
    'j': (0, 0, 1, 0),   # Increase height (Axis 4)
    'l': (0, 0, -1, 0),  # Decrease height (Axis 4)
}

# Button bindings for number keys
buttonBindings = {
    '1': 0,  # Button 0
    '2': 1,  # Button 1
    '3': 2,  # Button 2
    '4': 3,  # Button 3
    '5': 4,  # Button 4
    '6': 5,  # Button 5
    '7': 6,  # Button 6
    '8': 7,  # Button 7
}

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('teleop_twist_keyboard')
    joy_pub = rospy.Publisher('/notspot_joy/joy_ramped', Joy, queue_size=1)

    try:
        print(msg)
        while not rospy.is_shutdown():
            key = getKey()
            joy = Joy()
            joy.axes = [0.0] * 8  # Initialize with 8 axes
            joy.buttons = [0] * 11  # Initialize with 11 buttons

            if key in moveBindings.keys():
                x, y, z, th = moveBindings[key]

                # Map key bindings to axes
                joy.axes[0] = x  # Left/Right (Axis 0)
                joy.axes[1] = y  # Forward/Backward (Axis 1)
                joy.axes[2] = z  # Rotation (Axis 2)
                joy.axes[4] = th  # Height (Axis 4)

            elif key in buttonBindings.keys():
                # Map number keys to buttons
                button_index = buttonBindings[key]
                joy.buttons[button_index] = 1  # Press the button

            elif key == '\x03':  # CTRL-C
                break

            # Publish the Joy message
            joy_pub.publish(joy)

    except Exception as e:
        print(e)

    finally:
        # Reset the Joy message
        joy = Joy()
        joy.axes = [0.0] * 8
        joy.buttons = [0] * 11
        joy_pub.publish(joy)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
