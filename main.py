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
enemyPlatform = platforms[0]
enemy = createAlien(enemyPlatform.centerX, enemyPlatform.top, scale=0.55)
enemy.speed = 3
enemy.dy = 0
enemy.jumpPower = -13
enemy.onGround = False
enemy.groundPlatform = None
enemy.direction = 1
enemy.bottom = enemyPlatform.top - 60
enemy.attackTimer = 0
enemy.attackCooldown = 0
slash = Arc(0, 0, 80, 80, 30, 120, fill="white", opacity=0, visible=False)
chests = createChests()
obstacles = createObstacles()
axes = createAxes()
bullets = []


def applyEnemyGravity():
    left, oldTop, right, oldBottom = enemy.getBounds()

    enemy.dy += 0.6
    movement = enemy.dy
    landedPlatform = None
    for platform in platforms:
        if right <= platform.left or left >= platform.right:
            continue
        if enemy.dy >= 0 and oldBottom <= platform.top:
            gap = platform.top - oldBottom
            if gap <= movement:
                movement = gap
                landedPlatform = platform
        elif enemy.dy < 0 and oldTop >= platform.bottom:
            movement = max(movement, platform.bottom - oldTop)
    enemy.centerY += movement
    enemy.groundPlatform = landedPlatform
    enemy.onGround = landedPlatform is not None
    if enemy.onGround or movement != enemy.dy:
        enemy.dy = 0


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

    enemyLocation = enemy.getBounds()
    enemyLeft, enemyTop, enemyRight, enemyBottom = enemyLocation
    if bottom > enemyTop and top < enemyBottom:
        if amount > 0 and right <= enemyLeft:
            amount = min(amount, enemyLeft - right)
        elif amount < 0 and left >= enemyRight:
            amount = max(amount, enemyRight - left)

    player.centerX += max(-left, min(amount, app.width - right))
    player.sword.refresh()
    left, top, right, bottom = player.getBounds()
    player.onGround = any(
        abs(bottom - platform.top) < 0.001
        and right > platform.left
        and left < platform.right
        for platform in platforms
    )


def moveEnemyX(amount):
    el, et, er, eb = enemy.getBounds()
    blockingBoxes = []
    for platform in platforms:
        blockingBoxes.append(
            (platform.left, platform.top, platform.right, platform.bottom)
        )
    blockingBoxes.append(player.getBounds())
    for box in blockingBoxes:
        boxLeft, boxTop, boxRight, boxBottom = box
        if eb <= boxTop or et >= boxBottom:
            continue

        if amount > 0 and er <= boxLeft:
            amount = min(amount, boxLeft - er)
        elif amount < 0 and el >= boxRight:
            amount = max(amount, boxRight - el)
    enemy.centerX += amount

    return amount


def chasePlayer():
    el, et, er, eb = enemy.getBounds()
    pl, pt, pr, pb = player.getBounds()
    dx = (pl + pr) / 2 - (el + er) / 2
    dy = pb - eb
    direction = 1 if dx > 0 else -1
    if abs(dx) < 40:
        enemy.updateWalkAnimation(False)
        return
    enemy.startTurn(direction)
    plat = enemy.groundPlatform
    step = enemy.speed * direction
    if plat is not None and dy < 10:
        atRightEdge = direction == 1 and er + step > plat.right
        atLeftEdge = direction == -1 and el + step < plat.left
        if atLeftEdge or atRightEdge:
            enemy.updateWalkAnimation(False)
            tryEnemyJump(dy)
            return

    moved = moveEnemyX(step)
    enemy.updateWalkAnimation(enemy.onGround and moved != 0)
    if moved == 0:
        tryEnemyJump(dy)


def playerInReach():
    el, et, er, eb = enemy.getBounds()
    pl, pt, pr, pb = player.getBounds()
    dx = (pl + pr) / 2 - (el + er) / 2
    return abs(dx) < 50 and abs(pb - eb) < 50


def tryEnemyJump(dy):
    if enemy.onGround == False:
        return

    if dy < -20:
        enemy.dy = enemy.jumpPower
        enemy.onGround = False


def updateEnemy():
    applyEnemyGravity()
    updateEnemyAttack()
    if enemy.attackTimer == 0:
        chasePlayer()
    else:
        enemy.updateWalkAnimation(False)


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


def updateEnemyAttack():
    if enemy.attackCooldown > 0:
        enemy.attackCooldown -= 1
        if enemy.attackTimer == 0:
            if enemy.attackCooldown == 0 and enemy.onGround and playerInReach():
                enemy.attackTimer = 24
            else:
                slash.visible = False
                return
    enemy.attackTimer -= 1
    # Put the slash in front of the alien
    el, et, er, eb = enemy.getBounds()
    if enemy.facing == "right":
        slash.centerX, slash.startAngle = er, 30
    else:
        slash.centerX, slash.startAngle = el, 210
        slash.centerY = (et + eb) / 2
        slash.visible = True
        slash.toFront()
    if enemy.attackTimer > 8:  # windup
        slash.opacity = 20
    elif enemy.attackTimer > 3:  # strike
        slash.opacity = 90
    if player.hitsShape(slash):
        player.takeDamage(20, healthBar, restart)
    else:  # recovery
        slash.visible = False
    if enemy.attackTimer == 0:
        enemy.attackCooldown = 45


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
