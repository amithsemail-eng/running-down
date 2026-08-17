from cmu_graphics import *

healthBarBackground = Rect(20, 20, 200, 25, fill="darkRed", border="black")

healthBar = Rect(20, 20, 200, 25, fill="limeGreen", border="black")

healthLabel = Label("100 / 100", 120, 32, fill="white", bold=True)


class HealthBar:
    def __init__(self, player):
        self.player = player
        self.maxWidth = 200

        self.background = Rect(
            20, 20, self.maxWidth, 25, fill="darkRed", border="black"
        )

        self.bar = Rect(20, 20, self.maxWidth, 25, fill="limeGreen", border="black")

        self.label = Label(
            str(player.health) + " / " + str(player.maxHealth),
            120,
            32,
            fill="white",
            bold=True,
        )


def createHealthBar(player):
    return HealthBar(player)
