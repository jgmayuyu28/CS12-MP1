import random
import pyxel
from bullet import Bullet, drawBullet
from stage import Stage, StageItem, isColliding, TILE_SIZE, SPRITE_BANK

class Enemy:

    IMG = 0
    U = 0 
    V = 24 
    WIDTH = 8 
    HEIGHT = 8
    DX = 1 
    DY = 1 


    def __init__(self, x, y, dir, stage, player, enemies):

        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.stage = stage
        self.dir = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.movement_countdown = random.randint(3, 5)
        self.bullets = []
        self.bullet_countdown = random.randint(1, 3)
        self.player = player
        self.enemies = enemies

        if dir == "LEFT":

            self.U, self.V = 0, 24

        elif dir == "RIGHT":

            self.U, self.V = 0, 16

        elif dir == "UP":

            self.U, self.V = 8, 24

        else:

            self.U, self.V = 8, 16

        self.state = "ACTIVE"
    

    def enemyBehavior(self):

        self.enemyMovement()
        self.shootBullets()
        self.bulletMovement()


    def enemyMovement(self): 

        is_free = 0

        if self.dir == "UP":

            for enemy in self.enemies:

                if (self.x + self.WIDTH > enemy.x
                and enemy.x + self.WIDTH > self.x
                and (self.y - 1) + self.HEIGHT > enemy.y
                and enemy.y + self.HEIGHT > self.y - 1
                ) and (self.x != enemy.x):
                    
                    is_free += 1

            if is_free == 0:

                self.move_up()

            is_free = 0

        elif self.dir == "DOWN":

            for enemy in self.enemies:
                
                if (self.x + self.WIDTH > enemy.x
                and enemy.x + self.WIDTH > self.x
                and (self.y + 1) + self.HEIGHT > enemy.y
                and enemy.y + self.HEIGHT > self.y + 1
                ) and (self.x != enemy.x):
                    
                    is_free += 1

            if is_free == 0:

                self.move_down()

            is_free = 0

        elif self.dir == "LEFT":

            for enemy in self.enemies:
                if ((self.x - 1) + self.WIDTH > enemy.x
                and enemy.x + self.WIDTH > self.x - 1
                and self.y + self.HEIGHT > enemy.y
                and enemy.y + self.HEIGHT > self.y
                ) and (self.x != enemy.x):
                    
                    is_free += 1

            if is_free == 0:

                self.move_left()

            is_free = 0

        elif self.dir == "RIGHT":

            for enemy in self.enemies:
                if ((self.x + 1) + self.WIDTH > enemy.x
                and enemy.x + self.WIDTH > self.x + 1
                and self.y + self.HEIGHT > enemy.y
                and enemy.y + self.HEIGHT > self.y
                ) and (self.x != enemy.x):
                    
                    is_free += 1

            if is_free == 0:

                self.move_right()

            is_free = 0

        self.movement_countdown  -= 0.1

        if self.movement_countdown <= 0:

            self.dir = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            self.movement_countdown  = random.randint(4,8)


    def shootBullets(self):

        self.bullet_countdown -= 0.1

        if self.bullet_countdown <= 0:

            self.bullet = Bullet(self.x + 3, self.y + 3, self.dir, self.stage, self.player, True)
            self.bullets.append(self.bullet)
            self.bullet_countdown = random.randint(4, 8)
    

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


    def drawBullets(self):

        if self.bullets:
            
            new_bullets = []

            for bullet in self.bullets:

                if bullet.state == "ACTIVE":

                    drawBullet(pyxel, bullet)
                    new_bullets.append(bullet)

            self.bullets = new_bullets

    
    def move_left(self):

        self.dir = "LEFT"
        self.U = 0
        self.V = 24
        
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
            )
        ) or (self.player.x + self.player.WIDTH > new_x
            and new_x + self.WIDTH > self.player.x
            and self.player.y + self.player.HEIGHT > self.y
            and self.y + self.HEIGHT > self.player.y):

            return
        
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = new_x
    

    def move_right(self):

        self.dir = "RIGHT"
        self.U = 0
        self.V = 16
        
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
            )
        ) or (self.player.x + self.player.WIDTH > new_x
            and new_x + self.WIDTH > self.player.x
            and self.player.y + self.player.HEIGHT > self.y
            and self.y + self.HEIGHT > self.player.y):

            return
        
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = new_x


    def move_up(self):

        self.dir = "UP"
        self.U = 8
        self.V = 24

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
            )
        ) or (self.player.x + self.player.WIDTH > self.x
            and self.x + self.WIDTH > self.player.x
            and self.player.y + self.player.HEIGHT > new_y
            and new_y + self.HEIGHT > self.player.y):

            return
        
        self.prev_x = self.x
        self.prev_y = self.y
        self.y = new_y
    

    def move_down(self):

        self.dir = "DOWN"
        self.U = 8
        self.V = 16
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
            )
        ) or (self.player.x + self.player.WIDTH > self.x
            and self.x + self.WIDTH > self.player.x
            and self.player.y + self.player.HEIGHT > new_y
            and new_y + self.HEIGHT > self.player.y):

            return

        self.prev_x = self.x
        self.prev_y = self.y
        self.y = new_y


def drawEnemy(pyxel, enemy):
    
    U, V = 0, 0

    if enemy.dir == "LEFT":

        U, V = 0, 24

    elif enemy.dir == "RIGHT":

        U, V = 0, 16

    elif enemy.dir == "UP":

        U, V = 8, 24

    elif enemy.dir == "DOWN":

        U, V = 8, 16

    pyxel.blt(
    enemy.x,
    enemy.y,
    SPRITE_BANK,
    U,
    V,
    8,
    8, 
    0
)