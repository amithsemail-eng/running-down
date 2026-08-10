BUFF = "buff"
DEBUFF = "debuff"
KEY = "key"


def startSpeedBoost(player, startBoostTimer):
    player.speed = player.boostSpeed
    startBoostTimer()


def startJumpPowerBoost(player, startBoostTimer):
    player.jumpPower = player.jumpBoostPower
    startBoostTimer()


class Item:
    def __init__(self, name, itemType, effect=None):
        self.name = name
        self.itemType = itemType
        self.itemType = self.itemType
        self.effect = effect


speedPowerBoost = Item("Speed Boost", BUFF, effect=startSpeedBoost)
