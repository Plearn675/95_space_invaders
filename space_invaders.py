import turtle
import time
import math
import random  # Needed for random enemy firing

# --- 1. SETUP THE GAME SCREEN (Goal 1) ---
screen = turtle.Screen()
screen.setup(width=600, height=800)
screen.bgcolor("black")
screen.title("Space Invaders by Turtle")
screen.tracer(0)  # Manual screen updates

# --- 2. SCORE AND LIVES (Goal 2) ---
score = 0
lives = 3
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 360)
score_pen.hideturtle()


def update_score():
    score_pen.clear()
    score_pen.write(f"Score: {score}  Lives: {lives}", align="left", font=("Courier", 18, "normal"))


update_score()  # Initial draw

# --- 3. PLAYER SHIP (Goal 3) ---
player = turtle.Turtle()
player.color("green")
player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0, -300)
player.setheading(90)
player_speed = 15

# --- 4a. PLAYER MISSILE SETUP (Goal 5) ---
missile = turtle.Turtle()
missile.color("yellow")
missile.shape("triangle")
missile.shapesize(stretch_wid=0.5, stretch_len=0.5)
missile.penup()
missile.speed(0)
missile.setheading(90)
missile.hideturtle()

missile_speed = 4  # Player missile speed

missile_state = "ready"  # 'ready' or 'fire'

# --- 4b. ENEMY MISSILE SETUP (New Goal) ---
enemy_missile = turtle.Turtle()
enemy_missile.color("orange")
enemy_missile.shape("square")
enemy_missile.shapesize(stretch_wid=0.4, stretch_len=0.4)
enemy_missile.penup()
enemy_missile.speed(0)
enemy_missile.setheading(270)  # Points down
enemy_missile.hideturtle()

enemy_missile_speed = 0.25  # Enemy missile speed
enemy_missile_state = "ready"


# --- 5. MOVEMENT FUNCTIONS ---
def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -280:
        x = -280
    player.setx(x)


def move_right():
    x = player.xcor()
    x += player_speed
    if x > 280:
        x = 280
    player.setx(x)


def fire_missile():
    global missile_state
    if missile_state == "ready":
        missile_state = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        missile.setposition(x, y)
        missile.showturtle()


# --- 6. COLLISION FUNCTION (Goal 7) ---
def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 20:
        return True
    else:
        return False


# --- 7. ENEMY SETUP (Goal 6 Refined: 3x10 Grid) ---
enemies = []
num_enemies = 30
aliens_per_row = 10
num_rows = num_enemies // aliens_per_row

start_x = -240
start_y = 250
x_spacing = 50
y_spacing = 50

for row in range(num_rows):
    for column in range(aliens_per_row):
        enemy = turtle.Turtle()
        enemy.color("red")
        enemy.shape("circle")
        enemy.penup()
        enemy.speed(0)

        x = start_x + (column * x_spacing)
        y = start_y - (row * y_spacing)

        enemy.setposition(x, y)
        enemies.append(enemy)

# Variable for enemy formation movement
enemy_speed_x = 0.5

# --- 8. KEYBOARD BINDINGS ---
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_missile, "space")

# --- 9. MAIN GAME LOOP (The Engine) ---
game_on = True
while game_on:
    try:
        # 1. Update Control
        time.sleep(0.01)
        screen.update()

        # 2. ENEMY MOVEMENT LOGIC (New Goal)
        move_down = False

        for enemy in enemies:
            # Move the enemy horizontally
            x = enemy.xcor()
            x += enemy_speed_x
            enemy.setx(x)

            # Check for wall collision (Reverse direction and set to move down)
            if enemy.xcor() > 280 or enemy.xcor() < -280:
                move_down = True

        # Move formation down if a wall was hit by any enemy
        if move_down:
            enemy_speed_x *= -1  # Reverse direction
            for enemy in enemies:
                y = enemy.ycor()
                y -= 20  # Move down 20 pixels
                enemy.sety(y)

        # 3. ENEMY FIRE LOGIC (New Goal)
        if enemy_missile_state == "ready":
            # 1 in 500 chance per frame to fire
            if random.randint(1, 500) == 1:
                firing_alien = random.choice(enemies)

                # Check if the alien is still "alive" (on screen)
                if firing_alien.ycor() < 1000:
                    enemy_missile_state = "fire"
                    x = firing_alien.xcor()
                    y = firing_alien.ycor() - 20
                    enemy_missile.setposition(x, y)
                    enemy_missile.showturtle()

        # 4. ENEMY MISSILE MOVEMENT AND PLAYER COLLISION (New Goal)
        if enemy_missile_state == "fire":
            y = enemy_missile.ycor()
            y -= enemy_missile_speed  # Moves DOWN
            enemy_missile.sety(y)

            # Check for Player-Hit Collision
            if is_collision(enemy_missile, player):
                enemy_missile.hideturtle()
                enemy_missile_state = "ready"

                # Lose a life
                lives -= 1
                update_score()

                # Optional: Move player back to start position after being hit
                player.setposition(0, -300)

                # Check for Game Over
                if lives == 0:
                    print("GAME OVER")
                    game_on = False

            # Check if enemy missile hit the bottom of the screen (reset it)
            if enemy_missile.ycor() < -370:
                enemy_missile.hideturtle()
                enemy_missile_state = "ready"

        # 5. PLAYER MISSILE MOVEMENT LOGIC
        if missile_state == "fire":
            y = missile.ycor()
            y += missile_speed  # Moves UP
            missile.sety(y)

        # Check if the missile hit the top of the screen (reset it)
        if missile.ycor() > 370:
            missile.hideturtle()
            missile_state = "ready"

        # 6. PLAYER MISSILE vs. ENEMY COLLISION LOGIC (Goal 7)
        for enemy in enemies:
            if is_collision(missile, enemy) and missile_state == "fire":
                # Reset the missile
                missile.hideturtle()
                missile_state = "ready"

                # Move enemy off-screen (simulating destruction)
                enemy.setposition(0, 1000)

                # Update the score
                score += 10
                update_score()

                # Missile only hits one target per shot
                break

    except turtle.Terminator:
        print("Game closed gracefully.")
        game_on = False
        break