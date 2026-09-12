import cmu_graphics
import math
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

    def getBounds():
        # Keep the gun and changing leg width out of platform collision
        return body.left - 2, head.top, body.right + 2, player.bottom

    def attachBlaster():
        # wrist is 4.5 pixels behind the blaster's centre in its original pose.
        angle = math.radians(blaster.rotateAngle)
        blaster.centerX = weaponArm.x2 + 4.5 * math.cos(angle)
        blaster.centerY = weaponArm.y2 + 4.5 * math.sin(angle)

    def takeDamage(damage, healthBar, restart):
        if player.damageCooldown > 0:
            return
        player.damageCooldown = app.stepsPerSecond
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
        attachBlaster()

        if player.isCrouching:
            updateCrouchLegs()

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
        attachBlaster()

        if player.isCrouching:
            updateCrouchLegs()

    def updateTurnAnimation():
        if player.turnTarget == 180:
            if blaster.rotateAngle < 180:
                blaster.rotateAngle += 5

        elif player.turnTarget == 0:
            if blaster.rotateAngle > 0:
                blaster.rotateAngle -= 5

        attachBlaster()

    def updateCrouchLegs():
        direction = 1 if player.facing == "right" else -1
        x = body.centerX

        # Rear knee down, front foot planted; mirror the pose when turning.
        leftUpperLeg.x1 = x - direction * 5
        leftUpperLeg.y1 = body.bottom
        leftUpperLeg.x2 = x - direction * 12
        leftUpperLeg.y2 = body.bottom + 6

        leftLowerLeg.x1 = x - direction * 12
        leftLowerLeg.y1 = body.bottom + 6
        leftLowerLeg.x2 = x - direction * 23
        leftLowerLeg.y2 = body.bottom + 6

        rightUpperLeg.x1 = x + direction * 5
        rightUpperLeg.y1 = body.bottom
        rightUpperLeg.x2 = x + direction * 18
        rightUpperLeg.y2 = body.bottom - 6

        rightLowerLeg.x1 = x + direction * 18
        rightLowerLeg.y1 = body.bottom - 6
        rightLowerLeg.x2 = x + direction * 18
        rightLowerLeg.y2 = body.bottom + 6

    def crouch():
        if player.isCrouching:
            return

        oldBottom = player.bottom
        player.isCrouching = True

        head.centerY += 14
        leftEye.centerY += 14
        rightEye.centerY += 14
        body.centerY += 14

        weaponArm.y1 += 14
        weaponArm.y2 += 14

        otherArm.y1 += 14
        otherArm.y2 += 14

        blaster.centerY += 14

        updateCrouchLegs()
        player.bottom = oldBottom

    def stand():
        if not player.isCrouching:
            return

        oldBottom = player.bottom
        player.isCrouching = False

        head.centerY -= 14
        leftEye.centerY -= 14
        rightEye.centerY -= 14
        body.centerY -= 14

        weaponArm.y1 -= 14
        weaponArm.y2 -= 14

        otherArm.y1 -= 14
        otherArm.y2 -= 14

        blaster.centerY -= 14

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

        player.bottom = oldBottom

    player.centerX = 50
    player.centerY = 710

    player.getBounds = getBounds
    player.getBulletStart = getBulletStart
    player.speed = 30
    player.boostSpeed = 50
    player.normSpeed = player.speed
    player.dy = 0
    player.jumpPower = -13
    player.normJumpPower = player.jumpPower
    player.onGround = False
    player.jumpBoostPower = -65

    player.damageCooldown = 0
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
