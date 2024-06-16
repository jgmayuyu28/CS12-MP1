import pyxel
from bullet import Bullet, drawBullet
from world import World, WorldItem, isColliding, TILE_SIZE, SPRITE_BANK

class Enemy:
    IMG = 0 #image bank
    U = 0 #starting point
    V = 24 #starting point
    WIDTH = 8 #sprite size
    HEIGHT = 8 #sprite size
    DX = 1 #movement change
    DY = 1 #movement change

    def __init__(self, x, y, dir, world): #initial coordinates
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.dir = dir
        self.world = world
        self.bullets = []
        if dir == "LEFT": #INITIAL U, V FOR INITIAL SPRITE
            self.U, self.V = 0, 24
        elif dir == "RIGHT":
            self.U, self.V = 0, 16
        elif dir == "UP":
            self.U, self.V = 8, 24
        else:
            self.U, self.V = 8, 16
        self.state = "ACTIVE"
    
    def enemyMovement(self): #****TO BE REPLACED WITH AI MOVEMENTS (PLEASE FIGURE THIS OUT)
        if pyxel.btn(pyxel.KEY_UP):
            self.move_up()
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.move_down()
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.move_left()
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.move_right()

    #44 TO 68 ARE METHODS FOR ENEMY BULLETS (SAME ADJUSTMENTS WILL BE MADE TO PLAYER CLASS)

    def shootBullets(self):
        if pyxel.btnr(pyxel.KEY_E):
            self.bullet = Bullet(self.x, self.y, self.dir, self.world)
            self.bullets.append(self.bullet)

    def drawBullets(self):
        if self.bullets:
            new_bullets = []
            for bullet in self.bullets:
                if bullet.state == "ACTIVE":
                    drawBullet(pyxel, bullet)
                    new_bullets.append(bullet)
            self.bullets = new_bullets
    
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

    #MOVEMENT METHODS; SAME AS PLAYER CLASS'
    
    def move_left(self):
        self.dir = "LEFT"
        self.U = 0
        self.V = 24
        
        new_x = self.x - self.DX
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_x  = tile_x - 1

        if new_x < 8: #collision with left border
            return
        
        next_tile_top = self.world.world_map[tile_y][new_tile_x]
        next_tile_bottom = self.world.world_map[tile_y + 1][new_tile_x]
        
        if ((
            (next_tile_top == WorldItem.BRICK or next_tile_top == WorldItem.STONE
            or next_tile_top == WorldItem.MIRROR_LEFT  or next_tile_top == WorldItem.MIRROR_RIGHT) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == WorldItem.BRICK or next_tile_bottom == WorldItem.STONE
            or next_tile_bottom == WorldItem.MIRROR_LEFT  or next_tile_bottom == WorldItem.MIRROR_RIGHT) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
            )) or ((next_tile_top != WorldItem.OPEN and isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE
            )) or (next_tile_bottom != WorldItem.OPEN and isColliding(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE))):
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

        if new_x > 112: #collision with right border
            return

        next_tile_top = self.world.world_map[tile_y][new_tile_x]
        next_tile_bottom = self.world.world_map[tile_y + 1][new_tile_x]

        if ((
            (next_tile_top == WorldItem.BRICK or next_tile_top == WorldItem.STONE
            or next_tile_top == WorldItem.MIRROR_LEFT  or next_tile_top == WorldItem.MIRROR_RIGHT) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == WorldItem.BRICK or next_tile_bottom == WorldItem.STONE
            or next_tile_bottom == WorldItem.MIRROR_LEFT  or next_tile_bottom == WorldItem.MIRROR_RIGHT) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
            )) or ((next_tile_top != WorldItem.OPEN and isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE
            )) or (next_tile_bottom != WorldItem.OPEN and isColliding(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE))):
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

        if new_y < 8: #collision with top border
            return

        next_tile_top = self.world.world_map[new_tile_y][tile_x]
        next_tile_bottom = self.world.world_map[new_tile_y][tile_x + 1]

        if ((
            (next_tile_top == WorldItem.BRICK or next_tile_top == WorldItem.STONE or 
            next_tile_top == WorldItem.MIRROR_LEFT  or next_tile_top == WorldItem.MIRROR_RIGHT) and
            isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == WorldItem.BRICK or next_tile_bottom == WorldItem.STONE or
            next_tile_bottom == WorldItem.MIRROR_LEFT  or next_tile_bottom == WorldItem.MIRROR_RIGHT) and
            isColliding(self.x, new_y, (tile_x+1) * TILE_SIZE, new_tile_y * TILE_SIZE)
            )) or ((next_tile_top != WorldItem.OPEN and isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE
            )) or (next_tile_bottom != WorldItem.OPEN and isColliding(self.x, new_y, (tile_x + 1) * TILE_SIZE, new_tile_y * TILE_SIZE))):
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

        next_tile_top = self.world.world_map[new_tile_y][tile_x]
        next_tile_bottom = self.world.world_map[new_tile_y][tile_x + 1]

        if ((
            (next_tile_top == WorldItem.BRICK or next_tile_top == WorldItem.STONE
            or next_tile_top == WorldItem.MIRROR_LEFT  or next_tile_top == WorldItem.MIRROR_RIGHT) and
            isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == WorldItem.BRICK or next_tile_bottom == WorldItem.STONE
            or next_tile_bottom == WorldItem.MIRROR_LEFT  or next_tile_bottom == WorldItem.MIRROR_RIGHT) and
            isColliding(self.x, new_y, (tile_x+1) * TILE_SIZE, new_tile_y * TILE_SIZE)
            )) or ((next_tile_top != WorldItem.OPEN and isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE
            )) or (next_tile_bottom != WorldItem.OPEN and isColliding(self.x, new_y, (tile_x + 1) * TILE_SIZE, new_tile_y * TILE_SIZE))):
            return

        self.prev_x = self.x
        self.prev_y = self.y
        self.y = new_y

#DRAW ENEMY FUNCTION (NOT INCLUDED IN ENEMY CLASS!!)

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
    8
)