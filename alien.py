from cmu_graphics import *
import math


def createAlien(x, y, scale=1):
    if scale <= 0:
        raise ValueError("Scale must be greater than zero")

    dark = rgb(7, 12, 23)
    blue = rgb(15, 27, 46)
    highlight = rgb(34, 51, 72)
    bone = rgb(92, 112, 131) 
    teeth = rgb(188, 201, 207)

    alien = Group()

    # Long, curved tail.
    alien.add(
        Polygon(
            164,
            213,
            139,
            228,
            110,
            242,
            79,
            245,
            52,
            234,
            33,
            211,
            23,
            182,
            25,
            154,
            34,
            130,
            30,
            162,
            33,
            186,
            46,
            207,
            66,
            222,
            89,
            227,
            115,
            220,
            144,
            197,
            fill=dark,
            border=highlight,
        ),
        Polygon(34, 130, 19, 151, 25, 169, 36, 153, fill=blue, border=highlight),
    )

    # Raised bones along the tail.
    for tx, ty in [(53, 234), (77, 245), (103, 243), (126, 234), (145, 224)]:
        alien.add(Polygon(tx - 6, ty - 3, tx - 7, ty + 10, tx + 6, ty - 4, fill=bone))

    # Far leg and foot.
    alien.add(
        Polygon(
            178,
            209,
            194,
            219,
            181,
            252,
            196,
            274,
            190,
            290,
            178,
            289,
            180,
            274,
            159,
            254,
            fill=dark,
            border=highlight,
        ),
        Polygon(179, 285, 194, 286, 213, 300, 176, 300, fill=dark),
    )

    farLeg, farFoot = list(alien.children)[-2:]

    # Far arm.
    alien.add(
        Polygon(
            192,
            147,
            208,
            152,
            221,
            187,
            243,
            200,
            238,
            208,
            211,
            196,
            fill=dark,
            border=highlight,
        )
    )

    # Hunched body and neck.
    bodyAnchor = Oval(175, 178, 57, 94, fill=blue, rotateAngle=18)
    alien.add(
        bodyAnchor,
        Oval(169, 218, 43, 42, fill=dark),
        Polygon(
            176,
            148,
            174,
            113,
            195,
            104,
            210,
            117,
            197,
            157,
            fill=blue,
            border=highlight,
        ),
    )

    # Bony spines down the back.
    for sx, sy in [(168, 132), (158, 149), (151, 168), (148, 188), (149, 207)]:
        alien.add(
            Polygon(
                sx + 5,
                sy - 7,
                sx - 18,
                sy - 15,
                sx - 6,
                sy + 8,
                sx + 7,
                sy + 7,
                fill=bone,
                border=dark,
            )
        )

    # Rib-like armor.
    for ry in range(155, 204, 12):
        alien.add(
            Line(168, ry, 188, ry + 7, fill=highlight, lineWidth=5),
            Line(188, ry + 7, 199, ry + 2, fill=highlight, lineWidth=3),
        )

    # Near leg: bent backward at the knee.
    alien.add(
        Polygon(
            157,
            213,
            178,
            221,
            160,
            255,
            172,
            281,
            162,
            292,
            151,
            283,
            145,
            255,
            fill=blue,
            border=highlight,
        ),
        Oval(159, 238, 20, 35, fill=highlight, rotateAngle=22),
        Polygon(154, 282, 170, 282, 190, 299, 149, 299, fill=blue, border=highlight),
    )

    nearLeg, legHighlight, nearFoot = list(alien.children)[-3:]

    # Foot claws.
    footClaws = []
    for cx in (165, 176, 187):
        claw = Polygon(cx - 5, 294, cx, 303, cx + 9, 301, fill=teeth)
        alien.add(claw)
        footClaws.append(claw)

    # Near arm and hand.
    alien.add(
        Oval(197, 153, 26, 31, fill=blue, border=highlight),
        Polygon(
            195,
            154,
            208,
            155,
            213,
            190,
            236,
            213,
            230,
            223,
            201,
            201,
            fill=blue,
            border=highlight,
        ),
        Oval(234, 220, 22, 16, fill=blue, rotateAngle=30),
    )

    # Three hooked fingers.
    for offset in (0, 7, 14):
        alien.add(
            Polygon(
                233 + offset,
                217,
                242 + offset,
                226,
                239 + offset,
                238,
                236 + offset,
                228,
                229 + offset,
                222,
                fill=bone,
            )
        )

    # Long skull extending far behind the face.
    alien.add(
        Oval(150, 91, 164, 57, fill=dark, border=highlight, rotateAngle=-8),
        Oval(143, 79, 131, 20, fill=blue, rotateAngle=-8),
        Oval(130, 75, 83, 7, fill=highlight, rotateAngle=-8),
        Polygon(190, 81, 216, 82, 234, 98, 230, 115, 207, 122, 188, 110, fill=dark),
    )

    # Narrow eye and heavy brow.
    alien.add(
        Polygon(207, 97, 224, 99, 210, 103, fill=rgb(115, 210, 220)),
        Line(203, 94, 225, 97, fill=blue, lineWidth=5),
    )

    # Jaw and jagged teeth.
    alien.add(
        Polygon(
            199,
            110,
            232,
            108,
            228,
            125,
            211,
            132,
            197,
            124,
            fill=blue,
            border=highlight,
        ),
        Polygon(202, 113, 230, 111, 223, 124, 207, 124, fill="black"),
    )

    for tx in (206, 213, 220):
        alien.add(
            Polygon(tx, 113, tx + 5, 113, tx + 2, 120, fill=teeth),
            Polygon(tx, 124, tx + 4, 124, tx + 2, 119, fill=teeth),
        )

    alien.width *= scale
    alien.height *= scale
    alien.centerX = x
    alien.bottom = y

    alien.normalWidth = alien.width
    alien.direction = 1
    alien.facing = "right"
    alien.turning = False
    alien.turnStage = None
    alien.newDirection = 1
    alien.turnSpeed = alien.normalWidth / 8

    # Walking settings. Distances are scaled to match the alien.
    alien.walkPhase = 0
    alien.walkSpeed = 0.22
    alien.strideLength = 16 * scale
    alien.stepHeight = 10 * scale

    # Remember the original leg shapes relative to the body.
    # Keeping the hips still prevents the legs from coming detached.
    legPoses = []
    hipY = bodyAnchor.centerY + 47 * scale

    def rememberLegPart(shape, phaseOffset, isFoot=False):
        points = []
        for px, py in shape.pointList:
            weight = 1 if isFoot else max(0, min(1, (py - hipY) / (65 * scale)))
            points.append((px - bodyAnchor.centerX,
                           py - bodyAnchor.centerY, weight))
        legPoses.append((shape, phaseOffset, points))

    rememberLegPart(farLeg, math.pi)
    rememberLegPart(farFoot, math.pi, True)
    rememberLegPart(nearLeg, 0)
    rememberLegPart(nearFoot, 0, True)
    for claw in footClaws:
        rememberLegPart(claw, 0, True)

    highlightX = legHighlight.centerX - bodyAnchor.centerX
    highlightY = legHighlight.centerY - bodyAnchor.centerY
    highlightAngle = legHighlight.rotateAngle
    highlightWeight = max(0, min(1, (legHighlight.centerY - hipY) / (65 * scale)))

    def drawLegs(walking):
        oldX, oldBottom = alien.centerX, alien.bottom
        anchorX, anchorY = bodyAnchor.centerX, bodyAnchor.centerY
        facing = 1 if alien.facing == "right" else -1

        for shape, phaseOffset, originalPoints in legPoses:
            phase = alien.walkPhase + phaseOffset
            step = math.sin(phase) * alien.strideLength if walking else 0
            lift = max(0, math.cos(phase)) * alien.stepHeight if walking else 0
            shape.pointList = [
                [anchorX + facing * (px + step * weight),
                 anchorY + py - lift * weight]
                for px, py, weight in originalPoints
            ]

        # The armor on the near leg follows that leg too.
        step = math.sin(alien.walkPhase) * alien.strideLength if walking else 0
        lift = max(0, math.cos(alien.walkPhase)) * alien.stepHeight if walking else 0
        legHighlight.centerX = anchorX + facing * (highlightX + step * highlightWeight)
        legHighlight.centerY = anchorY + highlightY - lift * highlightWeight
        legHighlight.rotateAngle = facing * highlightAngle

        # Keep the alien at its current world position and ground level.
        alien.centerX = oldX
        alien.bottom = oldBottom

    def updateWalkAnimation(isWalking=True):
        if alien.turning:
            return
        if isWalking:
            alien.walkPhase = (alien.walkPhase + alien.walkSpeed) % (2 * math.pi)
        else:
            alien.walkPhase = 0
        drawLegs(isWalking)

    def mirror():
        axis = alien.centerX
        for shape in alien.children:
            if isinstance(shape, Polygon):
                shape.pointList = [
                    [2 * axis - px, py] for px, py in shape.pointList
                ]
            elif isinstance(shape, Line):
                x1, x2 = shape.x1, shape.x2
                shape.x1 = 2 * axis - x1
                shape.x2 = 2 * axis - x2
            else:
                shape.centerX = 2 * axis - shape.centerX
                shape.rotateAngle *= -1

    def startTurn(newDirection):
        if newDirection not in (-1, 1):
            raise ValueError("Direction must be -1 or 1")
        if alien.turning or newDirection == alien.direction:
            return

        # Put both feet down before squeezing the drawing to turn.
        updateWalkAnimation(False)
        alien.turning = True
        alien.turnStage = "shrinking"
        alien.newDirection = newDirection

    def updateTurnAnimation():
        if not alien.turning:
            return

        oldX, oldBottom = alien.centerX, alien.bottom
        minimumWidth = alien.normalWidth * 0.15

        if alien.turnStage == "shrinking":
            alien.width = max(minimumWidth, alien.width - alien.turnSpeed)
            if alien.width <= minimumWidth:
                mirror()
                alien.direction = alien.newDirection
                alien.facing = "right" if alien.direction == 1 else "left"
                alien.turnStage = "expanding"

        elif alien.turnStage == "expanding":
            alien.width = min(alien.normalWidth, alien.width + alien.turnSpeed)
            if alien.width >= alien.normalWidth:
                alien.turning = False
                alien.turnStage = None

        alien.centerX = oldX
        alien.bottom = oldBottom

    alien.startTurn = startTurn
    alien.updateTurnAnimation = updateTurnAnimation
    alien.updateWalkAnimation = updateWalkAnimation

    return alien


# x is the horizontal center; y is where its feet touch.
