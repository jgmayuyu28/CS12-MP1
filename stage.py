TILE_SIZE = 8
SPRITE_SIZE = 8
SPRITE_BANK = 0

class StageItem: 

    BRICK = (1, 0)
    STONE = (4, 0)
    MIRROR_LEFT = (5, 0)
    MIRROR_RIGHT = (5, 1)
    OPEN = (0, 0)
    CRACKED_BRICK = (1, 1)
    SPAWNER = (1, 4)
    WATER = (3, 2)
    FOREST = (2, 2) #forest

class Stage:

    HEIGHT = 16
    WIDTH = 16


    def __init__(self, tilemap):
        
        self.tilemap = tilemap
        self.stage_map = [] 

        for y in range(self.HEIGHT): 

            self.stage_map.append([])

            for x in range(self.WIDTH):

                if self.tilemap.pget(x, y) == StageItem.BRICK:

                    self.stage_map[y].append(StageItem.BRICK)

                elif self.tilemap.pget(x, y) == StageItem.STONE:

                    self.stage_map[y].append(StageItem.STONE)

                elif self.tilemap.pget(x, y) == StageItem.MIRROR_LEFT:

                    self.stage_map[y].append(StageItem.MIRROR_LEFT)

                elif self.tilemap.pget(x, y) == StageItem.MIRROR_RIGHT:

                    self.stage_map[y].append(StageItem.MIRROR_RIGHT)

                elif self.tilemap.pget(x, y) == StageItem.CRACKED_BRICK:

                    self.stage_map[y].append(StageItem.CRACKED_BRICK)

                elif self.tilemap.pget(x, y) == StageItem.WATER:

                    self.stage_map[y].append(StageItem.WATER)

                elif self.tilemap.pget(x, y) == StageItem.SPAWNER:

                    self.stage_map[y].append(StageItem.SPAWNER)

                elif self.tilemap.pget(x, y) == StageItem.FOREST:

                    self.stage_map[y].append(StageItem.FOREST)

                else:

                    self.stage_map[y].append(StageItem.OPEN)


    def clear(self, x, y):

        self.tilemap.pset(x, y, StageItem.OPEN)
        self.stage_map[y][x] = StageItem.OPEN


    def set(self, x, y, stageItem): 

        self.tilemap.pset(x, y, stageItem)
        self.stage_map[y][x] = stageItem


def stage_item_draw(pyxel, x, y, stage_item):

    u, v = stage_item[0], stage_item[1]
    
    pyxel.blt(
        x * TILE_SIZE,
        y * TILE_SIZE,
        SPRITE_BANK,
        u * TILE_SIZE,
        v * TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE,
        0
    )


def isColliding(x1, y1, x2, y2):

    if x1 + SPRITE_SIZE <= x2 or x2 + SPRITE_SIZE <= x1:

        return False
    
    if y1 + SPRITE_SIZE <= y2 or y2 + SPRITE_SIZE <= y1:

        return False
    
    return True