from cmu_graphics import *


class Fireball:
    def __init__(self, x, y, targetX, targetY):
        self.shape = Group(
            Circle(x, y, 10, fill="orangeRed"),
            Circle(x, y, 5, fill="gold"),
        )
        # Split the trip into 40 small steps, so it reaches the target in 40 steps
        self.dx = (targetX - x) / 40
        self.dy = (targetY - y) / 40

    def update(self):
        self.shape.centerX += self.dx
        self.shape.centerY += self.dy

    def isOffScreen(self, screenWidth, screenHeight):
        return (
            self.shape.right < 0
            or self.shape.left > screenWidth
            or self.shape.top > screenHeight
        )
