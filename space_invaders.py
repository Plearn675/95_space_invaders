import turtle
import time

# --- 1. SETUP THE GAME SCREEN ---
screen = turtle.Screen()
screen.setup(width=600, height=800)
screen.bgcolor("black")
screen.title("Space Invaders by Turtle")
screen.tracer(0) # Turns off screen updates, we will update it manually later

# --- Score and Lives (Goal 2: Info Bar) ---
score = 0
lives = 3
score_pen = turtle.Turtle()
score_pen.speed(0) # Animation speed 0 means 'fastest'
score_pen.color("white")
score_pen.penup() # Do not draw lines when moving
# Position the score at the top
score_pen.setposition(-290, 360)
score_pen.hideturtle() # Make the turtle icon invisible

# Function to draw the score/lives
def update_score():
    score_pen.clear() # Clear previous text
    score_pen.write(f"Score: {score}  Lives: {lives}", align="left", font=("Courier", 18, "normal"))

update_score() # Initial draw

# --- 2. PLAYER SHIP (Goal 3) ---
player = turtle.Turtle()
player.color("green")
player.shape("triangle") # A triangle is a simple spaceship shape
player.penup()
player.speed(0)
# Start the player at the bottom center of the screen
player.setposition(0, -300)
player.setheading(90) # Point the triangle up (90 degrees)
player_speed = 15 # Pixels to move per key press

# --- 3. MOVEMENT FUNCTIONS (Goal 4) ---
def move_left():
    x = player.xcor() # Get current x-coordinate
    x -= player_speed
    # Boundary check: Don't let the player move past the left edge (-280)
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor() # Get current x-coordinate
    x += player_speed
    # Boundary check: Don't let the player move past the right edge (280)
    if x > 280:
        x = 280
    player.setx(x)

# --- 4. KEYBOARD BINDINGS ---
screen.listen() # Tell the screen to listen for keyboard input
screen.onkeypress(move_left, "Left") # Bind the 'Left' arrow key to move_left
screen.onkeypress(move_right, "Right") # Bind the 'Right' arrow key to move_right

# --- 5. MAIN GAME LOOP ---
game_on = True
while game_on:
    # ------------------------------------
    # LINE 67: THE 'try' KEYWORD IS REQUIRED, FOLLOWED BY A COLON
    try:
        screen.update()

        # --- YOUR GAME LOGIC WILL GO HERE ---
        # e.g., move_missiles(), check_collisions()

    # LINE 69: The 'except' block must follow 'try' and catch the error
    except turtle.Terminator:
        print("Game closed gracefully.")
        game_on = False  # Set the flag to False to exit the while loop cleanly
        break
    # ------------------------------------