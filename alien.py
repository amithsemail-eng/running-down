from cmu_graphics import *


def createAlien(x, y, scale=1):
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
    alien.add(
        Oval(175, 178, 57, 94, fill=blue, rotateAngle=18),
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

    # Foot claws.
    for cx in (165, 176, 187):
        alien.add(Polygon(cx - 5, 294, cx, 303, cx + 9, 301, fill=teeth))

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

    return alien


# x is the horizontal center; y is where its feet touch.
