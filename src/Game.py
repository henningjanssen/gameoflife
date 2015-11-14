import tkinter as Tk
import os
from Cell import *
from threading import Thread
import time

class Game(Thread):
    run = True
    def __init__(self, width, height, cellwidth, cellheight):
        self.width = width
        self.height = height
        self.running = False
        self.stayAlive = True
        super(Game, self).__init__()

        dir = os.path.dirname(__file__)
        self.tk = Tk.Tk()
        self.tk.geometry(str(width*cellwidth)+"x"+str(height*cellheight))
        self.tk.title("Game of Life")

        menubar = Tk.Menu()
        menubar.add_command(label="Start", command=self.startGame)
        menubar.add_command(label="Stop", command=self.stopGame)
        self.tk.config(menu=menubar)

        self.cells = []

        for i in range(0, height):
            self.cells.append([])
            for j in range(0, width):
                self.cells[i].append(Cell(self.tk, i, j, cellwidth, cellheight))

    def mainloop(self):
        self.start()
        self.tk.mainloop()
        self.stopGame()
        self.stayAlive = False
        self.join()

    def run(self):
        self.stayAlive = True
        while self.stayAlive:
            if not self.running:
                time.sleep(0.1)
                continue
            livingCells = [(cell.x, cell.y) for row in self.cells
                for cell in row if cell.alive]

            toCheck = []
            for (x, y) in livingCells:
                if(x,y) not in toCheck:
                    toCheck.append((x,y))

                for (a,b) in self.getNeighbours(x,y):
                    if (a,b) not in toCheck:
                        toCheck.append((a,b))

            for (x, y) in toCheck:
                livingNeighbours = self.getLivingNeighbourCount(x, y)

                if livingNeighbours > 3 or livingNeighbours < 2:
                    self.cells[x][y].alivetomorrow = False
                elif livingNeighbours == 3:
                    self.cells[x][y].alivetomorrow = True

            for (x,y) in toCheck:
                self.cells[x][y].update()

            time.sleep(0.3)

    def getLivingNeighbourCount(self, x, y):
        neighbours = self.getNeighbours(x, y)
        count = 0

        for (a,b) in neighbours:
            if self.cells[a][b].alive:
                count += 1
        return count

    def getNeighbours(self, x, y):
        neighbours = [(x-1, y-1), (x-1, y), (x-1, y+1),
            (x, y-1), (x, y+1),
            (x+1, y-1), (x+1, y), (x+1, y+1)]

        neighbours = [(a,b) for (a,b) in neighbours
            if a >= 0 and b >= 0 and a < self.width and b < self.height]

        return neighbours

    def startGame(self):
        self.running = True

    def stopGame(self):
        self.running = False
