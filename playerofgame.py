import cmu_graphics
from cmu_graphics import *


def drawWristBlaster():
    return Group(
        Polygon(
            84, 310, 96, 310, 102, 315, 96, 320, 84, 320, fill="gray", border="black"
        ),
        Rect(94, 311, 16, 8, fill="darkGray", border="black"),
        Rect(96, 313, 13, 3, fill="lightGray"),
        Circle(90, 315, 3, fill="cyan", border="black"),
        Circle(110, 315, 5, fill="darkGray", border="black"),
        Circle(110, 315, 3, fill="cyan"),
        Circle(110, 315, 1, fill="white"),
    )


def createPlayer():
    body = Rect(55, 307, 20, 28, fill="dodgerblue")

    weaponArm = Line(75, 315, 95, 315, lineWidth=4)

    otherArm = Line(55, 315, 45, 330, lineWidth=4)

    blaster = drawWristBlaster()

    player = Group(
        Circle(65, 295, 12, fill="peachPuff"),
        otherArm,
        weaponArm,
        blaster,
        body,
        Line(60, 335, 52, 355, lineWidth=4),
        Line(70, 335, 78, 355, lineWidth=4),
        Circle(61, 292, 2, fill="black"),
        Circle(69, 292, 2, fill="black"),
    )

    def takeDamage(damage, healthBar, restart):
        if player.health - damage < 0:
            player.health = 0
        else:
            player.health -= damage

        healthBar.update(restart)

    def faceLeft():
        if player.facing == "left":
            return

        player.facing = "left"

        weaponArm.x1 = body.left
        weaponArm.y1 = body.top + 8
        weaponArm.x2 = body.left - 20
        weaponArm.y2 = body.top + 8

        otherArm.x1 = body.right
        otherArm.y1 = body.top + 8
        otherArm.x2 = body.right + 10
        otherArm.y2 = body.top + 23

        blaster.centerX = body.left - 25
        blaster.centerY = body.top + 8

        blaster.rotateAngle = 165
        player.turnTarget = 180

    def faceRight():
        if player.facing == "right":
            return

        player.facing = "right"

        weaponArm.x1 = body.right
        weaponArm.y1 = body.top + 8
        weaponArm.x2 = body.right + 20
        weaponArm.y2 = body.top + 8

        otherArm.x1 = body.left
        otherArm.y1 = body.top + 8
        otherArm.x2 = body.left - 10
        otherArm.y2 = body.top + 23

        blaster.centerX = body.right + 25
        blaster.centerY = body.top + 8

        blaster.rotateAngle = 15
        player.turnTarget = 0

    def updateTurnAnimation():
        if player.turnTarget == 180:
            if blaster.rotateAngle < 180:
                blaster.rotateAngle += 5

        elif player.turnTarget == 0:
            if blaster.rotateAngle > 0:
                blaster.rotateAngle -= 5

    player.centerX = 50
    player.centerY = 710

    player.speed = 30
    player.boostSpeed = 50
    player.normSpeed = player.speed
    player.dy = 0
    player.jumpPower = -13
    player.onGround = False
    player.jumpBoostPower = -65

    player.health = 100
    player.maxHealth = 100

    player.facing = "right"
    player.turnTarget = 0

    player.takeDamage = takeDamage
    player.faceLeft = faceLeft
    player.faceRight = faceRight
    player.updateTurnAnimation = updateTurnAnimation

    return player
