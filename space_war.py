# SPACE WAR GAME
# 07/01/2020
# Python 3.9
# MADE BY @TampellaGiacomo - credits: @TokyoEdTech

import os
import random
import turtle
import winsound
import time
import platform

turtle.fd(0)
turtle.speed(0)
turtle.bgcolor("black")
turtle.bgpic("bgp.gif")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)

wn = turtle.Screen()
wn.title("Space Wars")
wn.register_shape("enemy.gif")
wn.register_shape("ally.gif")
wn.register_shape("player.gif")

# PLAY SOUND
def play_sound(sound_file, time = 0):
    winsound.PlaySound(sound_file, winsound.SND_ASYNC)

# SETTINGS
settings_pen = turtle.Turtle()
settings_pen.color("white")
settings_pen.penup()
settings_pen.setposition(-300, -370)
settingsstring = "Red: Enemies (HIT: +100pts, COLLISION: -100pts)\nOrange: Allies (HIT: -50pts)"
settings_pen.write(settingsstring, False, align="left", font=("Arial", 16, "bold"))
settings_pen.hideturtle()

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        # BOUNDARY DETECTION
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
        (self.xcor() <= (other.xcor() + 20)) and \
        (self.ycor() >= (other.ycor() - 20)) and \
        (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False

class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 4
        self.lives = 3

    def move_left():
        player.speed = -0.6

    def move_right():
        player.speed = 0.6

    def move_player():
        x = player.xcor()
        x += player.speed
        if x < -280:
            x = -280
        player.setx(x)
        if x > 280:
            x = 280
        player.setx(x)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0, 360))

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0, 360))

    def move(self):
        self.fd(self.speed)

        # BOUNDARY DETECTION
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)


class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            # PLAY MISSILE SOUND
            play_sound("laser.wav")
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):
        if self.status == "ready":
            self.goto(-1000, 1000)

        if self.status == "firing":
            self.fd(self.speed)

        # BORDER CHECK
        if self.xcor() < -290 or self.xcor() > 290 or \
            self.ycor() < -290 or self.ycor() > 290:
                self.goto(-1000, 1000)
                self.status = "ready"

class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        #DRAW BORDER
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range (4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-450, 210)
        self.pen.write(msg, font=("Arial", 16, "normal"))


# CREATE GAME OBJECT
game = Game()
# DRAW THE GAME BORDER
game.draw_border()

# SHOW THE GAME STATUS
game.show_status()

#CREATE MY SPRITES
player = Player("triangle", "white", 0, 0)
# enemy = Enemy("circle", "red", -100, 0)
missile = Missile("triangle", "yellow", 0, 0)
# ally = Ally("square", "green", 100, 0)

enemies = []
for i in range(6):
    enemies.append(Enemy("enemy.gif","red", -100, 0))
    #enemies.shape("enemy.gif")

allies = []
for i in range(6):
    allies.append(Ally("ally.gif", "green", 100, 0))

# KEYBOARD BINDINGS
turtle.onkeypress(player.turn_left, "Left")
turtle.onkeypress(player.turn_right, "Right")
turtle.onkeypress(player.accelerate, "Up")
turtle.onkeypress(player.decelerate, "Down")
turtle.onkeypress(missile.fire, "space")

turtle.listen()
#MAIN GAME LOOP
while True:
    turtle.update()
    time.sleep(0.05)

    player.move()
    missile.move()
    for enemy in enemies:
        enemy.move()

        # CHECK FOR A COLLISION BETWEEN THE PLAYER AND THE ENEMY
        if player.is_collision(enemy):
            play_sound("explosion.wav")
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score -= 100
            game.show_status()

            # CHECK FOR A COLLISION BETWEEN THE MISSILE AND THE ENEMY
        if missile.is_collision(enemy):
            play_sound("explosion.wav")
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            # INCREASE THE SCORE
            game.score += 100
            game.show_status()


    for ally in allies:
        ally.move()

        # CHECK FOR A COLLISION BETWEEN THE MISSILE AND THE ALLY
        if missile.is_collision(ally):
            play_sound("explosion.wav")
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            # DECREASE THE SCORE
            game.score -= 50
            game.show_status()


delay = raw_input("Press enter to finish. > ")
