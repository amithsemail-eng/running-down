import cmu_graphics
from cmu_graphics import *
from playerofgame import createPlayer
from screens import createScreens
from chest import createChests
from platforms import createPlatforms
from obstacles import createObstacles

app.stepPerSec = 30
app.width = 819
app.height = 820
app.boostTimer = 0
app.boostTimerLength = 10
# left top width height
app.gameOver = False

backgroundMusic = Sound("sounds/jumphigherrunfaster.ogg")
backgroundMusic.play(loop=False)
jumpSound = Sound("sounds/jump.flac")

player = createPlayer()
platforms = createPlatforms()
deathScreen, deathMessage, winScreen, winMessage = createScreens(app.width, app.height)

chests = createChests()
obstacles = createObstacles()


def startBoostTimer():
    app.boostTimer = app.boostTimerLength * app.stepPerSec


def winner():
    winMessage.visible = True
    winScreen.visible = True


def restart():
    player.centerX = 0
    player.centerY = 780
    player.dy = 0
    deathScreen.visible = True
    deathMessage.visible = True
    app.deathTimer = 300
    app.gameOver = True


def onKeyPress(key):
    if "left" == key or "a" == key:
        player.centerX -= player.speed
    if "right" == key or "d" == key:
        player.centerX += player.speed
    if "space" == key and player.onGround:
        jumpSound.play()
        player.dy = player.jumpPower
        player.onGround = False


def onStep():

    player.onGround = False
    if player.left < 0:
        player.left = 0
    if player.right > app.width:
        player.right = app.width
    # previous location
    oldTop = player.top
    oldBottom = player.bottom
    oldLeft = player.left
    oldRight = player.right
    # gravity
    player.dy += 0.6
    player.centerY += player.dy
    if player.bottom >= app.height:
        restart()
    if player.top <= 0:
        player.top = 0
    for obstacle in obstacles:
        if player.hitsShape(obstacle):
            restart()

    for platform in platforms:
        horizontallyOverlapping = (
            player.right > platform.left and player.left < platform.right
        )
        verticallyOverlapping = (
            player.bottom > platform.top and player.top < platform.bottom
        )
        if horizontallyOverlapping:

            if player.dy >= 0 and oldBottom <= platform.top <= player.bottom:
                player.bottom = platform.top
                player.dy = 0
                player.onGround = True

            elif player.dy < 0 and oldTop >= platform.bottom >= player.top:
                player.top = platform.bottom
                player.dy = 0

    for chest in chests:
        if player.hitsShape(chest.shape):
            chest.open()
            chest.item.effect(player, startBoostTimer)

    winning_platform = platforms[-1]
    if player.hitsShape(winning_platform):
        winner()
    if app.boostTimer > 0:
        app.boostTimer -= 1
        if app.boostTimer == 0:
            player.speed = player.normSpeed

    if app.gameOver:
        app.deathTimer -= 1
        if app.deathTimer <= 0:
            deathScreen.visible = False
            deathMessage.visible = False
            app.gameOver = False


cmu_graphics.run()
