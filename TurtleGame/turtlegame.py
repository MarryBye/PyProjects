from turtle import *

class Sprite(Turtle):
    def __init__(self, x, y, color="green", shape="circle", step=5):
        super().__init__()
        self.speed(999)
        self.penup()
        self.goto(x, y)
        self.color(color)
        self.shape(shape)
        self.health = 3

        self.step = step

    def is_touch(self, sprite):
        dist = self.distance(sprite.xcor(), sprite.ycor())
        if dist < 10:
           return True
        else:
           return False

    def set_move(self, x_start, y_start, x_end, y_end):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        self.goto(x_start, y_start)
        self.setheading(self.towards(x_end, y_end))

    def make_step(self):
        self.forward(10)

        if self.distance(self.x_end,self.y_end) < self.step:
            self.set_move(self.x_end, self.y_end, self.x_start, self.y_start)

    def goUp(self):
        if self.ycor() < 160:
            self.goto(self.xcor(), self.ycor() + self.step)

    def goRight(self):
        if self.xcor() < 160:
            self.goto(self.xcor() + self.step, self.ycor())

    def goLeft(self):
        if self.xcor() > -160:
            self.goto(self.xcor() - self.step, self.ycor())

    def goDown(self):
        if self.ycor() > -160:
            self.goto(self.xcor(), self.ycor() - self.step)

print("\t\t\tLUKIANOV VIKTOR")
print("\n\tСобери все монетки и не попадись противнику!\n")

hideturtle()
color("lightblue")
width(5000)
forward(1)

width(3)
penup()
goto(-165, 165)
pendown()

color("black")
for i in range(4):
    forward(165 * 2)
    right(90)

player = Sprite(0, -75)

goal_1 = Sprite(-150, -150, "yellow")
goal_2 = Sprite(150, 150, "yellow")
goal_3 = Sprite(-150, 150, "yellow")
goal_4 = Sprite(150, -150, "yellow")
goal_5 = Sprite(-30, 0, "yellow")
goal_5.set_move(-30, 0, 30, 0)

enemy_1 = Sprite(-150, 0, "red", "square")
enemy_1.set_move(-150, 0, -60, 0)

enemy_2 = Sprite(150, 0, "red", "square")
enemy_2.set_move(150, 0, 60, 0)

enemy_3 = Sprite(0, 150, "red", "square")
enemy_3.set_move(0, 150, 0, 60)

enemy_4 = Sprite(-40, 0, "red", "square")
enemy_5 = Sprite(40, 0, "red", "square")
enemy_6 = Sprite(0, 40, "red", "square")
enemy_7 = Sprite(0, -40, "red", "square")

heal_1 = Sprite(0, -150, "blue", "square")

scr = player.getscreen()
scr.onkey(player.goUp, "w")
scr.onkey(player.goDown, "s")
scr.onkey(player.goLeft, "a")
scr.onkey(player.goRight, "d")
scr.listen()

total_score = 0

while total_score < 5:
    enemy_1.make_step()
    enemy_2.make_step()
    enemy_3.make_step()
    goal_5.make_step()
    if player.is_touch(goal_1):
        goal_1.hideturtle()
        total_score += 1
        goal_1.goto(9999, 9999)
        print(f"Вы собрали {total_score} монеток из 5")
    if player.is_touch(goal_2):
        goal_2.hideturtle()
        total_score += 1
        goal_2.goto(9999, 9999)
        print(f"Вы собрали {total_score} монеток из 5")
    if player.is_touch(goal_3):
        goal_3.hideturtle()
        total_score += 1
        goal_3.goto(9999, 9999)
        print(f"Вы собрали {total_score} монеток из 5")
    if player.is_touch(goal_4):
        goal_4.hideturtle()
        total_score += 1
        goal_4.goto(9999, 9999)
        print(f"Вы собрали {total_score} монеток из 5")
    if player.is_touch(goal_5):
        goal_5.hideturtle()
        total_score += 1
        goal_5.goto(9999, 9999)
        print(f"Вы собрали {total_score} монеток из 5")
    if player.is_touch(heal_1):
        heal_1.hideturtle()
        player.health += 1
        heal_1.goto(9999, 9999)
        print(f"Вы подобрали аптечку и теперь у вас {player.health} жизней!")
    if player.is_touch(enemy_1) or player.is_touch(enemy_2) or player.is_touch(enemy_3) or player.is_touch(enemy_4) or player.is_touch(enemy_5) or player.is_touch(enemy_6) or player.is_touch(enemy_7):
        if player.health > 0:
            player.health -= 1
            print(f"Вы задели противника! У вас осталось {player.health} жизней!")
            player.goto(0, -75)
        else:
            print(f"Вы проиграли! Попробуйте еще раз!")
            break
else:
    print(f"Вы победили! Вы собрали все монетки!")

goal_1.hideturtle()
goal_2.hideturtle()
goal_3.hideturtle()
goal_4.hideturtle()
goal_5.hideturtle()
enemy_1.hideturtle()
enemy_2.hideturtle()
enemy_3.hideturtle()
enemy_4.hideturtle()
enemy_5.hideturtle()
enemy_6.hideturtle()
enemy_7.hideturtle()
heal_1.hideturtle()

done()
