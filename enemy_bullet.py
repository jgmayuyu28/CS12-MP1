import pyxel
from world_copy import WorldItem, TILE_SIZE, SPRITE_BANK, isColliding
from player_copy import Player

class EnemyBullet:
    def __init__(self, x, y, dir, world, player):
        self.x = x
        self.y = y
        self.dir = dir #IF TOWARS LEFT, RIGHT, UP, OR DOWN
        self.world = world
        self.player = player
        self.state = "ACTIVE" #ACTIVE AKA VISIBLE; INACTIVE AKA VANISHED

    #INCLUDES LOGIC FOR A BULLET HITTING STONE, BRICK, MIRROR CELLS, AS WELL AS ENEMY TANKS
    # NOT YET INCLUDED: LOGIC FOR COLLISION WITH ENEMY BULLETS 


    def left(self):
        new_x = (self.x - 3) % pyxel.width
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_x  = tile_x - 1

        next_tile_top = self.world.world_map[tile_y][new_tile_x]
        next_tile_bottom = self.world.world_map[tile_y + 1][new_tile_x]

        # ADDED LOGIC FOR BRICK AND CRACKED BRICK (ALREADY ADDED IN RIGHT, UP, AND DOWN
        if (
            (next_tile_top == WorldItem.BRICK or next_tile_top == WorldItem.STONE or next_tile_top == WorldItem.CRACKED_BRICK
            or next_tile_top == WorldItem.MIRROR_LEFT  or next_tile_top == WorldItem.MIRROR_RIGHT or next_tile_top == WorldItem.PLAYER) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == WorldItem.BRICK or next_tile_bottom == WorldItem.STONE or next_tile_bottom == WorldItem.CRACKED_BRICK
            or next_tile_bottom == WorldItem.MIRROR_LEFT  or next_tile_bottom == WorldItem.MIRROR_RIGHT or next_tile_bottom == WorldItem.PLAYER) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)):
            if next_tile_top == WorldItem.BRICK:
                self.state = "INACTIVE" #VANISHES ITSELF
                self.world.set(new_tile_x, tile_y, WorldItem.CRACKED_BRICK) #FUNCTION IMPORTED FROM WORLD FILE; LOGIC FOR BRICK DISAPPEARING WHEN BULLET HITS
                return
            elif next_tile_bottom == WorldItem.BRICK:
                self.state = "INACTIVE" #VANISHES ITSELF
                self.world.set(new_tile_x, tile_y + 1, WorldItem.CRACKED_BRICK) #FUNCTION IMPORTED FROM WORLD FILE; LOGIC FOR BRICK DISAPPEARING WHEN BULLET HITS
                return
            elif next_tile_top == WorldItem.CRACKED_BRICK:
                self.state = "INACTIVE" #VANISHES ITSELF
                self.world.set(new_tile_x, tile_y, WorldItem.OPEN)
                return
            elif next_tile_bottom == WorldItem.CRACKED_BRICK:
                self.state = "INACTIVE"
                self.world.set(new_tile_x, tile_y + 1, WorldItem.OPEN)
                return
            elif next_tile_top == WorldItem.MIRROR_LEFT:
                self.state = "ACTIVE"
                self.dir = "DOWN"
                self.x, self.y = new_tile_x * TILE_SIZE, tile_y * TILE_SIZE #LOGIC FOR MIRROR CELL WHEN BULLET HITS
            elif next_tile_bottom == WorldItem.MIRROR_RIGHT:
                self.state = "ACTIVE"
                self.dir = "UP"
                self.x, self.y = new_tile_x * TILE_SIZE, tile_y * TILE_SIZE #LOGIC FOR MIRROR CELL WHEN BULLET HITS
            elif next_tile_top == WorldItem.MIRROR_LEFT:
                self.state = "ACTIVE"
                self.dir = "DOWN"
                self.x, self.y = new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE #LOGIC FOR MIRROR CELL WHEN BULLET HITS
            elif next_tile_bottom == WorldItem.MIRROR_RIGHT:
                self.state = "ACTIVE"
                self.dir = "UP"
                self.x, self.y = new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE #LOGIC FOR MIRROR CELL WHEN BULLET HITS
                
            elif next_tile_top == WorldItem.STONE:
                self.state = "INACTIVE"
                return
            elif next_tile_bottom == WorldItem.STONE:
                self.state = "INACTIVE"
                return
            elif next_tile_top == WorldItem.PLAYER:
                self.player.state = "INACTIVE" #FUNCTION IMPORTED FROM WORLD FILE; LOGIC FOR ENEMY DYING WHEN BULLET HITS; THE CELL IS ASSIGNED THE ENEMY_D ITEM AND IS CONNECTED TO THE enemyHit() METHOD IN THE MAIN FILE
                self.state = "INACTIVE"
                return
            elif next_tile_bottom == WorldItem.PLAYER:
                self.player.state = "INACTIVE" #FUNCTION IMPORTED FROM WORLD FILE; LOGIC FOR ENEMY DYING WHEN BULLET HITS; THE CELL IS ASSIGNED THE ENEMY_D ITEM AND IS CONNECTED TO THE enemyHit() METHOD IN THE MAIN FILE
                self.state = "INACTIVE"
                return
        
        #SAME LOGIC FOR THER EST OF THE DIRECTIONS

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
        new_x = (self.x + 3) % pyxel.width
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_x  = tile_x + 1

        next_tile_top = self.world.world_map[tile_y][new_tile_x]
        next_tile_bottom = self.world.world_map[tile_y + 1][new_tile_x]

        if (
            (next_tile_top == WorldItem.BRICK or next_tile_top == WorldItem.STONE or next_tile_top == WorldItem.CRACKED_BRICK
            or next_tile_top == WorldItem.MIRROR_LEFT  or next_tile_top == WorldItem.MIRROR_RIGHT or next_tile_top == WorldItem.PLAYER) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == WorldItem.BRICK or next_tile_bottom == WorldItem.STONE or next_tile_bottom == WorldItem.CRACKED_BRICK
            or next_tile_bottom == WorldItem.MIRROR_LEFT  or next_tile_bottom == WorldItem.MIRROR_RIGHT or next_tile_bottom == WorldItem.PLAYER) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)):
            if next_tile_top == WorldItem.BRICK:
                self.state = "INACTIVE" #VANISHES ITSELF
                self.world.set(new_tile_x, tile_y, WorldItem.CRACKED_BRICK)
                return
            elif next_tile_bottom == WorldItem.BRICK:
                self.state = "INACTIVE" #VANISHES ITSELF
                self.world.set(new_tile_x, tile_y + 1, WorldItem.CRACKED_BRICK)
                return
            elif next_tile_top == WorldItem.CRACKED_BRICK:
                self.state = "INACTIVE"
                self.world.clear(new_tile_x, tile_y)
                return
            elif next_tile_bottom == WorldItem.CRACKED_BRICK:
                self.state = "INACTIVE"
                self.world.clear(new_tile_x, tile_y + 1)
                return
            elif next_tile_top == WorldItem.MIRROR_LEFT:
                self.state = "ACTIVE"
                self.dir = "UP"
                self.x, self.y = new_tile_x * TILE_SIZE, tile_y * TILE_SIZE
            elif next_tile_bottom == WorldItem.MIRROR_RIGHT:
                self.state = "ACTIVE"
                self.dir = "DOWN"
                self.x, self.y = new_tile_x * TILE_SIZE, tile_y * TILE_SIZE
            elif next_tile_top == WorldItem.MIRROR_LEFT:
                self.state = "ACTIVE"
                self.dir = "UP"
                self.x, self.y = new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE
            elif next_tile_bottom == WorldItem.MIRROR_RIGHT:
                self.state = "ACTIVE"
                self.dir = "DOWN"
                self.x, self.y = new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE
            elif next_tile_top == WorldItem.STONE:
                self.state = "INACTIVE"
                return
            elif next_tile_bottom == WorldItem.STONE:
                self.state = "INACTIVE"
                return
            elif next_tile_top == WorldItem.PLAYER:
                self.player.state = "INACTIVE"
                self.state = "INACTIVE"
                return
            elif next_tile_bottom == WorldItem.PLAYER:
                self.player.state = "INACTIVE"
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
        new_y = (self.y - 3) % pyxel.width
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_y  = tile_y - 1

        next_tile_top = self.world.world_map[new_tile_y][tile_x]
        next_tile_bottom = self.world.world_map[new_tile_y][tile_x + 1]

        if (
            (next_tile_top == WorldItem.BRICK or next_tile_top == WorldItem.STONE or next_tile_top == WorldItem.CRACKED_BRICK
            or next_tile_top == WorldItem.MIRROR_LEFT  or next_tile_top == WorldItem.MIRROR_RIGHT or next_tile_top == WorldItem.PLAYER) and
            isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == WorldItem.BRICK or next_tile_bottom == WorldItem.STONE or next_tile_bottom == WorldItem.CRACKED_BRICK
            or next_tile_bottom == WorldItem.MIRROR_LEFT  or next_tile_bottom == WorldItem.MIRROR_RIGHT or next_tile_bottom == WorldItem.PLAYER) and
            isColliding(self.x, new_y, (tile_x+1) * TILE_SIZE, new_tile_y * TILE_SIZE)):
            if next_tile_top == WorldItem.BRICK:
                self.state = "INACTIVE" #VANISHES ITSELF
                self.world.set(tile_x, new_tile_y, WorldItem.CRACKED_BRICK)
                return
            elif next_tile_bottom == WorldItem.BRICK:
                self.state = "INACTIVE" #VANISHES ITSELF
                self.world.set(tile_x + 1, new_tile_y, WorldItem.CRACKED_BRICK)
                return
            elif next_tile_top == WorldItem.CRACKED_BRICK:
                self.state = "INACTIVE"
                self.world.clear(tile_x, new_tile_y)
                return
            elif next_tile_bottom == WorldItem.CRACKED_BRICK:
                self.state = "INACTIVE"
                self.world.clear(tile_x + 1, new_tile_y) #FUNCTION IMPORTED FROM WORLD FILE; LOGIC FOR BRICK DISAPPEARING WHEN BULLET HITS
                return
            elif next_tile_top == WorldItem.MIRROR_LEFT:
                self.state = "ACTIVE"
                self.dir = "RIGHT"
                self.x, self.y = tile_x * TILE_SIZE, new_tile_y * TILE_SIZE
            elif next_tile_bottom == WorldItem.MIRROR_RIGHT:
                self.state = "ACTIVE"
                self.dir = "LEFT"
                self.x, self.y = tile_x * TILE_SIZE, new_tile_y * TILE_SIZE
            elif next_tile_top == WorldItem.MIRROR_LEFT:
                self.state = "ACTIVE"
                self.dir = "RIGHT"
                self.x, self.y = (tile_x + 1) * TILE_SIZE, new_tile_y * TILE_SIZE
            elif next_tile_bottom == WorldItem.MIRROR_RIGHT:
                self.state = "ACTIVE"
                self.dir = "LEFT"
                self.x, self.y = (tile_x + 1) * TILE_SIZE, new_tile_y * TILE_SIZE
            elif next_tile_top == WorldItem.STONE:
                self.state = "INACTIVE"
                return
            elif next_tile_bottom == WorldItem.STONE:
                self.state = "INACTIVE"
                return
            elif next_tile_top == WorldItem.PLAYER:
                self.player.state = "INACTIVE"
                self.state = "INACTIVE"
                return
            elif next_tile_bottom == WorldItem.PLAYER:
                self.player.state = "INACTIVE"
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
        new_y = (self.y + 3) % pyxel.width
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_y  = tile_y + 1

        next_tile_top = self.world.world_map[new_tile_y][tile_x]
        next_tile_bottom = self.world.world_map[new_tile_y][tile_x + 1]

        if (
            (next_tile_top == WorldItem.BRICK or next_tile_top == WorldItem.STONE or next_tile_top == WorldItem.CRACKED_BRICK
            or next_tile_top == WorldItem.MIRROR_LEFT  or next_tile_top == WorldItem.MIRROR_RIGHT or next_tile_top == WorldItem.PLAYER) and
            isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == WorldItem.BRICK or next_tile_bottom == WorldItem.STONE or next_tile_bottom == WorldItem.CRACKED_BRICK
            or next_tile_bottom == WorldItem.MIRROR_LEFT  or next_tile_bottom == WorldItem.MIRROR_RIGHT or next_tile_bottom == WorldItem.PLAYER) and
            isColliding(self.x, new_y, (tile_x+1) * TILE_SIZE, new_tile_y * TILE_SIZE)):
            if next_tile_top == WorldItem.BRICK:
                self.state = "INACTIVE" #VANISHES ITSELF
                self.world.set(tile_x, tile_y + 1, WorldItem.CRACKED_BRICK)
                return
            elif next_tile_bottom == WorldItem.BRICK:
                self.state = "INACTIVE" #VANISHES ITSELF
                self.world.set(tile_x + 1, new_tile_y, WorldItem.CRACKED_BRICK)
                return
            elif next_tile_top == WorldItem.CRACKED_BRICK:
                self.state = "INACTIVE"
                self.world.clear(tile_x, new_tile_y)
                return
            elif next_tile_bottom == WorldItem.CRACKED_BRICK:
                self.state = "INACTIVE"
                self.world.clear(tile_x + 1, new_tile_y) #FUNCTION IMPORTED FROM WORLD FILE; LOGIC FOR BRICK DISAPPEARING WHEN BULLET HITS
                return
            elif next_tile_top == WorldItem.MIRROR_LEFT:
                self.state = "ACTIVE"
                self.dir = "LEFT"
                self.x, self.y = tile_x * TILE_SIZE, new_tile_y * TILE_SIZE
            elif next_tile_bottom == WorldItem.MIRROR_RIGHT:
                self.state = "ACTIVE"
                self.dir = "RIGHT"
                self.x, self.y = tile_x * TILE_SIZE, new_tile_y * TILE_SIZE
            elif next_tile_top == WorldItem.MIRROR_LEFT:
                self.state = "ACTIVE"
                self.dir = "LEFT"
                self.x, self.y = (tile_x + 1) * TILE_SIZE, new_tile_y * TILE_SIZE
            elif next_tile_bottom == WorldItem.MIRROR_RIGHT:
                self.state = "ACTIVE"
                self.dir = "RIGHT"
                self.x, self.y = (tile_x + 1) * TILE_SIZE, new_tile_y * TILE_SIZE
            elif next_tile_top == WorldItem.STONE:
                self.state = "INACTIVE"
                return
            elif next_tile_bottom == WorldItem.STONE:
                self.state = "INACTIVE"
                return
            elif next_tile_top == WorldItem.PLAYER:
                self.player.state = "INACTIVE"
                self.state = "INACTIVE"
                return
            elif next_tile_bottom == WorldItem.PLAYER:
                self.player.state = "INACTIVE"
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

#DRAWS THE BULLET (NOT PART OF BULLET CLASS; USED IN MAIN FILE)

def drawBullet(pyxel, bullet):
    U, V = 0, 0

    if bullet.dir == "LEFT":
        U, V = 64, 8
    elif bullet.dir == "RIGHT":
        U, V = 64, 0
    elif bullet.dir == "UP":
        U, V = 56, 8
    elif bullet.dir == "DOWN":
        U, V = 56, 0

    pyxel.blt(
    bullet.x,
    bullet.y,
    SPRITE_BANK,
    U,
    V,
    8,
    8
)