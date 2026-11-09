from cmu_graphics import *


def createBossBackground():
    # Dark, smoky red sky
    sky = Rect(
        0, 0, 819, 820, fill=gradient(rgb(25, 0, 0), rgb(150, 25, 0), start="top")
    )
    moon = Circle(150, 120, 45, fill=rgb(200, 40, 20))

    # Volcanoes in the distance, with glowing craters
    volcanoes = Polygon(
        0,
        640,
        0,
        520,
        90,
        470,
        170,
        330,
        230,
        330,
        330,
        520,
        420,
        560,
        560,
        380,
        610,
        380,
        720,
        560,
        819,
        520,
        819,
        640,
        fill=rgb(35, 12, 10),
    )
    craterGlow = Group(
        Circle(200, 330, 24, fill="gold", opacity=70),
        Circle(585, 380, 22, fill="gold", opacity=70),
    )

    # Lava running down the volcanoes
    lavaFlows = Group(
        Polygon(
            185,
            330,
            215,
            330,
            205,
            400,
            225,
            470,
            205,
            560,
            190,
            470,
            198,
            400,
            fill="orangeRed",
        ),
        Polygon(
            195,
            335,
            205,
            335,
            202,
            400,
            212,
            470,
            204,
            540,
            198,
            470,
            201,
            400,
            fill="gold",
        ),
        Polygon(
            570,
            380,
            600,
            380,
            610,
            450,
            595,
            520,
            600,
            600,
            580,
            520,
            588,
            450,
            fill="orangeRed",
        ),
        Polygon(
            580,
            385,
            590,
            385,
            597,
            450,
            589,
            520,
            592,
            580,
            585,
            520,
            590,
            450,
            fill="gold",
        ),
    )

    # Smoke pouring out of the craters
    smoke = Group(
        Oval(200, 280, 90, 50, fill="dimGray", opacity=60),
        Oval(225, 230, 120, 60, fill="dimGray", opacity=50),
        Oval(260, 170, 150, 70, fill="dimGray", opacity=40),
        Oval(585, 330, 80, 45, fill="dimGray", opacity=60),
        Oval(560, 280, 110, 55, fill="dimGray", opacity=50),
        Oval(530, 215, 140, 65, fill="dimGray", opacity=40),
    )

    # A lake of lava behind the battle
    lavaLake = Rect(
        0, 580, 819, 120, fill=gradient("orangeRed", "darkRed", start="top")
    )
    lavaBubbles = Group(
        Oval(120, 600, 40, 10, fill="gold"),
        Oval(330, 640, 60, 12, fill="orange"),
        Oval(560, 610, 35, 9, fill="gold"),
        Oval(720, 655, 50, 11, fill="orange"),
        Oval(60, 670, 45, 10, fill="orange"),
    )

    # Glowing embers floating in the air
    embers = Group()
    for x, y in [
        (60, 300),
        (300, 250),
        (410, 420),
        (470, 150),
        (650, 260),
        (760, 380),
        (350, 530),
        (90, 520),
        (740, 180),
        (520, 480),
    ]:
        embers.add(Circle(x, y, 3, fill="orange"))

    background = Group(
        sky,
        moon,
        smoke,
        volcanoes,
        craterGlow,
        lavaFlows,
        lavaLake,
        lavaBubbles,
        embers,
    )
    return background
