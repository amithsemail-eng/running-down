from cmu_graphics import *


class Bullet:
    def __init__(self, x, y, direction):
        self.shape = Circle(x, y, 5, fill="cyan", border="blue")
        self.direction = direction
        self.speed = 20

    def update(self):
        if self.direction == "right":
            self.shape.centerX += self.speed
        else:
            self.shape.centerX -= self.speed

    def isOffScreen(self, screenWidth):
        return self.shape.right < 0 or self.shape.left > screenWidth


def createBullet(player):
    x, y = player.getBulletStart()
    return Bullet(x, y, player.facing)
