from cmu_graphics import *
import math


def drawSpikes(x, y, width=100, height=20):
    spikes = Group()

    spikeWidth = 20
    numberOfSpikes = width // spikeWidth

    for i in range(numberOfSpikes):
        left = x + i * spikeWidth

        spike = Polygon(
            left,
            y + height,
            left + spikeWidth / 2,
            y,
            left + spikeWidth,
            y + height,
            fill="gray",
            border="black",
        )

        spikes.add(spike)

    return spikes


def createObstacles():
    obstacles = [
        drawSpikes(270, 670, 100),
        drawSpikes(310, 495, 80),
    ]

    return obstacles


class SwingingAxe:
    def __init__(self, x, y, length=150):
        self.pivotX = x
        self.pivotY = y
        self.length = length

        self.angle = 0
        self.swingSpeed = 3
        self.maxAngle = 60

        self.handle = Line(x, y, x, y + length, fill="brown", lineWidth=8)

        self.blade = Polygon(
            x - 25,
            y + length - 15,
            x + 25,
            y + length - 15,
            x + 35,
            y + length + 10,
            x,
            y + length + 30,
            x - 35,
            y + length + 10,
            fill="silver",
            border="black",
        )

        self.pivot = Circle(x, y, 8, fill="black")

        self.shape = Group(self.handle, self.blade, self.pivot)

    def update(self):
        self.angle += self.swingSpeed

        if self.angle >= self.maxAngle:
            self.angle = self.maxAngle
            self.swingSpeed *= -1

        elif self.angle <= -self.maxAngle:
            self.angle = -self.maxAngle
            self.swingSpeed *= -1

        radians = math.radians(self.angle)

        axeX = self.pivotX + math.sin(radians) * self.length
        axeY = self.pivotY + math.cos(radians) * self.length

        self.handle.x2 = axeX
        self.handle.y2 = axeY

        self.blade.centerX = axeX
        self.blade.centerY = axeY


def createAxes():
    axes = [SwingingAxe(400, 100)]

    return axes
