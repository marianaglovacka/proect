from tkinter import *
import random

WIDTH = 900
HEIGHT = 300
#Ширина і висота ракетки
PAD_W = 10
PAD_H = 100

#Збільшення швидкості м'яча
BALL_SPEED_UP = 1.05
#Максимальна швидкість м'яча
BALL_MAX_SPEED = 40
#Радіус м'яча
BALL_RADIUS = 30

INITIAL_SPEED = 20
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED
#Рахунок гравців
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0
#Зміна яка відповідає за відстань до правого краю поля
right_line_distance = WIDTH - PAD_W


def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)


def spawn_ball():
    global BALL_X_SPEED
    #Виставляєм м'яч по центру
    c.coords(BALL, WIDTH / 2 - BALL_RADIUS / 2,
             HEIGHT / 2 - BALL_RADIUS / 2,
             WIDTH / 2 + BALL_RADIUS / 2,
             HEIGHT / 2 + BALL_RADIUS / 2)
    #Задаємо м'ячу напрямок в сторону прогрвшого гравця і знижаємо швидкість до початкової
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED) / abs(BALL_X_SPEED)

#Функція віштовхування м'яча
def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == "strike":
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED



root = Tk()
root.title("PythonicWay Pong")

#Анімація
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#003300")
c.pack()
#Елементи ігрового поля

#ліва лінія
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
#права лінія
c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="white")
#центральна лінія
c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white")

#створюємо м'яч
BALL = c.create_oval(WIDTH / 2 - BALL_RADIUS / 2,
                     HEIGHT / 2 - BALL_RADIUS / 2,
                     WIDTH / 2 + BALL_RADIUS / 2,
                     HEIGHT / 2 + BALL_RADIUS / 2, fill="white")

#ліва ракетка
LEFT_PAD = c.create_line(PAD_W / 2, 0, PAD_W / 2, PAD_H, width=PAD_W, fill="yellow")
#права ракетка
RIGHT_PAD = c.create_line(WIDTH - PAD_W / 2, 0, WIDTH - PAD_W / 2,
                          PAD_H, width=PAD_W, fill="yellow")

#текст
p_1_text = c.create_text(WIDTH - WIDTH / 6, PAD_H / 4,
                         text=PLAYER_1_SCORE,
                         font="Arial 20",
                         fill="white")

p_2_text = c.create_text(WIDTH / 6, PAD_H / 4,
                         text=PLAYER_2_SCORE,
                         font="Arial 20",
                         fill="white")
#по горизонталі
BALL_X_CHANGE = 20
#по вертикалі
BALL_Y_CHANGE = 0


def move_ball():
    #координати сторін м'яча і його цетра
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2
    #якщо ми далеко від вертикальної лінії то просто рухаємо м'яча
    if ball_right + BALL_X_SPEED < right_line_distance and \
            ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    #якщо м'яч торкається правой або лівої сторони границі поля
    elif ball_right == right_line_distance or ball_left == PAD_W:
        #перевіряємо якої сторони торкаємося
        if ball_right > WIDTH / 2:
            #Якщо правою, то порівнюємо позицію центру м'яча з позицією правої ракетки І якщо м'яч у межах ракетки робимо відскок
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce("strike")
            else:
                #Інакше гравець пропустив - тут залишимо поки що pass, його ми замінимо на підрахунок очок і респаун м'ячика
                update_score("left")
                spawn_ball()
        else:
            #теж саме для лівого гравця
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce("strike")
            else:
                update_score("right")
                spawn_ball()
    #Перевірка ситуації, в якій м'ячик може вилетіти за межі ігрового поля. У такому разі просто рухаємо його до межі поля.
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance - ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left + PAD_W, BALL_Y_SPEED)
    #горизонтальний відскок
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")

#швидкість з якою будуть їздити ракетки
PAD_SPEED = 20
#швидкість лівої
LEFT_PAD_SPEED = 0
#швидкість правої
RIGHT_PAD_SPEED = 0
#функція для пересування обох ракеток
def move_pads():
    PADS = {LEFT_PAD: LEFT_PAD_SPEED,
            RIGHT_PAD: RIGHT_PAD_SPEED}
    #перебираємо ракетки
    for pad in PADS:
        #рухаємо ракетку з завданою швидкістю
        c.move(pad, 0, PADS[pad])
        #якщо ракетка вилітає за ігрове поле то повертаємо її на місце
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])


def main():
    move_ball()
    move_pads()
    #визиваємо саму себе кожні 30 мілісекунд
    root.after(30, main)

#встановлюємо фокус на Canvas щоб вона реагувала на нажимання клавіші
c.focus_set()

#функція для обробки нажимання клавіші
def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "s":
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED
        
c.bind("<KeyPress>", movement_handler)

main()
root.mainloop()