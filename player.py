from world_copy import World, WorldItem, isColliding, TILE_SIZE

class Player:
    IMG = 0 #image bank
    U = 16 #starting point
    V = 0 #starting point
    WIDTH = 8 #sprite size
    HEIGHT = 8 #sprite size
    DX = 1 #movement change
    DY = 1 #movement change

    def __init__(self, world): #initial coordinates
        self.x = 8
        self.y = 8
        self.prev_x = self.x
        self.prev_y = self.y
        self.dir = "DOWN"
        self.world = world
        self.state = "ACTIVE"

    # ADDED LOGIC FOR WATER FOR ALL DIRECTIONS
    def move_left(self):
        self.player_img = 0
        self.dir = "LEFT"
        self.U = 16
        self.V = 8
        
        new_x = self.x - self.DX
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        new_tile_x  = tile_x - 1

        #31 TO 49 CHECKS FOR COLLISIONS WITH ITEMS OR ENEMY TANKS

        if new_x < 8: #collision with left border
            return
        
        next_tile_top = self.world.world_map[tile_y][new_tile_x]
        next_tile_bottom = self.world.world_map[tile_y + 1][new_tile_x]

        if ((
            (next_tile_top == WorldItem.BRICK or next_tile_top == WorldItem.STONE
            or next_tile_top == WorldItem.MIRROR_LEFT  or next_tile_top == WorldItem.MIRROR_RIGHT or next_tile_top == WorldItem.WATER) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == WorldItem.BRICK or next_tile_bottom == WorldItem.STONE
            or next_tile_bottom == WorldItem.MIRROR_LEFT  or next_tile_bottom == WorldItem.MIRROR_RIGHT or next_tile_bottom == WorldItem.WATER) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
            )) or ((next_tile_top != WorldItem.OPEN and isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE
            )) or (next_tile_bottom != WorldItem.OPEN and isColliding(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE))):
            return
        
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = new_x
    
    def move_right(self):
        self.player_img = 0
        self.dir = "RIGHT"
        self.U = 16
        self.V = 0
        
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
            or next_tile_top == WorldItem.MIRROR_LEFT  or next_tile_top == WorldItem.MIRROR_RIGHT or next_tile_top == WorldItem.WATER) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == WorldItem.BRICK or next_tile_bottom == WorldItem.STONE
            or next_tile_bottom == WorldItem.MIRROR_LEFT  or next_tile_bottom == WorldItem.MIRROR_RIGHT or next_tile_bottom == WorldItem.WATER) and
            isColliding(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
            )) or ((next_tile_top != WorldItem.OPEN and isColliding(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)) or (next_tile_bottom != WorldItem.OPEN and isColliding(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE))):
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

        if new_y < 8: #collision with top border
            return

        next_tile_top = self.world.world_map[new_tile_y][tile_x]
        next_tile_bottom = self.world.world_map[new_tile_y][tile_x + 1]

        if ((
            (next_tile_top == WorldItem.BRICK or next_tile_top == WorldItem.STONE or 
            next_tile_top == WorldItem.MIRROR_LEFT  or next_tile_top == WorldItem.MIRROR_RIGHT or next_tile_top == WorldItem.WATER) and
            isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == WorldItem.BRICK or next_tile_bottom == WorldItem.STONE or
            next_tile_bottom == WorldItem.MIRROR_LEFT  or next_tile_bottom == WorldItem.MIRROR_RIGHT or next_tile_bottom == WorldItem.WATER) and
            isColliding(self.x, new_y, (tile_x+1) * TILE_SIZE, new_tile_y * TILE_SIZE)
            )) or ((next_tile_top != WorldItem.OPEN and isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)) or (next_tile_bottom != WorldItem.OPEN and isColliding(self.x, new_y, (tile_x + 1) * TILE_SIZE, new_tile_y * TILE_SIZE))):
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

        next_tile_top = self.world.world_map[new_tile_y][tile_x]
        next_tile_bottom = self.world.world_map[new_tile_y][tile_x + 1]

        if ((
            (next_tile_top == WorldItem.BRICK or next_tile_top == WorldItem.STONE
            or next_tile_top == WorldItem.MIRROR_LEFT  or next_tile_top == WorldItem.MIRROR_RIGHT or next_tile_top == WorldItem.WATER) and
            isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ) or (
            (next_tile_bottom == WorldItem.BRICK or next_tile_bottom == WorldItem.STONE
            or next_tile_bottom == WorldItem.MIRROR_LEFT  or next_tile_bottom == WorldItem.MIRROR_RIGHT or next_tile_bottom == WorldItem.WATER) and
            isColliding(self.x, new_y, (tile_x+1) * TILE_SIZE, new_tile_y * TILE_SIZE)
            )) or ((next_tile_top != WorldItem.OPEN and isColliding(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)) or (next_tile_bottom != WorldItem.OPEN and isColliding(self.x, new_y, (tile_x + 1) * TILE_SIZE, new_tile_y * TILE_SIZE))):
            return

        self.prev_x = self.x
        self.prev_y = self.y
        self.y = new_y