import csv

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
    HOME = (3,3)
    FOREST = (2, 2) 
    HEART_ON = (1, 5)
    HEART_OFF = (1, 6)

class Stage:

    HEIGHT = 16
    WIDTH = 16
    HOME = (6, 14)

    def __init__(self, stage_no, file_name):

        self.file_name = file_name
        self.stages = []
        self.max_spawn_per_stage = []

        self.load_file()

        self.stage_no = stage_no
        self.player_x = 0
        self.player_y = 0
        
        self.stage_map = [] 

        for y in range(self.HEIGHT): 

            self.stage_map.append([])

            for x in range(self.WIDTH):

                if self.stages[self.stage_no][y][x] == "PLAYER":

                    self.stage_map[y].append(StageItem.OPEN)
                    self.player_x, self.player_y = x, y

                elif self.stages[self.stage_no][y][x] == "BRICK":

                    self.stage_map[y].append(StageItem.BRICK)

                elif self.stages[self.stage_no][y][x] == "STONE":

                    self.stage_map[y].append(StageItem.STONE)

                elif self.stages[self.stage_no][y][x] == "MIRROR_LEFT":

                    self.stage_map[y].append(StageItem.MIRROR_LEFT)

                elif self.stages[self.stage_no][y][x] == "MIRROR_RIGHT":

                    self.stage_map[y].append(StageItem.MIRROR_RIGHT)

                elif self.stages[self.stage_no][y][x] == "CRACKED_BRICK":

                    self.stage_map[y].append(StageItem.CRACKED_BRICK)

                elif self.stages[self.stage_no][y][x] == "WATER":

                    self.stage_map[y].append(StageItem.WATER)

                elif self.stages[self.stage_no][y][x] == "SPAWNER":

                    self.stage_map[y].append(StageItem.SPAWNER)

                elif self.stages[self.stage_no][y][x] == "FOREST":

                    self.stage_map[y].append(StageItem.FOREST)
                
                elif self.stages[self.stage_no][y][x] == "HOME":

                    self.stage_map[y].append(StageItem.HOME)

                elif self.stages[self.stage_no][y][x] == "HEART_ON":

                    self.stage_map[y].append(StageItem.HEART_ON)
                
                elif self.stages[self.stage_no][y][x] == "HEART_OFF":

                    self.stage_map[y].append(StageItem.HEART_OFF)

                else:

                    self.stage_map[y].append(StageItem.OPEN)


    def load_file(self):

        file = open(self.file_name, mode ='r')
        csvFile = csv.reader(file)
        rows = []

        for file in csvFile:

            rows.append(file)

        self.no_of_stages = int(rows[0][1])

        self.spwan_locs = []

        for i in range(1, self.no_of_stages + 1):

            self.max_spawn_per_stage.append(int(rows[1][i]))

        print(self.max_spawn_per_stage)

        row_min, row_max = 0, 0

        for i in range(0, self.no_of_stages):

            if i == 0:

                row_min, row_max = 3, 19

            else:
                
                prev_row_max = row_max

                row_min, row_max = prev_row_max + 1, prev_row_max + 17

            stage = []

            for j in range(row_min, row_max):

                row = []

                for tile in rows[j]:

                    if tile:

                        row.append(tile)

                    else:

                        raise Exception("Please don't leave cells blank!")
                        
                stage.append(row)

            self.stages.append(stage)


    def clear(self, x, y):

        self.stages[self.stage_no][y][x] = "OPEN"
        self.stage_map[y][x] = StageItem.OPEN


    def set(self, x, y, stageItem, string): 

        self.stages[self.stage_no][y][x] = string
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