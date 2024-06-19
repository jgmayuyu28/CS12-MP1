import pyxel
from stage import StageItem, TILE_SIZE, SPRITE_BANK, isColliding

class Bullet:

    def __init__(self, x, y, dir, stage, player):

        self.x = x
        self.y = y
        self.dir = dir
        self.stage = stage
        self.player = player
        self.U, self.V = 64, 11
        self.WIDTH, self.HEIGHT = 3, 2

        if self.dir == "RIGHT":

            self.U, self.V = 69, 3
            self.WIDTH, self.HEIGHT = 3, 2

        elif self.dir == "UP":

            self.U, self.V = 59, 8
            self.WIDTH, self.HEIGHT = 2, 3

        elif self.dir == "DOWN":

            self.U, self.V = 59, 5
            self.WIDTH, self.HEIGHT = 2, 3

        self.state = "ACTIVE"


    def left(self):

        self.player.timer -= 0.05
        new_x = (self.x - 3)
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_x  = tile_x - 1

        next_tile = self.stage.stage_map[tile_y][new_tile_x]

        if (
            (next_tile == StageItem.BRICK or next_tile == StageItem.CRACKED_BRICK or next_tile == StageItem.STONE
            or next_tile == StageItem.MIRROR_LEFT  or next_tile == StageItem.MIRROR_RIGHT) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ):

            if next_tile == StageItem.BRICK:

                self.state = "INACTIVE"
                self.stage.set(new_tile_x, tile_y, StageItem.CRACKED_BRICK)
                return
            
            elif next_tile == StageItem.CRACKED_BRICK:

                self.state = "INACTIVE"
                self.stage.clear(new_tile_x, tile_y)
                return
            
            elif next_tile == StageItem.HOME:

                self.state = "INACTIVE"
                self.stage.clear(new_tile_x, tile_y)
                return

            elif next_tile == StageItem.MIRROR_LEFT:

                self.state = "ACTIVE"
                self.dir = "DOWN"
                self.x, self.y = (new_tile_x * TILE_SIZE) + 3, (tile_y * TILE_SIZE) + 3 

            elif next_tile == StageItem.MIRROR_RIGHT:

                self.state = "ACTIVE"
                self.dir = "UP"
                self.x, self.y = (new_tile_x * TILE_SIZE) + 3, (tile_y * TILE_SIZE) - 3 
                
            elif next_tile == StageItem.STONE:

                self.state = "INACTIVE"
                return

        if self.state != "INACTIVE":

            if self.dir == "UP":

                new_y = (self.y - 3) % pyxel.width
                self.y = new_y

            elif self.dir == "DOWN":

                new_y = (self.y + 3) % pyxel.width
                self.y = new_y

            else:

                new_x = (self.x - 3) % pyxel.width
                self.x = new_x
    

    def right(self):

        self.player.timer -= 0.05
        new_x = (self.x + 3)
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_x  = tile_x + 1

        next_tile = self.stage.stage_map[tile_y][new_tile_x]

        if (
            (next_tile == StageItem.BRICK or next_tile == StageItem.CRACKED_BRICK or next_tile == StageItem.STONE
            or next_tile == StageItem.MIRROR_LEFT  or next_tile == StageItem.MIRROR_RIGHT) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ):

            if next_tile == StageItem.BRICK:

                self.state = "INACTIVE"
                self.stage.set(new_tile_x, tile_y, StageItem.CRACKED_BRICK)
                return
            
            elif next_tile == StageItem.CRACKED_BRICK:

                self.state = "INACTIVE"
                self.stage.clear(new_tile_x, tile_y)
                return

            elif next_tile == StageItem.HOME:

                self.state = "INACTIVE"
                self.stage.clear(new_tile_x, tile_y)
                return

            elif next_tile == StageItem.MIRROR_LEFT:

                self.state = "ACTIVE"
                self.dir = "UP"
                self.x, self.y = (new_tile_x * TILE_SIZE) + 3, (tile_y * TILE_SIZE) - 3

            elif next_tile == StageItem.MIRROR_RIGHT:

                self.state = "ACTIVE"
                self.dir = "DOWN"
                self.x, self.y = (new_tile_x * TILE_SIZE) + 3, (tile_y * TILE_SIZE) + 3

            elif next_tile == StageItem.STONE:

                self.state = "INACTIVE"
                return
        
        if self.state != "INACTIVE":

            if self.dir == "UP":

                new_y = (self.y - 3) % pyxel.width
                self.y = new_y

            elif self.dir == "DOWN":

                new_y = (self.y + 3) % pyxel.width
                self.y = new_y

            else:

                new_x = (self.x + 3) % pyxel.width
                self.x = new_x


    def up(self):

        self.player.timer -= 0.05
        new_y = (self.y - 3)
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_y  = tile_y - 1

        next_tile = self.stage.stage_map[new_tile_y][tile_x]

        if (
            (next_tile == StageItem.BRICK or next_tile == StageItem.CRACKED_BRICK or next_tile == StageItem.STONE
            or next_tile == StageItem.MIRROR_LEFT  or next_tile == StageItem.MIRROR_RIGHT) and
            isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ):

            if next_tile == StageItem.BRICK:

                self.state = "INACTIVE"
                self.stage.set(tile_x, new_tile_y, StageItem.CRACKED_BRICK)
                return
            
            elif next_tile == StageItem.CRACKED_BRICK:

                self.state = "INACTIVE"
                self.stage.clear(tile_x, new_tile_y)
                return
            
            elif next_tile == StageItem.HOME:

                self.state = "INACTIVE"
                self.stage.clear(tile_x, new_tile_y)
                return
            
            elif next_tile == StageItem.MIRROR_LEFT:

                self.state = "ACTIVE"
                self.dir = "RIGHT"
                self.x, self.y = (tile_x * TILE_SIZE) + 3, (new_tile_y * TILE_SIZE) + 3

            elif next_tile == StageItem.MIRROR_RIGHT:

                self.state = "ACTIVE"
                self.dir = "LEFT"
                self.x, self.y = (tile_x * TILE_SIZE) - 3, (new_tile_y * TILE_SIZE) - 3

            elif next_tile == StageItem.STONE:

                self.state = "INACTIVE"
                return
        
        if self.state != "INACTIVE":

            if self.dir == "LEFT":

                new_x = (self.x - 3) % pyxel.width
                self.x = new_x
            elif self.dir == "RIGHT":

                new_x = (self.x + 3) % pyxel.width
                self.x = new_x
            else:

                new_y = (self.y - 3) % pyxel.width
                self.y = new_y


    def down(self):

        self.player.timer -= 0.05
        new_y = (self.y + 3)
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_y  = tile_y + 1

        next_tile = self.stage.stage_map[new_tile_y][tile_x]

        if (
            (next_tile == StageItem.BRICK or next_tile == StageItem.CRACKED_BRICK or next_tile == StageItem.STONE
            or next_tile == StageItem.MIRROR_LEFT  or next_tile == StageItem.MIRROR_RIGHT) and
            isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ):

            if next_tile == StageItem.BRICK:

                self.state = "INACTIVE"
                self.stage.set(tile_x, new_tile_y, StageItem.CRACKED_BRICK)
                return
            
            elif next_tile == StageItem.CRACKED_BRICK:

                self.state = "INACTIVE"
                self.stage.clear(tile_x, new_tile_y)
                return
            
            elif next_tile == StageItem.HOME:

                self.state = "INACTIVE"
                self.stage.clear(tile_x, new_tile_y)
                return
            
            elif next_tile == StageItem.MIRROR_LEFT:

                self.state = "ACTIVE"
                self.dir = "LEFT"
                self.x, self.y = (tile_x * TILE_SIZE) - 3, (new_tile_y * TILE_SIZE) + 3

            elif next_tile == StageItem.MIRROR_RIGHT:

                self.state = "ACTIVE"
                self.dir = "RIGHT"
                self.x, self.y = (tile_x * TILE_SIZE) + 3, (new_tile_y * TILE_SIZE) + 3

            elif next_tile == StageItem.STONE:

                self.state = "INACTIVE"
                return
        
        if self.state != "INACTIVE":

            if self.dir == "LEFT":

                new_x = (self.x - 3) % pyxel.width
                self.x = new_x

            elif self.dir == "RIGHT":

                new_x = (self.x + 3) % pyxel.width
                self.x = new_x

            else:

                new_y = (self.y + 3) % pyxel.width
                self.y = new_y


def drawBullet(pyxel, bullet):

    U, V = 0, 0
    W, H = 0, 0

    if bullet.dir == "LEFT":

        U, V = 64, 11
        W, H = 3, 2

    elif bullet.dir == "RIGHT":

        U, V = 69, 3
        W, H = 3, 2

    elif bullet.dir == "UP":

        U, V = 59, 8
        W, H = 2, 3

    elif bullet.dir == "DOWN":

        U, V = 59, 5
        W, H = 2, 3

    pyxel.blt(
    bullet.x,
    bullet.y,
    SPRITE_BANK,
    U,
    V,
    W,
    H
)
