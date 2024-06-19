TILE_SIZE = 8
SPRITE_SIZE = 8
SPRITE_BANK = 0

class WorldItem: #ASSIGNS EACH CELL OF TILEMAP THE COORDINATES OF AN ITEM FROM THE SPRITE BANK
    BRICK = (1, 0)
    STONE = (4, 0)
    MIRROR_LEFT = (5, 0)
    MIRROR_RIGHT = (5, 1)
    OPEN = (0, 0)
    PLAYER = (10, 0)
    PLAYER_D = (9, 0)
    ENEMY = (0, 2)
    ENEMY_D = (0, 6)
    CRACKED_BRICK = (5,2) # PHASE 2
    WATER = (3,2) # PHASE 2
    SPAWNER = (1,4) # PHASE 2
    HOME = (3,4) # PHASE 3

    
class World:
    HEIGHT = 16
    WIDTH = 16

    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.world_map = [] #STORES THE ITEM SET ON EACH TILEMAP CELL (TILEMAP SIZE = 16 BY 16)
        for y in range(self.HEIGHT): #
            self.world_map.append([])
            for x in range(self.WIDTH):
                if self.tilemap.pget(x, y) == WorldItem.BRICK:
                    self.world_map[y].append(WorldItem.BRICK)
                elif self.tilemap.pget(x, y) == WorldItem.STONE:
                    self.world_map[y].append(WorldItem.STONE)
                elif self.tilemap.pget(x, y) == WorldItem.MIRROR_LEFT:
                    self.world_map[y].append(WorldItem.MIRROR_LEFT)
                elif self.tilemap.pget(x, y) == WorldItem.MIRROR_RIGHT:
                    self.world_map[y].append(WorldItem.MIRROR_RIGHT)
                elif self.tilemap.pget(x, y) == WorldItem.ENEMY:
                    self.world_map[y].append(WorldItem.ENEMY)
                elif self.tilemap.pget(x, y) == WorldItem.PLAYER:
                    self.world_map[y].append(WorldItem.PLAYER)
                elif self.tilemap.pget(x, y) == WorldItem.CRACKED_BRICK: # PHASE 2
                    self.world_map[y].append(WorldItem.CRACKED_BRICK)
                elif self.tilemap.pget(x, y) == WorldItem.WATER: # PHASE 2
                    self.world_map[y].append(WorldItem.WATER)
                elif self.tilemap.pget(x, y) == WorldItem.SPAWNER: # PHASE 2
                    self.world_map[y].append(WorldItem.SPAWNER)
                elif self.tilemap.pget(x, y) == WorldItem.HOME: # PHASE 3
                    self.world_map[y].append(WorldItem.HOME)
                else:
                    self.world_map[y].append(WorldItem.OPEN)

    def clear(self, x, y): #clears an obstacle
        self.tilemap.pset(x, y, WorldItem.OPEN)
        self.world_map[y][x] = WorldItem.OPEN

    def set(self, x, y, worldItem): #REPLACES AN ITEM OF A TILEMAP WITH ANOTHER (PARAMS: X - TILE COORDINATE, Y - TILE COORDINATE, ITEM (ex. WorldItem.STONE))
        self.tilemap.pset(x, y, worldItem)
        self.world_map[y][x] = worldItem

#DRAWS THE STAGE (NOT PART OF WORLD CLASS; USED/IMPORTED IN MAIN FILE)

def world_item_draw(pyxel, x, y, world_item):
    if world_item == WorldItem.ENEMY:
        u, v = 0, 0
    else:
        u, v = world_item[0], world_item[1]
    pyxel.blt(
        x * TILE_SIZE,
        y * TILE_SIZE,
        SPRITE_BANK,
        u * TILE_SIZE,
        v * TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE
    )

#COLLISION LOGIC (NOT PART OF WORLD CLASS; USED/IMPORTED IN PLAYER, BULLET, AND ENEMY FILES)

def isColliding(x1, y1, x2, y2):

    if x1 + SPRITE_SIZE <= x2 or x2 + SPRITE_SIZE <= x1:
        return False
    
    if y1 + SPRITE_SIZE <= y2 or y2 + SPRITE_SIZE <= y1:
        return False
    return True
