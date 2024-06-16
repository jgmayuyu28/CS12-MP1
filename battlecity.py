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

#TO BE DONE
    #LOGIC FOR ENEMY RANDOM MOVEMENTS (AI MOVEMENTS, SEE SIR 11CHO'S NOTION)
    #LOGIC FOR ENEMY RANDOM BULLETS
    #LOGIC FOR ENEMY BULLET HITTING PLAYER
    #LOGIC FOR FRIENDLY FIRE

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
from player import Player
from world import World, world_item_draw, WorldItem, TILE_SIZE
from bullet import Bullet, drawBullet
from enemy import Enemy, drawEnemy

TILE_SIZE = 8

class App:
    def __init__(self):
        pyxel.init(128, 128, title = "Battle City") #sCREEN SIZE
        pyxel.load("pyxeledit.pyxres") #LOADS RESOURCE FILE FOR TILEMAP AND SPRITES
        self.world = World(pyxel.tilemap(0)) #CREATE INSTANCE OF STAGE (WITH TILEMAP AS ARGUMENT)
        self.player = Player(self.world) #CREATE INSTANCE OF PLAYER CHARACTER
        self.player_bullets = [] #TO STORE ALL BULLETS EJECTED BY PLAYER
        self.enemy1 = Enemy(32, 72, "DOWN", self.world)
        self.enemy2 = Enemy(64, 32, "LEFT", self.world) 
        self.enemies = [self.enemy1, self.enemy2] #TO STORE ALL INSTANCES OF ENEMY TANK
        pyxel.run(self.update, self.draw)

    def update(self): #RUNS ALL FUNCTIONS EVERY FRAME
        self.playerMovement()
        self.shoot()
        self.bulletMovement()
        self.enemy1.enemyMovement()
        self.enemyHit()
        self.enemy1.shootBullets()
        self.enemy1.bulletMovement()

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

    def shoot(self): #TRIGGER FOR PLAYER'S BULLET #***FUNCTION TO BE MADE A METHOD OF PLAYER LATER
        if pyxel.btnr(pyxel.KEY_Z):
            self.bullet = Bullet(self.player.x, self.player.y, self.player.dir, self.world)
            self.player_bullets.append(self.bullet)

    def enemyHit(self): #CHECKS IF PLAYER'S BULLET HITS AN ENEMY TANK
        if self.enemies:
            for enemy in self.enemies:
                print(int(enemy.x / TILE_SIZE), int(enemy.y / TILE_SIZE))
                print(self.world.world_map[int(enemy.y / TILE_SIZE)][int(enemy.x / TILE_SIZE)] == WorldItem.ENEMY_D)
                if self.world.world_map[int(enemy.y / TILE_SIZE)][int(enemy.x / TILE_SIZE)] == WorldItem.ENEMY_D:
                    print("enemy state inactive")
                    enemy.state = "INACTIVE"

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

        self.enemy1.drawBullets()

        if self.enemies: #DRAW ENEMY TANKS
            new_enemies = []
            for enemy in self.enemies:
                self.world.clear(int(enemy.prev_x / TILE_SIZE), int(enemy.prev_y / TILE_SIZE))
                if enemy.state == "ACTIVE":
                    self.world.set(int(enemy.x / TILE_SIZE), int(enemy.y / TILE_SIZE), WorldItem.ENEMY)
                    new_enemies.append(enemy)
                    drawEnemy(pyxel, enemy)
                elif enemy.state == "INACTIVE":
                    self.world.clear(int(enemy.x / TILE_SIZE), int(enemy.y / TILE_SIZE))
            self.enemies = new_enemies #UPDATES ENEMY TANK LIST (INACTIVE AKA DEAD TANKS ARE REOMVED)

        pyxel.blt( #DRAW THE PLAYER
            self.player.x, 
            self.player.y, 
            self.player.IMG, 
            self.player.U,
            self.player.V, 
            self.player.WIDTH, 
            self.player.HEIGHT
        )

App()