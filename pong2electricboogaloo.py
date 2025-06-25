import turtle
import time

# --- Setup Screen ---
sc = turtle.Screen()
sc.title("Pong")
sc.bgcolor("purple")
sc.setup(width=1000, height=800)
sc.tracer(0)

# --- Menu Function ---
def show_menu():
    menu = turtle.Turtle()
    menu.hideturtle()
    menu.penup()
    menu.color("yellow")
    menu.goto(0, 50)
    menu.write("PONG GAME", align="center", font=("Courier", 40, "bold"))
    menu.goto(0, 0)
    menu.write("Press SPACE to Start\nPress ESC to Exit", align="center", font=("Courier", 24, "normal"))
    return menu

# --- Exit Function ---
def exit_game():
    sc.bye()

# --- Main Game Function ---
def start_game():
    menu.clear()
    # --- Paddle Setup ---
    def create_paddle(x):
        paddle = turtle.Turtle()
        paddle.speed(0)
        paddle.shape("square")
        paddle.color("blue")
        paddle.shapesize(stretch_wid=6, stretch_len=2)
        paddle.penup()
        paddle.goto(x, 0)
        return paddle

    left_paddle = create_paddle(-400)
    right_paddle = create_paddle(400)

    # --- Ball Setup ---
    hit_ball = turtle.Turtle()
    hit_ball.speed(0)
    hit_ball.shape("circle")
    hit_ball.color("red")
    hit_ball.penup()
    hit_ball.goto(0, 0)
    hit_ball.dx = 5
    hit_ball.dy = -5

    # --- Score Setup ---
    left_player_score = 0
    right_player_score = 0
    sketch = turtle.Turtle()
    sketch.speed(0)
    sketch.color("blue")
    sketch.penup()
    sketch.hideturtle()
    sketch.goto(0, 260)
    sketch.write("Left Player: 0  Right Player: 0", align="center", font=("Courier", 24, "normal"))

    # --- Paddle Movement Functions ---
    def paddleaup():
        y = left_paddle.ycor()
        if y < 250:
            y += 20
        left_paddle.sety(y)

    def paddleadown():
        y = left_paddle.ycor()
        if y > -240:
            y -= 20
        left_paddle.sety(y)

    def paddlebup():
        y = right_paddle.ycor()
        if y < 250:
            y += 20
        right_paddle.sety(y)

    def paddlebdown():
        y = right_paddle.ycor()
        if y > -240:
            y -= 20
        right_paddle.sety(y)

    # --- Keyboard Bindings ---
    sc.listen()
    sc.onkeypress(paddleaup, "w")
    sc.onkeypress(paddleadown, "s")
    sc.onkeypress(paddlebup, "Up")
    sc.onkeypress(paddlebdown, "Down")
    sc.onkeypress(exit_game, "Escape")

    # --- Collision Check Function ---
    def check_collision(ball, paddle):
        return (abs(ball.xcor() - paddle.xcor()) < 30) and (abs(ball.ycor() - paddle.ycor()) < 60)

    # --- Main Game Loop ---
    while True:
        sc.update()
        time.sleep(0.01)
        hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
        hit_ball.sety(hit_ball.ycor() + hit_ball.dy)

        # Border checking
        if hit_ball.ycor() > 280:
            hit_ball.sety(280)
            hit_ball.dy *= -1
        if hit_ball.ycor() < -280:
            hit_ball.sety(-280)
            hit_ball.dy *= -1

        # Score update
        if hit_ball.xcor() > 500:
            hit_ball.goto(0, 0)
            hit_ball.dx *= -1
            left_player_score += 1
            sketch.clear()
            sketch.write(f"Left Player: {left_player_score}  Right Player: {right_player_score}", align="center", font=("Courier", 24, "normal"))
        if hit_ball.xcor() < -500:
            hit_ball.goto(0, 0)
            hit_ball.dx *= -1
            right_player_score += 1
            sketch.clear()
            sketch.write(f"Left Player: {left_player_score}  Right Player: {right_player_score}", align="center", font=("Courier", 24, "normal"))

        # Paddle collisions
        if check_collision(hit_ball, right_paddle):
            hit_ball.setx(right_paddle.xcor() - 30)
            hit_ball.dx *= -1
        if check_collision(hit_ball, left_paddle):
            hit_ball.setx(left_paddle.xcor() + 30)
            hit_ball.dx *= -1

        # Win condition (first to 5)
        if left_player_score == 5 or right_player_score == 5:
            winner = "Left" if left_player_score == 5 else "Right"
            sketch.goto(0, 0)
            sketch.write(f"{winner} Player Wins!", align="center", font=("Courier", 36, "bold"))
            break

# --- Show Menu and Bindings ---
menu = show_menu()
sc.listen()
sc.onkeypress(start_game, "space")
sc.onkeypress(exit_game, "Escape")
sc.mainloop()
