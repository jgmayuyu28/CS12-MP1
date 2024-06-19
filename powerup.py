from stage import SPRITE_BANK

class PowerUp:
    def __init__(self, x, y, duration):

        self.x = x
        self.y = y
        IMG = 0
        U = 0
        V = 32
        WIDTH = 8
        HEIGHT = 8
        self.original_duration = duration
        self.duration = duration
        self.freeze = False
        self.state = "ACTIVE"


def drawPowerUp(pyxel, powerUp):

    pyxel.blt(
    powerUp.x,
    powerUp.y,
    SPRITE_BANK,
    0,
    32,
    8,
    8
)