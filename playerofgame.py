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
    head = Circle(65, 295, 12, fill="peachPuff")
    body = Rect(55, 307, 20, 28, fill="dodgerblue")

    weaponArm = Line(75, 315, 95, 315, lineWidth=4)
    otherArm = Line(55, 315, 45, 330, lineWidth=4)

    blaster = drawWristBlaster()

    leftUpperLeg = Line(60, 335, 56, 345, lineWidth=4)
    leftLowerLeg = Line(56, 345, 52, 355, lineWidth=4)

    rightUpperLeg = Line(70, 335, 74, 345, lineWidth=4)
    rightLowerLeg = Line(74, 345, 78, 355, lineWidth=4)

    leftEye = Circle(61, 292, 2, fill="black")
    rightEye = Circle(69, 292, 2, fill="black")

    player = Group(
        head,
        otherArm,
        weaponArm,
        blaster,
        body,
        leftUpperLeg,
        leftLowerLeg,
        rightUpperLeg,
        rightLowerLeg,
        leftEye,
        rightEye,
    )

    def getBulletStart():
        if player.facing == "right":
            return blaster.right + 5, blaster.centerY
        else:
            return blaster.left - 5, blaster.centerY

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

    def crouch():
        if player.isCrouching:
            return

        player.isCrouching = True

        head.centerY += 10
        leftEye.centerY += 10
        rightEye.centerY += 10
        body.centerY += 10

        weaponArm.y1 += 10
        weaponArm.y2 += 10

        otherArm.y1 += 10
        otherArm.y2 += 10

        blaster.centerY += 10

        leftUpperLeg.x1 = body.left + 5
        leftUpperLeg.y1 = body.bottom
        leftUpperLeg.x2 = body.left
        leftUpperLeg.y2 = body.bottom + 8

        leftLowerLeg.x1 = body.left
        leftLowerLeg.y1 = body.bottom + 8
        leftLowerLeg.x2 = body.left - 12
        leftLowerLeg.y2 = body.bottom + 8

        rightUpperLeg.x1 = body.right - 5
        rightUpperLeg.y1 = body.bottom
        rightUpperLeg.x2 = body.right + 5
        rightUpperLeg.y2 = body.bottom + 8

        rightLowerLeg.x1 = body.right + 5
        rightLowerLeg.y1 = body.bottom + 8
        rightLowerLeg.x2 = body.right + 18
        rightLowerLeg.y2 = body.bottom + 8

    def stand():
        if not player.isCrouching:
            return

        player.isCrouching = False

        head.centerY -= 10
        leftEye.centerY -= 10
        rightEye.centerY -= 10
        body.centerY -= 10

        weaponArm.y1 -= 10
        weaponArm.y2 -= 10

        otherArm.y1 -= 10
        otherArm.y2 -= 10

        blaster.centerY -= 10

        leftUpperLeg.x1 = body.left + 5
        leftUpperLeg.y1 = body.bottom
        leftUpperLeg.x2 = body.left + 1
        leftUpperLeg.y2 = body.bottom + 10

        leftLowerLeg.x1 = body.left + 1
        leftLowerLeg.y1 = body.bottom + 10
        leftLowerLeg.x2 = body.left - 3
        leftLowerLeg.y2 = body.bottom + 20

        rightUpperLeg.x1 = body.right - 5
        rightUpperLeg.y1 = body.bottom
        rightUpperLeg.x2 = body.right - 1
        rightUpperLeg.y2 = body.bottom + 10

        rightLowerLeg.x1 = body.right - 1
        rightLowerLeg.y1 = body.bottom + 10
        rightLowerLeg.x2 = body.right + 3
        rightLowerLeg.y2 = body.bottom + 20

    player.centerX = 50
    player.centerY = 710

    player.getBulletStart = getBulletStart
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
    player.isCrouching = False

    player.takeDamage = takeDamage
    player.faceLeft = faceLeft
    player.faceRight = faceRight
    player.updateTurnAnimation = updateTurnAnimation
    player.crouch = crouch
    player.stand = stand

    return player
