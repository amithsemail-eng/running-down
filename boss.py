from cmu_graphics import *
import math


# x is the horizontal center; y is where its feet touch.
def createBoss(x, y, scale=1):
    skin = rgb(118, 116, 58)
    skinDark = rgb(66, 68, 32)
    skinLight = rgb(165, 158, 95)
    headColor = rgb(38, 26, 38)
    armor = rgb(98, 90, 115)
    metal = rgb(52, 52, 46)
    metalLight = rgb(115, 112, 95)

    boss = Group()

    # Invisible hitbox: how close the player can get.
    hitbox = Rect(75, 100, 180, 190, fill=None)
    boss.add(hitbox)

    # Shadow on the ground.
    boss.add(Oval(165, 296, 230, 14, fill="black", opacity=30))

    # Legs: long armor plates. Each leg is its own Group so it can step.
    legs = []
    for lx in (145, 185):
        leg = Group(
            Polygon(
                lx - 14,
                195,
                lx + 14,
                195,
                lx + 18,
                250,
                lx + 10,
                292,
                lx - 8,
                296,
                lx - 16,
                250,
                fill=armor,
                border=metal,
            ),
            Line(lx, 205, lx + 2, 285, fill=metal, lineWidth=2),
            Polygon(lx - 10, 290, lx + 12, 290, lx + 20, 298, lx - 12, 298, fill=metal),
        )
        boss.add(leg)
        legs.append(leg)

    # Back arm, holding the minigun.
    boss.add(
        Oval(108, 140, 30, 30, fill=skin, border=skinDark),
        Polygon(96, 135, 120, 140, 112, 200, 94, 198, fill=skin, border=skinDark),
        Polygon(94, 196, 112, 198, 106, 245, 90, 242, fill=skin, border=skinDark),
    )
    boss.add(
        Rect(70, 150, 32, 120, fill=metal, border=metalLight),
        Line(86, 155, 86, 265, fill=metalLight, lineWidth=2),
        Rect(66, 190, 40, 8, fill=metalLight),
        Rect(66, 225, 40, 8, fill=metalLight),
        Rect(66, 258, 40, 8, fill=metalLight),
    )
    for bx in (75, 86, 97):
        boss.add(
            Line(bx, 270, bx, 284, fill=metal, lineWidth=5),
            Oval(bx, 286, 8, 8, fill=metalLight, border=metal),
        )

    # Tall, glossy egg-shaped head (drawn first so the shoulders cover its bottom).
    boss.add(
        Oval(165, 82, 58, 96, fill=headColor, border=skinDark, borderWidth=3),
        Oval(177, 62, 14, 30, fill=rgb(215, 180, 205), opacity=55),
    )

    # Big muscly torso that narrows to a thin waist.
    body = Oval(165, 165, 50, 70, fill=skin)
    boss.add(
        Polygon(
            98,
            118,
            130,
            100,
            145,
            115,
            165,
            128,
            185,
            115,
            200,
            100,
            232,
            118,
            218,
            155,
            185,
            205,
            145,
            205,
            112,
            155,
            fill=skin,
            border=skinDark,
        ),
        Oval(112, 118, 40, 34, fill=skinLight, border=skinDark),
        Oval(218, 118, 40, 34, fill=skinLight, border=skinDark),
        Oval(148, 138, 34, 22, fill=skinLight, border=skinDark),
        Oval(182, 138, 34, 22, fill=skinLight, border=skinDark),
        body,
        Line(165, 135, 165, 198, fill=skinDark, lineWidth=2),
    )
    for ay in (158, 172, 186):
        boss.add(Line(152, ay, 178, ay, fill=skinDark, lineWidth=2))

    # Straps hanging from the waist.
    boss.add(
        Line(142, 190, 134, 238, fill=metal, lineWidth=2),
        Line(188, 190, 196, 238, fill=metal, lineWidth=2),
    )

    # Front arm with a clawed hand: this is the attack arm.
    shoulder = Oval(222, 145, 30, 30, fill=skin, border=skinDark)
    armParts = [
        Polygon(212, 138, 236, 140, 250, 200, 232, 204, fill=skin, border=skinDark),
        Polygon(232, 200, 250, 198, 262, 248, 246, 252, fill=skin, border=skinDark),
        Polygon(
            244, 248, 264, 246, 272, 262, 260, 272, 248, 266, fill=skin, border=skinDark
        ),
        Polygon(248, 264, 254, 266, 248, 284, fill=skinLight),
        Polygon(256, 268, 262, 268, 258, 288, fill=skinLight),
        Polygon(264, 264, 270, 262, 270, 282, fill=skinLight),
    ]
    boss.add(shoulder, *armParts)

    boss.width *= scale
    boss.height *= scale
    boss.centerX = x
    boss.bottom = y

    boss.direction = 1
    boss.facing = "right"
    boss.walkPhase = 0

    # Remember where things are, measured from the body's center.
    legSpots = [
        (leg.centerX - body.centerX, leg.centerY - body.centerY) for leg in legs
    ]
    sx, sy = shoulder.centerX - body.centerX, shoulder.centerY - body.centerY
    armPoints = []
    for part in armParts:
        armPoints.append(
            [(px - body.centerX, py - body.centerY) for px, py in part.pointList]
        )

    def updateWalkAnimation(isWalking=True):
        if isWalking:
            boss.walkPhase += 0.25
        else:
            boss.walkPhase = 0
        facing = boss.direction
        for i in range(len(legs)):
            phase = boss.walkPhase + i * math.pi
            step = math.sin(phase) * 10 * scale if isWalking else 0
            lift = max(0, math.cos(phase)) * 8 * scale if isWalking else 0
            legX, legY = legSpots[i]
            legs[i].centerX = body.centerX + facing * (legX + step)
            legs[i].centerY = body.centerY + legY - lift

    def mirror(group):
        axis = body.centerX
        for shape in group.children:
            if isinstance(shape, Group):
                mirror(shape)
            elif isinstance(shape, Polygon):
                shape.pointList = [[2 * axis - px, py] for px, py in shape.pointList]
            elif isinstance(shape, Line):
                shape.x1, shape.x2 = 2 * axis - shape.x1, 2 * axis - shape.x2
            else:
                shape.centerX = 2 * axis - shape.centerX

    def startTurn(newDirection):
        if newDirection == boss.direction:
            return
        updateWalkAnimation(False)
        bottom = boss.bottom
        mirror(boss)
        boss.direction = newDirection
        boss.facing = "right" if newDirection == 1 else "left"
        boss.bottom = bottom

    def setArmAngle(angle):
        # 0 = resting; negative = raised back; positive = swung forward
        cos, sin = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        for part, points in zip(armParts, armPoints):
            newPoints = []
            for px, py in points:
                dx, dy = px - sx, py - sy
                newX = sx + dx * cos - dy * sin
                newY = sy + dx * sin + dy * cos
                newPoints.append(
                    [body.centerX + boss.direction * newX, body.centerY + newY]
                )
            part.pointList = newPoints

    def getShoulder():
        return shoulder.centerX, shoulder.centerY

    def getBounds():
        return hitbox.left, boss.top, hitbox.right, boss.bottom

    boss.armReach = max(
        math.dist((px, py), (sx, sy)) for points in armPoints for px, py in points
    )
    boss.updateWalkAnimation = updateWalkAnimation
    boss.startTurn = startTurn
    boss.setArmAngle = setArmAngle
    boss.getShoulder = getShoulder
    boss.getBounds = getBounds
    return boss
