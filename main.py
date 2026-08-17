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


def movePlayerX(amount):
    oldLeft = player.left
    oldRight = player.right

    player.centerX += amount

    for platform in platforms:
        verticallyOverlapping = (
            player.bottom > platform.top and player.top < platform.bottom
        )

        if not verticallyOverlapping:
            continue

        # Moving right: hit left side of platform
        if amount > 0:
            if oldRight <= platform.left and player.right >= platform.left:
                player.right = platform.left

        # Moving left: hit right side of platform
        elif amount < 0:
            if oldLeft >= platform.right and player.left <= platform.right:
                player.left = platform.right


def onKeyPress(key):
    if "left" == key or "a" == key:
        movePlayerX(-player.speed)

    if "right" == key or "d" == key:
        movePlayerX(player.speed)

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

        # Land on top of platform
        if (
            horizontallyOverlapping
            and player.dy >= 0
            and oldBottom <= platform.top <= player.bottom
        ):
            player.bottom = platform.top
            player.dy = 0
            player.onGround = True

        # Hit underside of platform
        elif (
            horizontallyOverlapping
            and player.dy < 0
            and oldTop >= platform.bottom >= player.top
        ):
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
