#MAIN FILE (RUN THIS CODE TO EXECUTE GAME)
#--------------------------------------
#LOGS

#PHASE 1
#ALREADY DONE:
    #STONE, BRICK, MIRROR, AND EMPTY CELLS
    #STAGE LAYOUT (SUBJECT TO ADJUSTMENTS)
    #PLAYER MOVEMENT
    #WALKABILITY LOGIC
    #SHOOTING BULLETS
    #LOGIC FOR BULLET HITTING STONE, BRICK, AND MIRROR CELLS (YAY!!!)
    #LOGIC FOR BULLET HITTING ENEMY
    #LOGIC FOR PLAYER-ENEMY TANK COLLISIONS
    #LOGIC FOR ENEMY RANDOM BULLETS
    #LOGIC FOR ENEMY RANDOM MOVEMENTS (AI MOVEMENTS, SEE SIR 11CHO'S NOTION)
    #LOGIC FOR ENEMY BULLET HITTING PLAYER
    #LOGIC FOR FRIENDLY FIRE (HEHE NOT SURE IMMA SKIP)

#TO BE DONE

#PHASE 2
#TO BE DONE
    #BULLET-BULLET COLLISION
    #PERIODIC ENEMY SPAWNING
    #SEPARATE STAGE FILE FROM SOURCE CODE (IDK WHAT THIS MEANS; MAYBE CREATE AN INSTANCE OR SEPARATE FILE)
    #WATER CELL (DESIGN AND IMPLEMENTATION)
    #CRACKED BRICK CELL (DESIGN AND IMPLEMNTATION)

#PHASE 3
#TO BE DONE
    #REFER NALANG SA NOTION HAHAHAHA

#--------------------------------------

#TILEMAP WAS USED; NO PYXELGRID
import pyxel
import yaml
from player_copy import Player
from world_copy import World, world_item_draw, WorldItem, isColliding, TILE_SIZE
from bullet_copy import Bullet, drawBullet
from enemy_copy import Enemy, drawEnemy
import time
import random

TILE_SIZE = 8

