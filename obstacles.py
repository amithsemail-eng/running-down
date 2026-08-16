from cmu_graphics import *


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
        drawSpikes(240, 670, 100),
        drawSpikes(310, 520, 80),
    ]

    return obstacles
