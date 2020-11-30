import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

pygame.init()


def setup(win):
    win.fill((0, 0, 0))
    pygame.draw.line(win, (255, 255, 255), (200, 0), (200, 600))
    pygame.draw.line(win, (255, 255, 255), (0, 200), (600, 200))
    pygame.draw.line(win, (255, 255, 255), (400, 0), (400, 600))
    pygame.draw.line(win, (255, 255, 255), (0, 400), (600, 400))
    pygame.display.update()


def insertShape(win, shape, pos_x, pos_y):

    m = pos_y*200 + 100
    n = pos_x*200 + 100

    if (shape == "o"):
        pygame.draw.circle(win, (230, 50, 100), (n, m), 80, 2)
        pygame.display.update()

    elif (shape == "x"):
        pygame.draw.line(win, (230, 50, 100), (m-65, n-65), (m+65, n+65), 2)
        pygame.draw.line(win, (230, 50, 100), (m+65, n-65), (m-65, n+65), 2)
        pygame.display.update()


def checkWin(b):

    for i in range(3):
        if b[i][0] == b[i][1] and b[i][1] == b[i][2]:
            if b[i][0] == "x":
                return +10
            elif b[i][0] == "o":
                return -10

    for i in range(3):
        if b[0][i] == b[1][i] and b[1][i] == b[2][i]:
            if b[0][i] == "x":
                return +10
            elif b[0][i] == "o":
                return -10

    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:
        if b[0][0] == "x":
            return +10
        elif b[0][0] == "o":
            return -10

    if b[0][2] == b[1][1] and b[1][1] == b[2][0]:
        if b[0][2] == "x":
            return +10
        elif b[0][2] == "o":
            return -10

    return 0


def isMovesLeft(b):

    for i in range(3):
        for j in range(3):
            if b[i][j] == 0:
                return True

    return False


def minimax(state, depth, isMaximiser, alpha, beta):

    result = checkWin(state)

    if (result == 10 or result == -10):
        return result

    if (isMovesLeft(state) == False):
        return 0

    if (isMaximiser == True):

        bestScore = -100

        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    state[i][j] = "x"
                    score = minimax(state, depth+1, False,
                                    alpha, beta) - 0.5*depth
                    state[i][j] = 0
                    bestScore = max(bestScore, score)
                    alpha = max(alpha, bestScore)
                    if beta <= alpha:
                        break

        return bestScore

    else:

        bestScore = 100

        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    state[i][j] = "o"
                    score = minimax(state, depth+1, True,
                                    alpha, beta) + 0.5*depth
                    state[i][j] = 0
                    bestScore = min(bestScore, score)
                    beta = min(beta, bestScore)
                    if beta <= alpha:
                        break

        return bestScore


def compMove(win, b):

    bestScore = -100

    best_x = 0
    best_y = 0

    for i in range(3):
        for j in range(3):
            if b[i][j] == 0:
                b[i][j] = "x"
                score = minimax(b, 0, False, -1000, 1000)
                b[i][j] = 0

                if score > bestScore:
                    bestScore = score
                    best_x = i
                    best_y = j

    b[best_x][best_y] = "x"
    insertShape(win, "x", best_x, best_y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()

    messagebox.showinfo(subject, content)

    try:
        root.destroy()
    except:
        pass


def main():

    win = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    flag = True

    state = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    comp_move = True

    setup(win)

    while flag:

        pygame.time.delay(50)
        clock.tick(10)

        if comp_move == True:
            comp_move = False
            compMove(win, state)

        else:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    x = x // 200
                    y = y // 200

                    if (state[y][x] == 0):
                        state[y][x] = 'o'

                        insertShape(win, "o", x, y)

                        comp_move = True

        result = checkWin(state)

        if (result == 10 or result == -10 or isMovesLeft(state) == False):

            if result == 10:
                message_box("X won!", "Play again ...")
            elif result == -10:
                message_box("O won!", "Play again ...")
            elif result == 0:
                message_box("Draw!", "Play again ...")

            state = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]

            comp_move = True

            setup(win)


main()
