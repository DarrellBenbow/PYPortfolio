import turtle
import time
#create a screen
sc = turtle.Screen()
sc.title("Pong")
sc.bgcolor("white")
sc.setup(width=1000, height=800)


#left paddle
left_paddle = turtle.Turtle()
left_paddle.speed(0)
left_paddle.shape("square")
left_paddle.color("black")
left_paddle.shapesize(stretch_wid=6, stretch_len=2)
left_paddle.penup()
left_paddle.goto(-400, 0)

right_paddle = turtle.Turtle()
right_paddle.speed(0)  
right_paddle.shape("square")
right_paddle.color("black")
right_paddle.shapesize(stretch_wid=6, stretch_len=2)
right_paddle.penup()
right_paddle.goto(400, 0)


#Ball of circle shape
hit_ball = turtle.Turtle()
hit_ball.speed(40)
hit_ball.shape("circle")
hit_ball.color("red")
hit_ball.penup()
hit_ball.goto(0, 0)
hit_ball.goto(0, 0)
hit_ball.dx = 5 #change the value to increase or decrease speed
hit_ball.dy = -5 #change the value to increase or decrease speed    
#Initializing the score
left_player_score = 0
right_player_score = 0
 
 #Display the score
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("blue")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 260)
sketch.write("Left Player: 0  Right Player: 0", align="center", font=("Courier", 24, "normal"))

#Function to move the left paddle up
def paddleaup():
    y = left_paddle.ycor()
    if y < 250: # Limit the paddle movement to the top of the screen
        y += 20
    left_paddle.sety(y)

#Function to move the left paddle down
def paddleadown():
    y = left_paddle.ycor()
    if y > -240: # Limit the paddle movement to the bottom of the screen
        y -= 20
    left_paddle.sety(y)

#Function to move the right paddle up
def paddlebup():
    y = right_paddle.ycor()
    if y < 250: # Limit the paddle movement to the top of the screen
        y += 20
    right_paddle.sety(y)

#Function to move the right paddle down
def paddlebdown():
    y = right_paddle.ycor()
    if y > -240: # Limit the paddle movement to the bottom of the screen
        y -= 20
    right_paddle.sety(y)

#Keyboard bindings
sc.listen()
sc.onkeypress(paddleaup, "w") # 
sc.onkeypress(paddleadown, "s")
sc.onkeypress(paddlebup, "Up")
sc.onkeypress(paddlebdown, "Down")

#Main game loop
while True:
    sc.update()  # Update the screen
    time.sleep(0.01)  # Control the speed of the game add delay to make things smoother
    hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
    hit_ball.sety(hit_ball.ycor() + hit_ball.dy)
    #Border checking
    if hit_ball.ycor() > 280:
        hit_ball.sety(280)
        hit_ball.dy *= -1
    if hit_ball.ycor() < -280:
        hit_ball.sety(-280)
        hit_ball.dy *= -1
    if hit_ball.xcor() > 500:
        hit_ball.goto(0, 0)
        hit_ball.dx *= -1
        left_player_score += 1
        sketch.clear()
        sketch.write("Left Player: {}  Right Player: {}".format(left_player_score, right_player_score), align="center", font=("Courier", 24, "normal"))
    if hit_ball.xcor() < -500:
        hit_ball.goto(0, 0)
        hit_ball.dx *= -1
        right_player_score += 1
        sketch.clear()
        sketch.write("Left Player: {}  Right Player: {}".format(left_player_score, right_player_score), align="center", font=("Courier", 24, "normal"))
    font = ("Courier", 24, "normal")
    # Paddle and ball collisions
    if (hit_ball.xcor() > 360 and hit_ball.xcor() < 370) and (hit_ball.ycor() < right_paddle.ycor() + 50 and hit_ball.ycor() > right_paddle.ycor() - 50):
        hit_ball.setx(360)
        hit_ball.dx *= -1
    if (hit_ball.xcor() < -360 and hit_ball.xcor() > -370) and (hit_ball.ycor() < left_paddle.ycor() + 50 and hit_ball.ycor() > left_paddle.ycor() - 50):
        hit_ball.setx(-360)
        hit_ball.dx *= -1
        