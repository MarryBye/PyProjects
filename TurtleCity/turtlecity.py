from turtle import *

sky_color = "lightblue"
sun_color = "yellow"
star_color = "white"

default_width = 5


# Функция чтобы переходить на место не поднимая/опуская перо
# Использование: go(координата_х, координата_у)
def go(x, y):
    penup()
    goto(x, y)
    pendown()


# Функция чтобы рисовать солнце
# Использование: sun(координата_х, координата_у, радиус)
def sun(x, y, radius):
    go(x, y)
    color(sun_color)
    width(default_width)
    begin_fill()
    for i in range(20):
        forward(radius)
        left(100)
    end_fill()
    go(x, y)
    setheading(0)


# Функция чтобы рисовать солнце
# Использование: star(координата_х, координата_у, радиус)
def star(x, y, radius):
    go(x, y)
    color(star_color)
    width(default_width)
    begin_fill()
    for i in range(14):
        forward(radius)
        left(144)
    end_fill()
    go(x, y)
    setheading(0)


# Функция чтобы нарисовать дом
# Использование: house(координата_х, координата_у, ширина, высота, тип_окна (circle, triangle, square), тип_крыши (square, triangle), цвет_крыши, цвет_дома)
def house(x, y, wid, hg, window_type, roof_type, color_roof, color_base):
    width(default_width)
    go(x, y)

    # Рисуем основу дома
    color(color_base)
    begin_fill()
    for i in range(2):
        forward(wid)
        left(90)
        forward(hg)
        left(90)
    end_fill()

    left(90)
    forward(hg)
    right(90)
    color(color_roof)

    # Рисуем крышу
    if roof_type == "triangle":
        begin_fill()
        for i in range(3):
            forward(wid)
            left(120)
        end_fill()
    else:
        begin_fill()
        for i in range(2):
            forward(wid)
            left(90)
            forward(5)
            left(90)
        end_fill()

    # Идем рисовать дверь. old_x и old_y чтобы потом вернуться назад в угол дома, чтобы окно потом рисовалось независимо ни от чего
    old_x, old_y = xcor(), ycor()
    penup()
    right(90)
    forward(hg)
    left(90)
    forward(wid / 2 - 2.5)
    pendown()

    # Рисуем дверь
    color("brown")
    begin_fill()
    for i in range(2):
        forward(5)
        left(90)
        forward(15)
        left(90)
    end_fill()

    # Вернулись туда, где начинали чтобы правильно нарисовать окно
    go(old_x, old_y)

    # Рисуем окно
    window_width = wid / 3  # Ширина окна это половина ширины дома
    margin = (
                         wid - window_width) / 2  # Считаем отступы слева и справа (дом 100 в ширину, окно будет 100 / 2. 100 - 50 = 50. Значит левый и правый отступ будут 50 / 2 = 25)
    if window_type == "square":
        penup()
        forward(margin)
        right(90)
        forward(margin)
        pendown()

        color("black")
        begin_fill()
        for i in range(4):
            forward(window_width)
            left(90)
        color("cyan")
        end_fill()
    elif window_type == "circle":
        penup()
        color("cyan")
        right(90)
        forward(margin + window_width)
        left(90)
        forward(margin + window_width / 2)
        pendown()
        color("black")
        begin_fill()
        circle(window_width / 2)
        color("cyan")
        end_fill()
    elif window_type == "triangle":
        penup()
        forward(margin)
        right(90)
        forward(margin)
        forward(window_width)
        left(90)
        pendown()
        color("black")
        begin_fill()
        for i in range(3):
            forward(window_width)
            left(120)
        color("cyan")
        end_fill()
    go(x, y)
    setheading(0)


# Функция чтобы рисовать облако
# Использование: oblako(координата_х, координата_у, ширина_облака)
def oblako(x, y, wid):
    go(x, y)
    width(default_width)
    color("white")
    for i in range(wid):
        begin_fill()
        circle(15)
        end_fill()
        forward(25)
    begin_fill()
    circle(15)
    end_fill()
    go(x, y)
    setheading(0)


# Функция чтобы рисовать дерево
# Использование: tree(координата_х, координата_у, высота_дерева)
def tree(x, y, hg):
    width(15)
    color("brown")
    go(x, y)
    left(90)
    forward(hg)
    right(90)
    color("green")
    begin_fill()
    circle(hg / 3)  # Крона дерева = треть от высоты
    end_fill()
    go(x, y)
    setheading(0)


# Функция чтобі рисовать плоский цветов
# Использование: flower(координата_х, координата_у, цвет)
def flower(x, y, clr):
    width(default_width)
    color(clr)
    margin = 8
    radius = 5
    go(x + margin, y)
    begin_fill()
    circle(radius)
    end_fill()
    go(x - margin, y)
    begin_fill()
    circle(radius)
    end_fill()
    go(x, y + margin)
    begin_fill()
    circle(radius)
    end_fill()
    go(x, y - margin)
    begin_fill()
    circle(radius)
    end_fill()
    go(x, y)
    color("yellow")
    begin_fill()
    circle(radius)
    end_fill()
    go(x, y)
    setheading(0)


# Функция чтобы нарисовать траву
# Использование: grass(координата_х, координата_у, ширина_травы)
def grass(x, y, wd):
    color("green")
    width(default_width)
    go(x, y)
    grass_wd = 10
    for i in range(1, wd + 1):
        for j in range(3):
            left(120)
            forward(grass_wd)
        forward(grass_wd + 5)
    for j in range(3):
        left(120)
        forward(grass_wd)
    go(x, y)
    setheading(0)


