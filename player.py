from stage import StageItem, isColliding, TILE_SIZE
from bullet import Bullet
from sound import PyxelSounds
import pyxel

class Player:

    IMG = 0
    U = 16
    V = 0
    WIDTH = 8
    HEIGHT = 8
    DX = 1
    DY = 1


    def __init__(self, x, y, stage, enemies, health):

        self.x = x
        self.y = y
        self.prev_x = self.x
        self.prev_y = self.y
        self.stage = stage
        self.bullets = []
        self.enemies = enemies
        self.dir = "RIGHT"
        self.state = "ACTIVE"
        self.health = health
        self.timer = 0.2
        self.ff_on = False
        self.isGameOver = False
        self.sounds = PyxelSounds()

    def player_behavior(self):

        self.playerMovement()
        self.shoot()
        self.bulletMovement()


    def playerMovement(self):
        
        is_free = 0

        if pyxel.btn(pyxel.KEY_W):

            self.player_img = 0
            self.dir = "UP"
            self.U = 24
            self.V = 8

            for enemy in self.enemies:

                if (self.x + self.WIDTH > enemy.x
                and enemy.x + self.WIDTH > self.x
                and (self.y - 1) + self.HEIGHT > enemy.y
                and enemy.y + self.HEIGHT > self.y - 1):
                    
                    is_free += 1

            if is_free == 0:

                self.move_up()

            is_free = 0

        elif pyxel.btn(pyxel.KEY_S):

            self.player_img = 0
            self.dir = "DOWN"
            self.U = 24
            self.V = 0

            for enemy in self.enemies:
                
                if (self.x + self.WIDTH > enemy.x
                and enemy.x + self.WIDTH > self.x
                and (self.y + 1) + self.HEIGHT > enemy.y
                and enemy.y + self.HEIGHT > self.y + 1):
                    
                    is_free += 1

            if is_free == 0:

                self.move_down()

            is_free = 0

        elif pyxel.btn(pyxel.KEY_A):

            self.player_img = 0
            self.dir = "LEFT"
            self.U = 16
            self.V = 8

            for enemy in self.enemies:

                if ((self.x - 1) + self.WIDTH > enemy.x
                and enemy.x + self.WIDTH > self.x - 1
                and self.y + self.HEIGHT > enemy.y
                and enemy.y + self.HEIGHT > self.y):
                    
                    is_free += 1

            if is_free == 0:

                self.move_left()

            is_free = 0

        elif pyxel.btn(pyxel.KEY_D):

            self.player_img = 0
            self.dir = "RIGHT"
            self.U = 16
            self.V = 0

            for enemy in self.enemies:

                if ((self.x + 1) + self.WIDTH > enemy.x
                and enemy.x + self.WIDTH > self.x + 1
                and self.y + self.HEIGHT > enemy.y
                and enemy.y + self.HEIGHT > self.y):
                    is_free += 1

            if is_free == 0:

                self.move_right()

            is_free = 0


    def shoot(self):

        if pyxel.btnr(pyxel.KEY_Z):

            if len(self.bullets) == 0:

                self.sounds.play_sound(0)

                if self.dir == "LEFT" or self.dir == "RIGHT":

                    self.bullet = Bullet(self.x, self.y + 3, self.dir, self.stage, self, False)

                elif self.dir == "UP" or self.dir == "DOWN":

                    self.bullet = Bullet(self.x + 3, self.y, self.dir, self.stage, self, False)

                self.bullets.append(self.bullet)

    
    def bulletMovement(self):

        if self.bullets:

            for bullet in self.bullets:

                if bullet.dir == "LEFT":

                    bullet.left()

                elif bullet.dir == "RIGHT":

                    bullet.right()

                elif bullet.dir == "UP":

                    bullet.up()

                elif bullet.dir == "DOWN":

                    bullet.down()


    def drawPlayer(self):

        if self.state == "INACTIVE":

            self.isGameOver = True
            self.U, self.V = 0, 0

        pyxel.blt(
            self.x, 
            self.y, 
            self.IMG, 
            self.U,
            self.V, 
            self.WIDTH, 
            self.HEIGHT,
            0
        )


    def move_left(self):
        
        new_x = self.x - self.DX
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_x  = tile_x - 1


        if new_x < 8:

            return
        
        next_tile_top = self.stage.stage_map[tile_y][new_tile_x]
        next_tile_bottom = self.stage.stage_map[tile_y + 1][new_tile_x]

        if ((
            (next_tile_top == StageItem.BRICK or next_tile_top == StageItem.CRACKED_BRICK or next_tile_top == StageItem.STONE
            or next_tile_top == StageItem.MIRROR_LEFT  or next_tile_top == StageItem.MIRROR_RIGHT
            or next_tile_top == StageItem.WATER or next_tile_top == StageItem.HEART_OFF or next_tile_top == StageItem.HEART_ON
            or next_tile_top == StageItem.HOME) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == StageItem.BRICK or next_tile_bottom == StageItem.CRACKED_BRICK or next_tile_bottom == StageItem.STONE
            or next_tile_bottom == StageItem.MIRROR_LEFT  or next_tile_bottom == StageItem.MIRROR_RIGHT
            or next_tile_bottom == StageItem.WATER or next_tile_bottom == StageItem.HEART_OFF or next_tile_bottom == StageItem.HEART_ON) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
            )):

            return
        
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = new_x
    

    def move_right(self):
        
        new_x = self.x + self.DX
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_x  = tile_x + 1

        if new_x > 112:

            return

        next_tile_top = self.stage.stage_map[tile_y][new_tile_x]
        next_tile_bottom = self.stage.stage_map[tile_y + 1][new_tile_x]

        if ((
            (next_tile_top == StageItem.BRICK or next_tile_top == StageItem.CRACKED_BRICK or next_tile_top == StageItem.STONE
            or next_tile_top == StageItem.MIRROR_LEFT  or next_tile_top == StageItem.MIRROR_RIGHT
            or next_tile_top == StageItem.WATER or next_tile_top == StageItem.HEART_OFF or next_tile_top == StageItem.HEART_ON
            or next_tile_top == StageItem.HOME) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == StageItem.BRICK or next_tile_bottom == StageItem.CRACKED_BRICK or next_tile_bottom == StageItem.STONE
            or next_tile_bottom == StageItem.MIRROR_LEFT  or next_tile_bottom == StageItem.MIRROR_RIGHT
            or next_tile_bottom == StageItem.WATER or next_tile_bottom == StageItem.HEART_OFF or next_tile_bottom == StageItem.HEART_ON) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
            )):

            return
        
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = new_x


    def move_up(self):

        self.player_img = 0
        self.dir = "UP"
        self.U = 24
        self.V = 8

        new_y = self.y - self.DY
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_y  = tile_y - 1

        if new_y < 8:

            return

        next_tile_top = self.stage.stage_map[new_tile_y][tile_x]
        next_tile_bottom = self.stage.stage_map[new_tile_y][tile_x + 1]

        if ((
            (next_tile_top == StageItem.BRICK or next_tile_top == StageItem.CRACKED_BRICK or next_tile_top == StageItem.STONE or 
            next_tile_top == StageItem.MIRROR_LEFT  or next_tile_top == StageItem.MIRROR_RIGHT
            or next_tile_top == StageItem.WATER or next_tile_top == StageItem.HEART_OFF or next_tile_top == StageItem.HEART_ON
            or next_tile_top == StageItem.HOME) and
            isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == StageItem.BRICK or next_tile_bottom == StageItem.CRACKED_BRICK or next_tile_bottom == StageItem.STONE or
            next_tile_bottom == StageItem.MIRROR_LEFT  or next_tile_bottom == StageItem.MIRROR_RIGHT
            or next_tile_bottom == StageItem.WATER or next_tile_bottom == StageItem.HEART_OFF or next_tile_bottom == StageItem.HEART_ON) and
            isColliding(self.x, new_y, (tile_x+1) * TILE_SIZE, new_tile_y * TILE_SIZE)
            )):

            return
        
        self.prev_x = self.x
        self.prev_y = self.y
        self.y = new_y
    

    def move_down(self):

        self.player_img = 0
        self.dir = "DOWN"
        self.U = 24
        self.V = 0
        self.WIDTH *= 1

        new_y = self.y + self.DY
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_y  = tile_y + 1
        
        if new_y > 112:

            return

        next_tile_top = self.stage.stage_map[new_tile_y][tile_x]
        next_tile_bottom = self.stage.stage_map[new_tile_y][tile_x + 1]

        if ((
            (next_tile_top == StageItem.BRICK or next_tile_top == StageItem.CRACKED_BRICK or next_tile_top == StageItem.STONE
            or next_tile_top == StageItem.MIRROR_LEFT  or next_tile_top == StageItem.MIRROR_RIGHT
            or next_tile_top == StageItem.WATER or next_tile_top == StageItem.HEART_OFF or next_tile_top == StageItem.HEART_ON
            or next_tile_top == StageItem.HOME) and
            isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == StageItem.BRICK or next_tile_bottom == StageItem.CRACKED_BRICK or next_tile_bottom == StageItem.STONE
            or next_tile_bottom == StageItem.MIRROR_LEFT  or next_tile_bottom == StageItem.MIRROR_RIGHT
            or next_tile_bottom == StageItem.WATER or next_tile_bottom == StageItem.HEART_OFF or next_tile_bottom == StageItem.HEART_ON) and
            isColliding(self.x, new_y, (tile_x+1) * TILE_SIZE, new_tile_y * TILE_SIZE)
            )):

            return

        self.prev_x = self.x
        self.prev_y = self.y
        self.y = new_y