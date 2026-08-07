import cmu_graphics
from cmu_graphics import *


def createPlatforms():
    # left top width height
    platforms = [
        Rect(0, 780, 100, 30, fill="crimson"),
        Rect(100, 300, 120, 20, fill="gold"),
        Rect(320, 240, 120, 20, fill="limegreen"),
        Rect(4, 180, 90, 20, fill="red"),
        Rect(18, 180, 90, 20, fill="dodgerBlue"),
        Rect(40, 20, 90, 20, fill="purple"),
        Rect(480, 180, 90, 20, fill="orangeRed"),
        Rect(200, 180, 90, 20, fill="deepSkyBlue"),
        Rect(480, 20, 90, 20, fill="hotPink"),
        Rect(410, 180, 90, 20, fill="saddleBrown"),
        Rect(280, 180, 90, 20, fill="lavender"),
        Rect(80, 20, 90, 20, fill="forestGreen"),
        Rect(10, 180, 50, 80, fill="tomato"),
        Rect(380, 180, 90, 20, fill="navy"),
        Rect(480, 20, 90, 20, fill="peachPuff"),
    ]
    return platforms
