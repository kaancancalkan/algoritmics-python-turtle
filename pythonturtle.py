import antigravity  # Fun easter egg to grab the kids' attention!

import turtle  # Import the turtle library for drawing

# Set the background color to dark blue for a better mandala view
turtle.bgcolor("darkblue")

# Set the turtle speed to fast so we don't wait
turtle.speed(0)

# Create a color list with at least 6 colors
colors = ["red", "orange", "yellow", "green", "blue", "purple"]

# Main loop: repeat 120 times (between 100-150)
for i in range(120):
    # Change the pen color each step, cycling through the color list
    turtle.pencolor(colors[i % len(colors)])

    # Move forward, increasing distance each time
    turtle.forward(i * 2)

    # Turn left to create the spiral effect
    turtle.left(59)  # 59 degrees for a nice spiral angle

# Keep the window open after drawing
turtle.done()