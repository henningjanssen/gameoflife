import tkinter as Tk

class Cell:
    def __init__(self, parent, x, y, width, height):
        self.alive = False
        self.alivetomorrow = False
        self.x = x
        self.y = y
        self.button = Tk.Button(
            parent, width=width, height=height, bg='white', bd=0,
            command=self.click, relief=Tk.FLAT)
        self.button.place(x=x*width, y=y*height)

    def click(self):
        self.alive = not self.alive
        self.alivetomorrow = self.alive
        self.updateColor(self.alive)

    def updateColor(self, alive):
        if alive:
            self.button.config(bg = '#15681d')
        else:
            self.button.config(bg = 'white')

    def update(self):
        if self.alive != self.alivetomorrow:
            self.updateColor(self.alivetomorrow)
        self.alive = self.alivetomorrow
