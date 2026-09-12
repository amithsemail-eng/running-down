import math
from cmu_graphics import *


class Sword:
    def __init__(self, player, body, arm):
        self.player = player
        self.body = body
        self.arm = arm
        self.isSheathed = False
        self.swingFrame = None
        self.shape = Group(
            Polygon(
                -3, -8, -3, -35, 0, -43, 3, -35, 3, -8, fill="silver", border="dimGray"
            ),
            Line(0, -10, 0, -35, fill="white", lineWidth=1),
            Line(-7, -6, 7, -6, fill="goldenrod", lineWidth=3),
            Line(0, -4, 0, 5, fill="saddleBrown", lineWidth=4),
            Circle(0, 6, 3, fill="goldenrod"),
        )
        self.offsetX = self.shape.centerX
        self.offsetY = self.shape.centerY
        self.sheath = Group(
            Line(0, 0, 12, 29, fill="saddleBrown", lineWidth=8),
            Line(-4, 1, 4, -1, fill="goldenrod", lineWidth=3),
        )
        self.refresh()

    def toggle(self):
        self.isSheathed = not self.isSheathed
        self.swingFrame = None
        self.refresh()

    def swing(self):
        if not self.isSheathed and self.swingFrame is None:
            self.swingFrame = 0
            self.refresh()

    def reset(self):
        self.isSheathed = False
        self.swingFrame = None
        self.refresh()

    def update(self):
        if self.swingFrame is not None:
            self.swingFrame += 1
            if self.swingFrame >= 21:
                self.swingFrame = None
        self.refresh()

    def refresh(self):
        direction = 1 if self.player.facing == "right" else -1
        dx, dy, angle = -10, 15, -25
        if self.swingFrame is not None:
            # Wind up, slash forward, follow through, then return to rest.
            poses = [
                (0, -10, 15, -25),
                (4, -12, -16, -60),
                (11, 20, 0, 90),
                (15, 16, 12, 125),
                (21, -10, 15, -25),
            ]
            for start, end in zip(poses, poses[1:]):
                if start[0] <= self.swingFrame <= end[0]:
                    t = (self.swingFrame - start[0]) / (end[0] - start[0])
                    dx, dy, angle = [
                        a + (b - a) * t for a, b in zip(start[1:], end[1:])
                    ]
                    break

        self.arm.x1 = self.body.centerX - direction * 10
        self.arm.y1 = self.body.top + 8
        self.arm.x2 = self.arm.x1 + direction * dx
        self.arm.y2 = self.arm.y1 + dy
        self.sheath.visible = self.isSheathed
        if self.isSheathed:
            # Show the hilt above the scabbard, with the blade covered.
            gripX = self.body.centerX - direction * 13
            gripY = self.body.top - 3
            angle = 160
        else:
            gripX, gripY = self.arm.x2, self.arm.y2

        rotation = direction * angle
        radians = math.radians(rotation)
        self.shape.rotateAngle = rotation
        self.shape.centerX = (
            gripX + self.offsetX * math.cos(radians) - self.offsetY * math.sin(radians)
        )
        self.shape.centerY = (
            gripY + self.offsetX * math.sin(radians) + self.offsetY * math.cos(radians)
        )
        if self.isSheathed:
            vx, vy = math.sin(radians), -math.cos(radians)
            cover, rim = self.sheath.children
            cover.x1, cover.y1 = gripX + vx * 9, gripY + vy * 9
            cover.x2, cover.y2 = gripX + vx * 42, gripY + vy * 42
            rim.x1, rim.y1 = cover.x1 - vy * 5, cover.y1 + vx * 5
            rim.x2, rim.y2 = cover.x1 + vy * 5, cover.y1 - vx * 5
        # The blade is hidden while the sword is on the player's back.
        self.shape.children[0].opacity = 0 if self.isSheathed else 100
        self.shape.children[1].opacity = 0 if self.isSheathed else 100
