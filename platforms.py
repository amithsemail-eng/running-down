import cmu_graphics
from cmu_graphics import *


def createPlatforms():
    platforms = [
        Rect(0, 780, 260, 20, fill="crimson"),
        Rect(220, 700, 240, 20, fill="gold"),
        Rect(500, 620, 220, 20, fill="limeGreen"),
        Rect(280, 535, 200, 20, fill="red"),
        Rect(40, 450, 190, 20, fill="dodgerBlue"),
        Rect(300, 365, 180, 20, fill="purple"),
        Rect(560, 280, 170, 20, fill="orangeRed"),
        Rect(350, 195, 160, 20, fill="deepSkyBlue"),
        Rect(90, 110, 150, 20, fill="hotPink"),
        Rect(380, 30, 140, 20, fill="saddleBrown"),
    ]
    return platforms
