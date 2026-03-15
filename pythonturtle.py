import turtle  # Import the turtle library to draw graphics

# Set up the screen for the Vietnam flag: width 600, height 400 (2:3 ratio like the real flag)
screen = turtle.Screen()
screen.setup(width=600, height=400)
screen.title("Vietnam Flag Drawing")

# Set the background color to the vibrant red of the Vietnam flag (#DA001E)
turtle.bgcolor("#DA001E")

# Set the turtle speed to moderate (5) so we can watch the star being drawn step-by-step
turtle.speed(5)

# Hide the turtle for a cleaner look
turtle.hideturtle()

# Position the turtle to the center of the flag without drawing
turtle.penup()
turtle.goto(0, 0)  # Center of the screen (0,0) is perfect for centering the star
turtle.pendown()

# Set the pen color to golden yellow for the star (#FFCD00)
turtle.pencolor("#FFCD00")
turtle.fillcolor("#FFCD00")

# Start filling the star shape
turtle.begin_fill()

# Draw the five-pointed star using a for loop to demonstrate iteration
# A star has 5 points, so we repeat 5 times
# Each point requires moving forward and turning 144 degrees (360/5 = 72, but for star points we turn 144 to create the inward spikes)
for i in range(5):
    # Move forward to draw one side of the star point
    turtle.forward(100)  # Length of each star arm - adjust for size
    # Turn right by 144 degrees to position for the next point
    # Why 144? Because 360 degrees in a circle divided by 5 points = 72 degrees per section,
    # but for a star, we turn 144 degrees (72 * 2) to create the inward angle between points
    turtle.right(144)

# End the fill to color the star
turtle.end_fill()

# Keep the window open so we can admire the flag
turtle.done()