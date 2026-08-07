import cmu_graphics
from cmu_graphics import *
from item import powerBoost

#  chest will have either 8 sec extra speed


def drawTreasureChest(x, y):
    chest = Group(
        # Lid
        Polygon(
            x + 5,
            y + 20,
            x + 15,
            y + 5,
            x + 45,
            y + 5,
            x + 55,
            y + 20,
            fill=rgb(130, 75, 35),
            border="black",
        ),
        # Main body
        Rect(x + 5, y + 20, 50, 30, fill=rgb(105, 60, 30), border="black"),
        # Gold bands
        Rect(x + 10, y + 20, 6, 30, fill="gold", border="black"),
        Rect(x + 44, y + 20, 6, 30, fill="gold", border="black"),
        # Gold trim on lid
        Line(x + 8, y + 20, x + 52, y + 20, fill="gold", lineWidth=4),
        # Lock plate
        Rect(x + 25, y + 28, 10, 14, fill="gold", border="black"),
        # Keyhole
        Circle(x + 30, y + 34, 2, fill="black"),
        Rect(x + 29, y + 34, 2, 5, fill="black"),
        # Wood plank lines
        Line(x + 5, y + 35, x + 55, y + 35, fill=rgb(70, 35, 20)),
        Line(x + 20, y + 20, x + 20, y + 50, fill=rgb(70, 35, 20)),
        Line(x + 40, y + 20, x + 40, y + 50, fill=rgb(70, 35, 20)),
    )

    return chest


class Chest:
    def __init__(self, x, y, item):
        self.shape = drawTreasureChest(x, y)
        self.opened = False
        self.item = item

    def open(self):
        self.opened = True
        self.shape.visible = False


def createChests():
    chests = [Chest(120, 220, powerBoost)]
    return chests
