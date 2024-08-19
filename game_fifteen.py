# coding=UTF-8

''' Данная программа является одной из разновидностей игры "Пятнадцать" (https://ru.wikipedia.org/wiki/%D0%98%D0%B3%D1%80%D0%B0_%D0%B2_15)
 Не все комбинации являются решаемыми. Удачи! (Чтобы перейти сразу к финалу, достаточно разкомментарить строки 44-46'''

''' ПЕРЕМЕННЫЕ:
picture_fn - путь к jpg-файлу, используемому в игре (600*600)
picture_game - объект класса ImageTk, содержащий полное изображение
pics - список объектов класса ImageTk, сожержащих фрагменты изображения
win - список, содержащий номера блоков в состоянии "победа" (упорядоченная последовательность, включающая положение "дыры")
game -  список, содержащий номера блоков (включая "дыру") в текущем состоянии
labels - список, одержащий объекты класса tkinter.Label (блоки)
hole_nr - текущее положение "дыры" (код "дыры" - 99)"
'''
import tkinter as tk
from random import randint
from PIL import Image, ImageTk
import os
from pygame import mixer
import time

def init_game():
    global game_mode, hole_nr
    if game_mode == 4:
        win = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 99]
    else:
        win = [0, 1, 2, 3, 4, 5, 6, 7, 99]

    # hole = randint(0, game_mode*game_mode-1)
    # hole = game_mode * game_mode -1
    # win[hole] = 99
    game = []
    for i in range(game_mode*game_mode-1):
        n = randint(0, len(win)-1)
        piece = win.pop(n)
        game.append(piece)
    game.append(win[0])
    if game_mode == 4:
        win = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 99]
    else:
        win = [0, 1, 2, 3, 4, 5, 6, 7, 99]
    # win[hole] = 99
    #-------------------------------- один ход до победы
    # win = [0, 1, 2, 3, 4, 5, 6, 7, 99]
    # hole = 8
    # game = [0, 1, 2, 3, 4, 5, 99, 6, 7]
    #--------------------------------
    for i in range(game_mode*game_mode-1):
        if game[i] == 99:
            hole_nr = i
            break
    return game, hole_nr, win
def select_picture():
    pic_files = []
    pth = r'.\Files'
    files = os.listdir(pth)
    for i in files:
        if i[len(i)-3:len(i)] == 'jpg':
            pic_files.append(i)
    fn = pic_files[randint(0,len(pic_files)-1)]
    return fn
def cut_picture(fn):
    global game_mode, picture_game
    filename = os.path.join('.\\Files', fn)
    picture_game = Image.open(filename)
    picture_game.load()
    pics = []
    for i in range(game_mode*game_mode):
        x1 = (i % game_mode) * 600/game_mode
        x2 = x1 + 600/game_mode
        y1 = (i // game_mode) * 600/game_mode
        y2 = y1 + 600/game_mode
        pic = picture_game.crop((x1, y1, x2, y2))
        pic_tk = ImageTk.PhotoImage(pic)
        pics.append(pic_tk)
    picture_game = ImageTk.PhotoImage(picture_game)
    return pics
def my_key(event):
    global hole_nr, game, labels, picture_win, picture_game
    # ev = ''
    if event.keycode == 38: # Up
        if hole_nr > game_mode-1:
            game[hole_nr] = game[hole_nr-game_mode]
            game[hole_nr-game_mode] = 99
            hole_nr -= game_mode
            # ev = 'Up  '
    elif event.keycode == 40: # Down
        if hole_nr < game_mode*game_mode-game_mode:
            game[hole_nr] = game[hole_nr+game_mode]
            game[hole_nr+game_mode] = 99
            hole_nr += game_mode
            # ev = 'Down'
    elif event.keycode == 39: # Right
        if (hole_nr % game_mode) < game_mode-1:
            game[hole_nr] = game[hole_nr+1]
            game[hole_nr+1] = 99
            hole_nr += 1
            # ev = 'Right'
    elif event.keycode == 37: # Left
        if (hole_nr % game_mode) > 0:
            game[hole_nr] = game[hole_nr - 1]
            game[hole_nr - 1] = 99
            hole_nr -= 1
            # ev = 'Left'
    else:
        return
    mixer.music.play(loops=0, start=0.0, fade_ms = 0)
    reposition(labels, game)
    if game == win: # POBEDA
        lbl_last = tk.Label(width=600/game_mode, height=600/game_mode, image=pics[game_mode*game_mode-1])
        c = (game_mode*game_mode) % hole_nr + 1
        r = (game_mode*game_mode) // hole_nr + 1
        lbl_last.place(x = c * 600/game_mode + 4, y = r * 600/game_mode + 37)
        time.sleep(2)
        lbl_win = tk.Label()
        lbl_win.config(width=600, height=600, image=picture_game)
        lbl_win.place(x=5, y=35)
        for i in labels:
            i.destroy
        mixer.music.load('.\\Files\\L`Invitation au château.mp3')
        mixer.music.play()
def reposition(label_list, game_list):
    global hole_nr
    for i in range(game_mode*game_mode-1): #        Пробегаем список labels
        for j in range(game_mode*game_mode): #    Пробегаем список game
            if game_list[j] != 99: #   Только непустые фрагменты
                if i == game[j]: #  Если номер фрагмента (и label) совпадает с его позицией на игровом поле, то...
                    c = j % game_mode
                    r = j // game_mode
                    label_list[i].place(x = c * 600/game_mode + 4, y = r * 600/game_mode + 37)
                    break
    for i in range(game_mode*game_mode-1):
        if game[i] == 99:
            hole_nr = i
            break
def quit_game():
    exit()
def new_game():
    global game, hole, win, game_mode, labels, pics, hole_nr, picture_fn, game_picture
    try:
        mixer.music.stop()
    except:
        pass
    finally:
        mixer.init()
        mixer.music.load('.\\Files\\game_move.mp3')
    picture_fn = select_picture()
    pics = cut_picture(picture_fn)
    if len(labels) > 0:
        for i in labels:
            i.destroy()
        labels = []
    for i in range(game_mode * game_mode):
        label = tk.Label()
        label.config(text=str(i), width=600 / game_mode, height=600 / game_mode, relief=tk.RAISED, image=pics[i])
        labels.append(label)
    init_result = init_game()
    game = init_result[0]
    hole = init_result[1]
    win = init_result[2]
    reposition(labels, game)
def normal_game():
    global game_mode
    game_mode = 4
    new_game()
def easy_game():
    global game_mode
    game_mode = 3
    new_game()
if __name__ == '__main__':
    picture_win = None
    root = tk.Tk()
    game_mode = 3
    hole_nr = game_mode * game_mode -1
    labels = []
    game = []
    picture = None
    picture_game = None
    root.geometry('614x646')
    root.resizable(False, False)
    root.title('FIFTEEN-game')
    root.iconbitmap(default=".\\Files\\fifteen-game.ico")
    root.config()
    easy_game_btn = tk.Button(text='Easy game', width=33, command=easy_game)
    easy_game_btn.place(x=5, y=5)
    normal_game_btn = tk.Button(text='Normal game', width=33, command=normal_game)
    normal_game_btn.place(x=246, y=5)
    exit_btn = tk.Button(text='Exit', width=15, command=quit_game)
    exit_btn.place(x=492, y=5)
    easy_game()
    reposition(labels, game)
    root.bind("<Key>", my_key)
    root.mainloop()