import turtle  # Import the turtle library to draw graphics and write text
import time   # Import time library to add pauses in the animation

# Set up the screen for the animation: width 800, height 600 for better visibility
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("Algorithmics Vietnam Python Demo")

# Hide the turtle for cleaner text and drawing
turtle.hideturtle()

# Set the turtle speed to moderate (5) so we can watch the animation step-by-step
turtle.speed(5)

# ===============================
# PART 1: The Greeting (Matrix Style)
# ===============================

# Set the background to black for the Matrix-style greeting
turtle.bgcolor("black")

# Define the greeting message split into lines for better fit
line1 = "Hello Algorithmics team,"
line2 = "this is my Python beginner task!"

# Matrix-style color: bright green for that hacker aesthetic
matrix_color = "#00FF00"  # Bright green

# Function to write a line letter by letter
def write_line_by_letter(text, start_x, start_y):
    turtle.penup()
    turtle.goto(start_x, start_y)
    turtle.pendown()
    turtle.pencolor(matrix_color)
    
    for char in text:
        turtle.write(char, align="left", font=("Courier", 20, "normal"))  # Courier for Matrix feel
        turtle.penup()
        turtle.forward(12)  # Smaller step for Courier font
        turtle.pendown()
        time.sleep(0.05)  # Faster animation for Matrix effect

# Write first line
write_line_by_letter(line1, -250, 50)  # Upper line

# Write second line
write_line_by_letter(line2, -250, -20)  # Lower line, below the first

# Pause for 2 seconds to let the interviewers read the complete message
time.sleep(2)

# Clear the screen to prepare for the flag
turtle.clear()

# ===============================
# PART 2: A Child Holding the Vietnam Flag
# ===============================

# Set the background to light blue for a sky-like scene
turtle.bgcolor("lightblue")

# Reset turtle and set speed
turtle.speed(5)
turtle.pensize(3)

# Draw the child's head: a circle
turtle.penup()
turtle.goto(0, 50)
turtle.pendown()
turtle.fillcolor("peachpuff")
turtle.begin_fill()
turtle.circle(30)  # Head
turtle.end_fill()

# Draw the body: a simple rectangle
turtle.penup()
turtle.goto(-20, 20)
turtle.pendown()
turtle.fillcolor("blue")  # Shirt color
turtle.begin_fill()
for _ in range(2):
    turtle.forward(40)
    turtle.right(90)
    turtle.forward(60)
    turtle.right(90)
turtle.end_fill()

# Draw left arm (holding flag)
turtle.penup()
turtle.goto(-20, 10)
turtle.setheading(180)  # Left
turtle.pendown()
turtle.forward(30)

# Draw right arm
turtle.penup()
turtle.goto(20, 10)
turtle.setheading(0)  # Right
turtle.pendown()
turtle.forward(30)

# Draw left leg
turtle.penup()
turtle.goto(-10, -40)
turtle.setheading(270)
turtle.pendown()
turtle.forward(40)

# Draw right leg
turtle.penup()
turtle.goto(10, -40)
turtle.setheading(270)
turtle.pendown()
turtle.forward(40)

# Draw the flag in the left hand
# Flag pole
turtle.penup()
turtle.goto(-50, 10)
turtle.setheading(90)
turtle.pendown()
turtle.forward(80)  # Pole height

# Flag rectangle
turtle.penup()
turtle.goto(-50, 90)
turtle.pendown()
turtle.fillcolor("#DA251D")  # Red flag
turtle.begin_fill()
turtle.setheading(0)
turtle.forward(60)
turtle.right(90)
turtle.forward(40)
turtle.right(90)
turtle.forward(60)
turtle.right(90)
turtle.forward(40)
turtle.end_fill()

# Draw the star on the flag using a for loop
turtle.penup()
turtle.goto(-35, 110)  # Center of flag
turtle.pendown()
turtle.fillcolor("#FFFF00")  # Yellow star
turtle.begin_fill()
for i in range(5):
    turtle.forward(15)  # Smaller star
    turtle.right(144)
turtle.end_fill()

# Keep the window open
turtle.done()

# Keep the window open so we can admire the flag
turtle.done()