# Функция чтобы нарисовать птичку
# Использование: bird(координата_х, координата_у)
def bird(x, y):
    color("black")
    width(default_width)
    go(x, y)
    left(23)
    for i in range(45):
        forward(1)
        right(1)
    left(45)
    for i in range(45):
        forward(1)
        right(1)
    go(x, y)
    setheading(0)


# Функция чтобы нарисовать камешек
# Использование: stone(координата_х, координата_у)
def stone(x, y):
    color("gray")
    width(default_width)
    go(x, y)
    begin_fill()
    circle(5)
    end_fill()
    go(x, y)
    setheading(0)

# Функция чтобы нарисовать гору
# Использование: stone(координата_х, координата_у, высота)
def rock(x, y, h):
    width(default_width)
    go(x, y)
    color("gray")
    begin_fill()
    for i in range(3):
        forward(h)
        left(120)
    end_fill()
    left(60)
    small_rock = h / 3
    forward(h - small_rock)
    right(60)
    color("white")
    begin_fill()
    for i in range(3):
        forward(small_rock)
        left(120)
    end_fill()

    go(x, y)
    setheading(0)

# Функция чтобы нарисовать человека
# Использование: steve(координата_х, координата_у, размер_человека, цвет_кожи, цвет_рубашки, цвет_штанов)
def steve(x, y, scale, clr1, clr2, clr3):
    w = 2
    width(w)
    go(x, y)

    # Голова
    head_width = scale + w

    color(clr1)
    begin_fill()
    for i in range(4):
        forward(head_width)
        left(90)
    end_fill()
    go(xcor(), ycor())

    # Туловище
    body_width = head_width
    body_length = body_width * 1.5
    hand_width = head_width * 0.5
    hand_length = body_length

    right(90)

    color(clr2)
    begin_fill()
    for i in range(2):
        forward(body_length)
        left(90)
        forward(body_width)
        left(90)
    end_fill()

    setheading(0)

    # Туловище - Рука (Левая)
    go(xcor() - hand_width, ycor())

    color(clr1)
    begin_fill()
    for i in range(2):
        forward(hand_width)
        right(90)
        forward(hand_length)
        right(90)
    end_fill()

    # Туловище - Рука (Левая) - Рукав
    color(clr2)
    begin_fill()
    for i in range(4):
        forward(hand_width)
        right(90)
    end_fill()

    # Туловище - Рука (Правая)
    go(xcor() + body_width + hand_width, ycor())

    color(clr1)
    begin_fill()
    for i in range(2):
        forward(hand_width)
        right(90)
        forward(hand_length)
        right(90)
    end_fill()

    # Туловище - Рука (Правая) - Рукав
    color(clr2)

    begin_fill()
    for i in range(4):
        forward(hand_width)
        right(90)
    end_fill()

    # Ноги
    legs_width = head_width
    legs_length = legs_width * 1.5

    go(xcor(), ycor() - body_length)
    right(90)

    color(clr3)
    begin_fill()
    for i in range(2):
        forward(legs_length)
        right(90)
        forward(legs_width)
        right(90)
    end_fill()

    # Ботинки
    go(xcor(), ycor() - legs_length)
    right(90)

    color("gray")
    begin_fill()
    for i in range(2):
        forward(legs_width)
        right(90)
        forward(legs_length * 0.15)
        right(90)
    end_fill()

    go(x, y)
    setheading(0)


# Функция чтобы нарисовать фон
# Использование: background()
def background():
    color(sky_color)
    width(1000)
    forward(1)
    penup()
    color("darkgreen")
    width(75)
    right(90)
    forward(225)
    left(90)
    pendown()
    forward(300)
    left(180)
    forward(600)
    go(0, 0)
    setheading(0)


if __name__ == "__main__":
    ground_y = -205
    speed(999)

    hideturtle()

    background()

    rock(-275, ground_y + 20, 450)

    sun(0, 200, 100)

    oblako(-175, 200, 5)
    oblako(-50, 150, 2)
    oblako(-100, 80, 3)

    bird(-150, 150)
    bird(-200, 115)
    bird(150, 190)

    house(-130, ground_y + 15, 50, 225, "square", "square", "gray", "white")
    house(-200, ground_y - 5, 100, 100, "circle", "square", "yellow", "red")
    house(30, ground_y + 15, 100, 125, "square", "square", "yellow", "pink")
    house(-75, ground_y - 10, 100, 175, "triangle", "square", "blue", "yellow")
    house(100, ground_y - 7, 100, 145, "square", "triangle", "brown", "green")

    tree(-215, ground_y, 225)

    flower(-200, ground_y - 44, "navy")
    flower(-155, ground_y - 55, "red")
    flower(35, ground_y - 37, "green")
    flower(150, ground_y - 28, "pink")

    grass(-175, ground_y - 38, 5)
    grass(-65, ground_y - 24, 5)
    grass(55, ground_y - 33, 5)
    grass(125, ground_y - 45, 5)

    stone(115, ground_y - 25)
    stone(-115, ground_y - 30)
    stone(10, ground_y - 33)
    stone(-175, ground_y - 55)

    steve(-175, ground_y - 25, 15, "wheat", "pink", "navy")
    steve(175, ground_y - 25, 15, "wheat", "green", "pink")
    steve(0, ground_y - 25, 15, "chocolate4", "yellow", "brown")

    done()