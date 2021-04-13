# -*- coding: utf-8 -*-
# author : MEYNIEL


import tkinter as tk
import numpy as np

"""Ce programme consiste à creer un labyrinthe aléatoire, avec pour contraintes
que toutes les zones soient accessibles et donc reliées entre elles.
la fonction is_finished() verifie que cette propriété soit respectée.
le depart et l'arrivée se situent au coin superieur gauche et au coin inferieur 
droit.
la fonction make_it_complex() supprime aleatoirement des murs afin de donner
plusieurs solutions au labyrinthe, sans cette focntion il est composé de deux
situés de part et d'autre du chemin solveur.

L'algorithme de resolution part du depart et cartographie toutes les zones en
notant leur distance par rapport à l'arrivée.
ensuite l'algorithme se place au depart et se contente de parcourir le 
labyrinthe en suivant les chiffres de plus en plus petits, jusqu'a atteindre 
l'arrivée, il trouve donc le chemin le plus court pour aller du depart à 
l'arrivée

D'autre part avec quelques modifications ce script peut etre utilisé comme un
GPS pour trouver le chemin le plus rapide d'un point A à un point B.
"""


def start_application():
    # few variables
    mazeSize = 20  # number of rows and columns
    slotSize = 10  # in pixels

    # create window
    wnd = tk.Tk()
    wnd.title('Maze')

    # create canvas
    cnv = tk.Canvas(wnd, width=slotSize * (mazeSize + 2),
                    height=slotSize * (mazeSize + 2))
    cnv.pack()
    # create a button to solve the maze
    buttonSolve = tk.Button(wnd, text="solve this maze",
                            command=lambda: solve(cnv, maze, mazeSize,
                                                  slotSize))
    buttonSolve.pack()

    if mazeSize % 2 == 0:
        mazeSize += 1  # a maze may have an impair size

    # generate and draw the maze
    maze = create_maze(mazeSize)
    maze = make_it_complex(maze, mazeSize)
    maze = maze.tolist()
    print(maze)
    show_maze(cnv, maze, mazeSize, slotSize)

    wnd.mainloop()


def is_finished(maze, mazeSize):
    # check if all the slots are available from the starting point
    for i in range(1, mazeSize - 1, 2):
        for j in range(1, mazeSize - 1, 2):
            if maze[i][j] != maze[1][1]:
                return False
    return True

def create_maze(mazeSize):
    # create a grid
    # the only solution i've found to dodge an error array out of bounds
    maze = np.zeros((mazeSize, mazeSize + 1))
    for i in range(0, mazeSize):
        for j in range(0, mazeSize, 2):
            maze[i][j] = -1
            maze[j][i] = -1

    # give a different number to every slot of the grid
    numSlot = 0
    for i in range(mazeSize):
        for j in range(mazeSize):
            if maze[i][j] == 0:
                numSlot += 1
                maze[i][j] = numSlot

    # create an enter and an exit
    maze[1][0] = 1
    maze[mazeSize - 2][mazeSize - 1] = numSlot

    # connect all the slots
    while not is_finished(maze, mazeSize):
        x = np.random.randint(1, mazeSize - 1)
        if x % 2 == 0:
            # y = impair number between 1 and mazeSize - 1
            y = int(
                (np.random.randint(1, 32768) % ((mazeSize - 1) / 2)) * 2 + 1)
        else:
            # y = pair number between 1 and mazeSize - 1
            y = int(
                (np.random.randint(1, 32768) % ((mazeSize - 1) / 2)) * 2 + 2)

        # define two slots
        if maze[x - 1][y] == -1:
            slot_1 = maze[x][y - 1]
            slot_2 = maze[x][y + 1]
        else:
            slot_1 = maze[x - 1][y]
            slot_2 = maze[x + 1][y]

        # if the slots are different, break the wall to create an area composed
        # of 0 and slot_1 number
        if slot_1 != slot_2:
            maze[x][y] = 0
            for i in range(1, mazeSize - 1, 2):
                for j in range(1, mazeSize - 1, 2):
                    if maze[i][j] == slot_2:
                        maze[i][j] = slot_1
    # all the area are available from the starting point
    return maze