class App:
    def __init__(self):
        pyxel.init(128, 128, title = "Battle City") #sCREEN SIZE
        pyxel.load("pyxeledit_copy.pyxres") #LOADS RESOURCE FILE FOR TILEMAP AND SPRITES
        self.world = World(pyxel.tilemap(0)) #CREATE INSTANCE OF STAGE (WITH TILEMAP AS ARGUMENT)
        self.player = Player(self.world) #CREATE INSTANCE OF PLAYER CHARACTER
        self.player_bullets = [] #TO STORE ALL BULLETS EJECTED BY PLAYER
        self.last_spawn_time = time.time()
        self.SPAWN_COOLDOWN = 10 # TIME INTERVAL FOR ENEMY SPAWNING
        self.enemies = [] #TO STORE ALL INSTANCES OF ENEMY TANK
        self.isGameOver  = False
        pyxel.run(self.update, self.draw)

    def update(self): #RUNS ALL FUNCTIONS EVERY FRAME

        if not self.isGameOver:
            self.playerMovement()
            self.shoot()
            self.bulletMovement()
            self.enemyHit()
            

            # PERIODICAL SPAWNING FOR ENEMIES 
            current_time = time.time()
            if current_time - self.last_spawn_time >= self.SPAWN_COOLDOWN:
                DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
                spawn_places = [(4, 9), (8, 4)]  # Tile coordinates (32/8, 72/8) and (64/8, 32/8)
                chosen_spawn = random.choice(spawn_places)

                tile_x, tile_y = chosen_spawn
                if self.world.world_map[tile_y][tile_x] == WorldItem.SPAWNER:
                    spawn_x, spawn_y = tile_x * TILE_SIZE, tile_y * TILE_SIZE
                    chosen_enemy = Enemy(spawn_x, spawn_y, random.choice(DIRECTIONS), self.world, self.player)
                    self.enemies.append(chosen_enemy)
                    self.last_spawn_time = current_time
            # PERIODICAL SPAWNING FOR ENEMIES


            self.world.set(4,9, WorldItem.SPAWNER) # designated enemy spawn spots in the map (ensures spawner tile is set after enemy spawning)
            self.world.set(8,4, WorldItem.SPAWNER) # designated enemy spawn spots in the map (ensures spawner tile is set after enemy spawning)

            for enemy in self.enemies: 
                enemy.enemyMovement()
                enemy.shootBullets()
                enemy.bulletMovement()


    def playerMovement(self): #***FUNCTION TO BE MADE A METHOD OF PLAYER LATER
        if pyxel.btn(pyxel.KEY_W):
            self.player.move_up()
        elif pyxel.btn(pyxel.KEY_S):
            self.player.move_down()
        elif pyxel.btn(pyxel.KEY_A):
            self.player.move_left()
        elif pyxel.btn(pyxel.KEY_D):
            self.player.move_right()
    
    def bulletMovement(self): #MOVEMENT OF PLAYER'S BULLET/S #***FUNCTION TO BE MADE A METHOD OF PLAYER LATER
        if self.player_bullets:
            for bullet in self.player_bullets:
                if bullet.dir == "LEFT":
                    bullet.left()
                elif bullet.dir == "RIGHT":
                    bullet.right()
                elif bullet.dir == "UP":
                    bullet.up()
                elif bullet.dir == "DOWN":
                    bullet.down()
                
                # REMOVE INACTIVE BULLETS 
                if bullet.state == "INACTIVE":
                    self.player_bullets.remove(bullet)

    def shoot(self): #TRIGGER FOR PLAYER'S BULLET #***FUNCTION TO BE MADE A METHOD OF PLAYER LATER
        if pyxel.btnr(pyxel.KEY_Z) and not self.player_bullets:
            self.bullet = Bullet(self.player.x, self.player.y, self.player.dir, self.world, self.player)
            self.player_bullets.append(self.bullet)

    def enemyHit(self): #CHECKS IF PLAYER'S BULLET HITS AN ENEMY TANK
        if self.player_bullets and self.enemies:
            for bullet in self.player_bullets:
                for enemy in self.enemies:
                    if isColliding(bullet.x, bullet.y, enemy.x, enemy.y):
                        enemy.state = "INACTIVE"
                        bullet.state = "INACTIVE"
                        break
        # EDITED SO THAT IT TURNS COLLIDED BULLETS INACTIVE -> INACTIVE BULLETS ARE REMOVED FROM THE LIST (CHECK def bulletMovement)

    def draw_game_over(self):
        pyxel.text(128 / 2 - 17, 128 / 2 - 2, 'Game over', 4)

    def draw(self): #ALSO RUNS THE FUNCTIONS EVERY FRAME
        pyxel.cls(0)

        for y in range(self.world.HEIGHT): #DRAW THE STAGE
            for x in range(self.world.WIDTH):
                world_item = self.world.world_map[y][x]
                world_item_draw(pyxel, x, y, world_item)

        if self.player_bullets: #DRAW PLAYER'S BULLETS
            new_player_bullet = []
            for bullet in self.player_bullets:
                if bullet.state == "ACTIVE":
                    drawBullet(pyxel, bullet)
                    new_player_bullet.append(bullet)
            self.player_bullets = new_player_bullet #UPDATES PLAYER'S BULLETS LIST (INACTIVE AKA VANISHED BULLETS ARE REOMVED)
            # i tried to test when is the best way to remove the inactive bullets pero PARANG wala naman difference if the remove inactive bullets
            # is here or in the earlier functions LOL.

        if self.enemies: #DRAW ENEMY TANKS
            new_enemies = []
            for enemy in self.enemies:
                enemy.drawBullets() #DRAW ENEMY BULLETS
                self.world.clear(int(enemy.prev_x / TILE_SIZE), int(enemy.prev_y / TILE_SIZE))
                if enemy.state == "ACTIVE":
                    self.world.set(int(enemy.x / TILE_SIZE), int(enemy.y / TILE_SIZE), WorldItem.ENEMY)
                    new_enemies.append(enemy)
                    drawEnemy(pyxel, enemy)
                elif enemy.state == "INACTIVE":
                    self.world.clear(int(enemy.x / TILE_SIZE), int(enemy.y / TILE_SIZE))
            self.enemies = new_enemies #UPDATES ENEMY TANK LIST (INACTIVE AKA DEAD TANKS ARE REOMVED)

        self.world.clear(int(self.player.prev_x / TILE_SIZE), int(self.player.prev_y / TILE_SIZE))
        if self.player.state == "ACTIVE":
            pyxel.blt( #DRAW THE PLAYER
                self.player.x, 
                self.player.y, 
                self.player.IMG, 
                self.player.U,
                self.player.V, 
                self.player.WIDTH, 
                self.player.HEIGHT
            )
            self.world.set(int(self.player.x / TILE_SIZE), int(self.player.y / TILE_SIZE), WorldItem.PLAYER)

        elif self.player.state == "INACTIVE":
            self.draw_game_over()
            self.isGameOver = True
            pyxel.blt( #DRAW THE PLAYER
                self.player.x, 
                self.player.y, 
                self.player.IMG, 
                0,
                0, 
                self.player.WIDTH, 
                self.player.HEIGHT
            )
            self.world.clear(int(self.player.x / TILE_SIZE), int(self.player.y / TILE_SIZE))


        # ENSURES SPAWNER TILE IS DRAWN ALL TIMES BEFORE SPAWNING
        for y in range(self.world.HEIGHT):
            for x in range(self.world.WIDTH):
                if self.world.world_map[y][x] == WorldItem.SPAWNER:
                    world_item_draw(pyxel, x, y, WorldItem.SPAWNER)
        # ENSURES SPAWNER TILE IS DRAWN ALL TIMES BEFORE SPAWNING
        
        
App()