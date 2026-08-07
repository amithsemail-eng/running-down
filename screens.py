from cmu_graphics import *


def createDeathScreen(width, height):
    deathScreen = Rect(0, 0, width, height, fill="red", visible=False)
    deathMessage = Label(
        "You have died, want to play?",
        app.width // 2,
        app.height // 2,
        size=65,
        fill="black",
        visible=False,
    )
    return deathScreen, deathMessage


def createWinScreen(width, height):
    winScreen = Rect(0, 0, width, height, fill="green", visible=False)
    winMessage = Label(
        "Great, you won!",
        app.width // 2,
        app.height // 2,
        size=80,
        fill="blue",
        visible=False,
    )
    return winScreen, winMessage


def createScreens(width, height):
    deathScreen, deathMessage = createDeathScreen(width, height)
    winScreen, winMessage = createWinScreen(width, height)
    return deathScreen, deathMessage, winScreen, winMessage
