import cmu_graphics
from cmu_graphics import *


def createPlayer():
    player = Group(
        Circle(65, 295, 12, fill="peachPuff"),
        Rect(55, 307, 20, 28, fill="dodgerblue"),
        Line(55, 315, 45, 330, lineWidth=4),
        Line(75, 315, 85, 330, lineWidth=4),
        Line(60, 335, 52, 355, lineWidth=4),
        Line(70, 335, 78, 355, lineWidth=4),
        Circle(61, 292, 2, fill="black"),
        Circle(69, 292, 2, fill="black"),
    )
    player.centerX = 50
    player.centerY = 710
    player.speed = 30
    player.boostSpeed = 50
    player.normSpeed = player.speed
    player.dy = 0
    player.jumpPower = -13
    player.onGround = False
    player.jumpBoostPower = -65
    return player


# 100 hp if hit spike - 20 hp if hit ax -25 hp and pushback
