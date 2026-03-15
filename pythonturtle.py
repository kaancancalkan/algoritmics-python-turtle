import turtle  # Import the turtle library to draw graphics and write text - this is our main tool for creating visuals!
import time   # Import time library to add pauses in the animation - helps control the timing of our demo

# Set up the screen for the animation: width 800, height 600 for better visibility
# This creates a window where our drawings will appear
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("Algorithmics Vietnam Python Demo")

# Hide the turtle for cleaner text and drawing - we don't want to see the drawing cursor
turtle.hideturtle()

# Set the turtle speed to moderate (5) so we can watch the animation step-by-step
# Speed 1 is slowest, 10 is fastest, 0 is instant - 5 lets kids follow along
turtle.speed(5)

# ===============================
# PART 1: The Greeting (Matrix Style)
# ===============================

# Set the background to black for the Matrix-style greeting
# Black background with green text looks cool, like in the movie "The Matrix"
turtle.bgcolor("black")

# Define the greeting message split into lines for better fit on screen
# We split it so it doesn't go off the edge of the window
line1 = "Hello Algorithmics team,"
line2 = "this is my Python beginner task!"

# Matrix-style color: bright green for that hacker aesthetic
# Green is used in The Matrix movie for computer code falling down the screen
matrix_color = "#00FF00"  # Bright green

# Function to write a line letter by letter - this creates the typing effect
# Functions let us reuse code - we call this function twice, once for each line
def write_line_by_letter(text, start_x, start_y):
    # Move turtle to starting position without drawing
    turtle.penup()
    turtle.goto(start_x, start_y)
    turtle.pendown()
    # Set the color for writing
    turtle.pencolor(matrix_color)
    
    # Loop through each character in the text - this is iteration in action!
    # For each letter, we write it, move a bit, and pause - like typing on a keyboard
    for char in text:
        # Write the current character on screen
        turtle.write(char, align="left", font=("Courier", 20, "normal"))  # Courier looks like computer code
        # Move to the right for the next character without drawing a line
        turtle.penup()
        turtle.forward(12)  # 12 pixels - just enough space for the next letter
        turtle.pendown()
        # Pause briefly to create the letter-by-letter animation effect
        # 0.05 seconds is very fast - makes it look like it's typing quickly
        time.sleep(0.05)  # This pause makes the animation exciting to watch!

# Write first line - call our function with the text and position
write_line_by_letter(line1, -250, 50)  # Upper line, centered-ish on screen

# Write second line - call the function again for the second part of the message
write_line_by_letter(line2, -250, -20)  # Lower line, below the first

# Pause for 2 seconds to let the interviewers read the complete message
# time.sleep(2) stops everything for 2 seconds - gives time to read before moving on
time.sleep(2)

# Clear the screen to prepare for the flag
# turtle.clear() removes all drawings from the screen - like erasing a whiteboard
turtle.clear()

# ===============================
# PART 2: The Vietnam Flag
# ===============================

# Set the background to the vibrant red of the Vietnam flag (#DA251D)
# This is the official red color used in the Vietnamese flag
turtle.bgcolor("#DA251D")

# Set pen and fill color to golden yellow for the star (#FFFF00)
# Yellow represents the golden star in the center of the flag
turtle.pencolor("#FFFF00")
turtle.fillcolor("#FFFF00")

# Position the turtle to the center of the flag without drawing
# penup() lifts the pen so we can move without drawing lines
turtle.penup()
turtle.goto(0, 0)  # Center of the screen (0,0) is perfect for centering the star
turtle.pendown()  # pendown() puts the pen back down to start drawing

# Start filling the star shape
# begin_fill() tells Turtle to fill the shape we're about to draw
turtle.begin_fill()

# Draw the five-pointed star using a for loop to demonstrate iteration
# A star has 5 points, so we repeat 5 times - this is called a "loop"
# Each point requires moving forward and turning 144 degrees
# Why 144 degrees? Because 360 degrees in a full circle divided by 5 points = 72 degrees per section,
# but for a star, we turn 144 degrees (72 * 2) to create the inward angle between points
# Imagine a clock: 360 degrees is a full circle. For a star, we need sharp points!
# The for loop makes this easy - instead of writing the same code 5 times, we loop!
# This teaches kids about "iteration" - repeating actions to save time
for i in range(5):  # range(5) means do this 5 times: 0, 1, 2, 3, 4
    # Move forward to draw one side of the star point
    turtle.forward(150)  # Length of each star arm - made larger for visibility
    # Turn right by 144 degrees to position for the next point
    # right(144) rotates the turtle clockwise by 144 degrees
    turtle.right(144)

# End the fill to color the star
# end_fill() fills the shape with the fillcolor we set earlier
turtle.end_fill()

# Keep the window open to admire the flag
# turtle.done() keeps the window open until you close it - perfect for showing off our work!
turtle.done()