def make_it_complex(maze, mazeSize):
    # destroy few walls to create different solutions
    for i in range(mazeSize):
        x = np.random.randint(1, mazeSize - 1)
        if x % 2 == 0:
            y = int(
                (np.random.randint(1, 32768) % ((mazeSize - 1) / 2)) * 2 + 1)
        else:
            y = int(
                (np.random.randint(1, 32768) % ((mazeSize - 1) / 2)) * 2 + 2)
        maze[x][y] = 0

    # correct the maze by recreating a wall and transform all the non-wall
    # slots in 0
    maze[1][0] = 0
    for i in range(mazeSize - 2):
        maze[i][mazeSize - 1] = -1
    for i in range(1, mazeSize - 1):
        for j in range(1, mazeSize - 1):
            if maze[i][j] >= 0:
                maze[i][j] = 0
    return maze


def show_maze(cnv, maze, mazeSize, slotSize):
    # draw a black rectangle for every -1 in maze (the walls)
    for i in range(mazeSize):
        for j in range(mazeSize):
            if maze[i][j] == -1:
                cnv.create_rectangle((j + 1) * slotSize, (i + 1) * slotSize,
                                     (j + 2) * slotSize, (i + 2) * slotSize,
                                     fill="black")


def step(numberOfStep, mazeSize, temp, maze):
    for i in range(mazeSize - 1, 0, -1):
        for j in range(mazeSize - 1, 0, -1):
            if temp[i][j] == numberOfStep:
                if i > 0 and temp[i - 1][j] == 0 and maze[i - 1][j] == 0:
                    temp[i - 1][j] = numberOfStep + 1
                if j > 0 and temp[i][j - 1] == 0 and maze[i][j - 1] == 0:
                    temp[i][j - 1] = numberOfStep + 1
                if i < mazeSize - 1 and temp[i + 1][j] == 0 and \
                        maze[i + 1][
                            j] == 0:
                    temp[i + 1][j] = numberOfStep + 1
                if j < mazeSize - 1 and temp[i][j + 1] == 0 and \
                        maze[i][j + 1] == 0:
                    temp[i][j + 1] = numberOfStep + 1


def score_slots(maze, mazeSize):
    # number the boxes according to their distance from the finish line
    temp = np.zeros((mazeSize, mazeSize))

    # start at the exit of the labyrinth
    temp[mazeSize - 2][mazeSize - 1] = 1
    numberOfStep = 0
    while temp[1][0] == 0:
        numberOfStep += 1
        step(numberOfStep, mazeSize, temp, maze)
    maxDistance = np.max(temp)
    # create impossible places (walls and areas even further away than the exit)
    for i in range(mazeSize):
        for j in range(mazeSize):
            if temp[i][j] == 0:
                temp[i][j] = maxDistance + 10
    return temp, maxDistance


def solve(cnv, maze, mazeSize, slotSize):
    temp, maxDistance = score_slots(maze, mazeSize)
    # create the first rectangle of the path
    x = 1
    y = 1
    cnv.create_rectangle((y + 1) * slotSize, (x + 1) * slotSize,
                         (y + 2) * slotSize, (x + 2) * slotSize,
                         fill='green', width=0)

    while x != mazeSize - 2 or y != mazeSize - 2:
        # define the directions
        up = temp[x][y - 1]
        down = temp[x][y + 1]
        left = temp[x - 1][y]
        right = temp[x + 1][y]

        # follow the smallest score distance
        if up <= down and up <= left and up <= right:
            y = y - 1
        elif down <= up and down <= left and down <= right:
            y = y + 1
        elif left <= up and left <= down and left <= right:
            x = x - 1
        elif right <= up and right <= down and right <= left:
            x = x + 1
        # create the next path rectangle
        cnv.create_rectangle((y + 1) * slotSize, (x + 1) * slotSize,
                             (y + 2) * slotSize, (x + 2) * slotSize,
                             fill='green', width=0)

    # create the entry and exit rectangles of the maze
    cnv.create_rectangle(slotSize, slotSize * 2, slotSize * 2, slotSize * 3,
                         fill='green', width=0)
    cnv.create_rectangle(mazeSize * slotSize, (mazeSize - 1) * slotSize,
                         (mazeSize + 1) * slotSize + 1,
                         mazeSize * slotSize, fill='green', width=0)


start_application()
