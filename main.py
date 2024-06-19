from player import Player
from stage import Stage, StageItem, stage_item_draw, TILE_SIZE
from bullet import drawBullet
from enemy import Enemy, drawEnemy
from powerup import PowerUp, drawPowerUp
from sound import PyxelSounds
import pyxel
import time
import random

class App:

    MAX_SPAWN = 20 #MAX SPAWN FOR STAGE 1

    def __init__(self):

        pyxel.init(128, 128, title = "Battle City", fps = 35)
        pyxel.load("pyxeledit.pyxres")
        self.stage = Stage(pyxel.tilemap(0))
        self.spawn_count = 0
        self.enemies = []
        self.enemies_killed = 0 #to know if round is won
        self.powerUps = [] #powerups
        self.activate_powerUp = False #powerups
        self.powerUp_duration = 5 #powerups
        self.player = Player(self.stage, self.enemies)
        self.enemy_1 = Enemy(32, 72, "DOWN", self.stage, self.player, self.enemies)
        self.enemies.append(self.enemy_1)
        self.last_spawn_time = time.time()
        self.spawn_cooldown = 5
        self.isGameWon = False
        self.powerUp_spawned = False
        self.sounds = PyxelSounds()
        pyxel.run(self.update, self.draw)


    def update(self):

        if not self.player.isGameOver and not self.isGameWon:

            self.player.player_behavior()
            self.enemy_hit()
            self.friendly_fire()
            self.powerUp_get()
            self.friendly_fire_delay()

            #power up (freeze)

            if not self.activate_powerUp: #powerups

                if self.spawn_count != self.MAX_SPAWN:

                    self.enemy_spawn()

                self.player_hit()
                self.bullet_collision()

                for enemy in self.enemies:

                    enemy.enemyBehavior()

            else:
                
                self.powerUp_duration -= 0.01

                if self.powerUp_duration < 0:

                    self.activate_powerUp = False
                    self.powerUp_duration = 5


            if self.enemies_killed >= self.MAX_SPAWN // 2 and not self.powerUp_spawned:

                self.powerUp_spawn()

            if self.enemies_killed == self.MAX_SPAWN:

                self.isGameWon = True
                self.sounds.play_sound(4) #round won sound

        if self.isGameWon: 

            if pyxel.btn(pyxel.KEY_N): #click to proceed to nnext stage

                self.stage = Stage(pyxel.tilemap(1))
                self.MAX_SPAWN = 30
                self.spawn_count = 0
                self.enemies_killed = 0
                self.player = Player(self.stage, self.enemies)
                self.enemy_1 = Enemy(32, 72, "DOWN", self.stage, self.player, self.enemies)
                self.isGameWon = False
                self.enemies.append(self.enemy_1)


    def player_hit(self):

        for enemy in self.enemies:

            for bullet in enemy.bullets:

                if (
                    self.player.x + self.player.WIDTH > bullet.x
                    and bullet.x + bullet.WIDTH > self.player.x
                    and self.player.y + self.player.HEIGHT > bullet.y
                    and bullet.y + bullet.HEIGHT > self.player.y
                ):
                    
                    self.sounds.play_sound(3) #game over sound
                    self.player.state = "INACTIVE"
                    bullet.state = "INACTIVE"


    def enemy_hit(self):

        for enemy in self.enemies:

            for bullet in self.player.bullets:

                if (
                    enemy.x + enemy.WIDTH > bullet.x
                    and bullet.x + bullet.WIDTH > enemy.x
                    and enemy.y + enemy.HEIGHT > bullet.y
                    and bullet.y + bullet.HEIGHT > enemy.y
                ):
                    
                    self.enemies_killed += 1
                    enemy.state = "INACTIVE"
                    bullet.state = "INACTIVE"

                    self.sounds.play_sound(1) #enemy tank dead sound

                    if self.powerUps:

                        self.powerUps[0].state = "INACTIVE"


    def powerUp_spawn(self): #spawn powerup

        spawn_places = []

        for y in range(len(self.stage.stage_map)): 

            for x in range(len(self.stage.stage_map[0])):

                if self.stage.stage_map[y][x] == StageItem.OPEN:

                    spawn_places.append((y, x))

        chosen_spawn = random.choice(spawn_places)

        tile_x, tile_y = chosen_spawn

        if self.stage.stage_map[tile_x][tile_y] == StageItem.OPEN:

            self.powerUp = PowerUp(tile_y * TILE_SIZE, tile_x * TILE_SIZE, 5)
            self.powerUps.append(self.powerUp)
            self.powerUp_spawned = True


    def powerUp_get(self): #pick up powerup

        if self.powerUps:
            if (
                self.player.x + self.player.WIDTH > self.powerUps[0].x
                and self.powerUps[0].x + 8 > self.player.x
                and self.player.y + self.player.HEIGHT > self.powerUps[0].y
                and self.powerUps[0].y + 8 > self.player.y
            ):
                
                self.activate_powerUp = True
                self.powerUps[0].state = "INACTIVE"


    def friendly_fire(self):

        for bullet in self.player.bullets:

            if (
                self.player.x + self.player.WIDTH > bullet.x
                and bullet.x + bullet.WIDTH > self.player.x
                and self.player.y + self.player.HEIGHT > bullet.y
                and bullet.y + bullet.HEIGHT > self.player.y
            ) and self.player.ff_on:
                
                self.player.state = "INACTIVE"
                bullet.state = "INACTIVE"

                if self.powerUps:

                        self.powerUps[0].state = "INACTIVE"


    def friendly_fire_delay(self):

        if self.player.timer < 0:

            self.player.ff_on = True

        if not self.player.bullets:

            self.player.timer = 0.2
            self.player.ff_on = False


    def bullet_collision(self):

        for enemy in self.enemies:

            for enemy_bullet in enemy.bullets:

                for player_bullet in self.player.bullets:

                    if (
                    enemy_bullet.x + enemy_bullet.WIDTH > player_bullet.x
                    and player_bullet.x + player_bullet.WIDTH > enemy_bullet.x
                    and enemy_bullet.y + enemy_bullet.HEIGHT > player_bullet.y
                    and player_bullet.y + player_bullet.HEIGHT > enemy_bullet.y
                    ):
                        
                        self.sounds.play_sound(2) #bullet - bullet collision
                        player_bullet.state = "INACTIVE"
                        enemy_bullet.state = "INACTIVE"

    
    def enemy_spawn(self):

        current_time = time.time()

        if current_time - self.last_spawn_time >= self.spawn_cooldown:

            spawn_places = []

            directions = ["UP", "DOWN", "LEFT", "RIGHT"]

            for y in range(len(self.stage.stage_map)): 

                for x in range(len(self.stage.stage_map[0])):

                    if self.stage.stage_map[y][x] == StageItem.SPAWNER:

                        spawn_places.append((y, x))

            chosen_spawn = random.choice(spawn_places)

            tile_x, tile_y = chosen_spawn

            if self.stage.stage_map[tile_x][tile_y] == StageItem.SPAWNER:

                spawn_x, spawn_y = tile_y * TILE_SIZE, tile_x * TILE_SIZE
                chosen_enemy = Enemy(spawn_x, spawn_y, random.choice(directions), self.stage, self.player, self.enemies)
                self.enemies.append(chosen_enemy)
                self.last_spawn_time = current_time

                self.spawn_count += 1

    
    def draw(self):

        pyxel.cls(0)
        
        self.draw_stage_above()
        self.player.drawPlayer()
        self.draw_enemies()
        self.draw_powerUp()
        self.draw_stage_below() #items above the player tank (forest)
        self.draw_player_bullets()

        if self.player.isGameOver:

            self.draw_game_over()
        
        if self.isGameWon:

            self.draw_game_won()



    def draw_stage_below(self): #items above the player tank (forest)

        for y in range(self.stage.HEIGHT): 

            for x in range(self.stage.WIDTH):

                stage_item = self.stage.stage_map[y][x]

                if stage_item == StageItem.FOREST:

                    stage_item_draw(pyxel, x, y, stage_item)

    
    def draw_stage_above(self):

        for y in range(self.stage.HEIGHT): 

            for x in range(self.stage.WIDTH):

                stage_item = self.stage.stage_map[y][x]

                if stage_item != StageItem.FOREST:

                    stage_item_draw(pyxel, x, y, stage_item)


    def draw_player_bullets(self):

        if self.player.bullets:

            new_player_bullet = []

            for bullet in self.player.bullets:

                if bullet.state == "ACTIVE":

                    drawBullet(pyxel, bullet)
                    new_player_bullet.append(bullet)

            self.player.bullets.clear()
            self.player.bullets.extend(new_player_bullet)


    def draw_enemies(self):

        if self.enemies:

            new_enemies = []

            for enemy in self.enemies:

                enemy.drawBullets() 

                if enemy.state == "ACTIVE":

                    new_enemies.append(enemy)
                    drawEnemy(pyxel, enemy)
                    
            self.enemies.clear()
            self.enemies.extend(new_enemies)


    def draw_powerUp(self):

        if self.powerUps:

            new_powerUps = []

            for powerUp in self.powerUps:

                if powerUp.state == "ACTIVE":

                    drawPowerUp(pyxel, powerUp)
                    new_powerUps.append(powerUp)

            self.powerUps.clear()
            self.powerUps.extend(new_powerUps)


    def draw_game_over(self):

        pyxel.text(128 / 2 - 17, 128 / 2 - 2, 'Game over!', 8)

    
    def draw_game_won(self):

        pyxel.text(128 / 2 - 15, 128 / 2 - 40, 'You Won!', 11)
        pyxel.text(128 / 2 - 50, 128 / 2, 'Press N for the next level!', 11)


App()