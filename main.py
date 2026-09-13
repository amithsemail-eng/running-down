import cmu_graphics
from cmu_graphics import *
from playerofgame import createPlayer
from screens import createScreens
from chest import createChests
from platforms import createPlatforms
from obstacles import createObstacles, createAxes
from healthbar import createHealthBar
from bullet import createBullet
from alien import createAlien

app.stepsPerSecond = 30
app.width = 819
app.height = 820
app.boostTimer = 0
app.boostTimerLength = 10
# left top width height
app.gameOver = False

backgroundMusic = Sound("sounds/jumphigherrunfaster.ogg")
backgroundMusic.play(loop=True)
jumpSound = Sound("sounds/jump.flac")

player = createPlayer()
healthBar = createHealthBar(player)
platforms = createPlatforms()
deathScreen, deathMessage, winScreen, winMessage = createScreens(app.width, app.height)
enemyPlatform = platforms[3]
enemy = createAlien(280, enemyPlatform.top, scale=0.55)
enemy.speed = 3
enemy.direction = 1
enemy.leftLimit = 200
enemy.rightLimit = enemyPlatform.right
chests = createChests()
obstacles = createObstacles()
axes = createAxes()
bullets = []


def startBoostTimer():
    app.boostTimer = app.boostTimerLength * app.stepsPerSecond


def winner():
    winMessage.visible = True
    winScreen.visible = True


def restart():
    if app.gameOver:
        return
    deathScreen.visible = True
    deathMessage.visible = True
    deathScreen.toFront()
    deathMessage.toFront()
    app.deathTimer = 300
    app.gameOver = True


def resetPlayer():
    player.stand()
    player.faceRight()
    player.updateTurnAnimation()
    player.centerX = 50
    player.bottom = platforms[0].top
    player.dy = 0
    player.onGround = True
    player.sword.reset()
    player.health = player.maxHealth
    player.damageCooldown = 0
    player.speed = player.normSpeed
    player.jumpPower = player.normJumpPower
    app.boostTimer = 0
    healthBar.update(restart)
    for bullet in bullets:
        bullet.shape.visible = False
    bullets.clear()
    for chest in chests:
        chest.opened = False
        chest.shape.visible = True
    deathScreen.visible = deathMessage.visible = False
    winScreen.visible = winMessage.visible = False
    app.gameOver = False


def tryStand():
    if not player.isCrouching:
        return True
    left, top, right, bottom = player.getBounds()
    for platform in platforms:
        if (
            right > platform.left
            and left < platform.right
            and bottom > platform.top
            and top - 14 < platform.bottom
        ):
            return False
    player.stand()
    return True


def movePlayerX(amount):
    left, top, right, bottom = player.getBounds()
    for platform in platforms:
        if bottom <= platform.top or top >= platform.bottom:
            continue
        # Limit movement to the nearest wall, even at boosted speed.
        if amount > 0 and right <= platform.left:
            amount = min(amount, platform.left - right)
        elif amount < 0 and left >= platform.right:
            amount = max(amount, platform.right - left)
    player.centerX += max(-left, min(amount, app.width - right))
    player.sword.refresh()
    left, top, right, bottom = player.getBounds()
    player.onGround = any(
        abs(bottom - platform.top) < 0.001
        and right > platform.left
        and left < platform.right
        for platform in platforms
    )


def updateEnemy():
    enemy.updateTurnAnimation()
    if enemy.turning:
        return
    enemy.centerX += enemy.speed * enemy.direction
    enemy.updateWalkAnimation(enemy.speed != 0)
    if enemy.direction == 1 and enemy.centerX >= enemy.rightLimit:
        enemy.centerX = enemy.rightLimit
        enemy.startTurn(-1)


def onKeyPress(key):
    if app.gameOver:
        return
    if "left" == key or "a" == key:
        player.faceLeft()
        movePlayerX(-player.speed)

    if "right" == key or "d" == key:
        player.faceRight()
        movePlayerX(player.speed)

    if "space" == key and player.onGround and tryStand():
        jumpSound.play()
        player.dy = player.jumpPower
        player.onGround = False
    if "1" == key:
        bullets.append(createBullet(player))
    if key == "up":
        player.sword.toggle()
    if key == "0":
        player.sword.swing()

    if key == "down":
        if player.isCrouching:
            tryStand()
        else:
            player.crouch()


def onStep():
    if app.gameOver:
        app.deathTimer -= 1
        if app.deathTimer <= 0:
            resetPlayer()
        return

    if player.damageCooldown > 0:
        player.damageCooldown -= 1
    player.updateTurnAnimation()
    player.onGround = False
    left, oldTop, right, oldBottom = player.getBounds()
    # Find the nearest platform crossed before applying gravity movement.
    player.dy += 0.6
    movement = player.dy
    landedPlatform = None
    for platform in platforms:
        if right <= platform.left or left >= platform.right:
            continue
        if player.dy >= 0 and oldBottom <= platform.top:
            gap = platform.top - oldBottom
            if gap <= movement:
                movement = gap
                landedPlatform = platform
        elif player.dy < 0 and oldTop >= platform.bottom:
            movement = max(movement, platform.bottom - oldTop)
    player.centerY += movement
    if landedPlatform is not None:
        player.dy = 0
        player.onGround = True
    elif movement != player.dy:
        player.dy = 0  
    player.sword.update()

    if player.bottom >= app.height:
        restart()
        return
    # Allow the head above the viewport so the y=30 platform is reachable.
    for obstacle in obstacles:
        if player.hitsShape(obstacle):
            player.takeDamage(15, healthBar, restart)
            if app.gameOver:
                return
    for ax in axes:
        ax.update()
        if player.hitsShape(ax.blade):
            player.takeDamage(25, healthBar, restart)
            if app.gameOver:
                return
    if player.hitsShape(enemy):
        player.takeDamage(5, healthBar, restart)

    updateEnemy()
    for bullet in bullets:
        bullet.update()
        if bullet.isOffScreen(app.width):
            bullet.shape.visible = False
            bullets.remove(bullet)
    for chest in chests:
        if player.hitsShape(chest.shape):
            chest.open()
            chest.item.effect(player, startBoostTimer)

    winning_platform = platforms[-1]
    if landedPlatform is winning_platform:
        winner()
    if app.boostTimer > 0:
        app.boostTimer -= 1
        if app.boostTimer == 0:
            player.speed = player.normSpeed


cmu_graphics.run()
