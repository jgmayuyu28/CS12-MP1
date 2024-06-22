from player import Player
from stage import Stage, StageItem, stage_item_draw, TILE_SIZE
from bullet import drawBullet
from enemy import Enemy, drawEnemy
from stronger_enemy import Stronger_Enemy, draw_StrongerEnemy
from powerup import PowerUp, drawPowerUp
from sound import PyxelSounds
import pyxel
import time
import random

#PRESS P TO PAUSE THE GAME. PRESS IT AGAIN TO UNPAUSE
#PRESS C TO USE THE CHEAT. WHEN YOU HAVE 1 LIFE LEFT, IT WILL ADD ANOTHER LIFE.
#PRESS J TO CONTINUE THE GAME AFTER BEING HIT.
#THERE ARE 2 TYPES OF ENEMIES. THE RED ONE REQUIRES ONE HIT TO DESTROY WHILE THE GRAY ONE REQUIRES TWO HITS
#THE HOME CELL IS THE ONE WITH THE LETTER H. IF HIT BY ANY BULLET (EITHER FROM THE ENEMY OR PLAYER), THE GAME IS OVER

class App:

    def __init__(self):

        pyxel.init(128, 128, title="Battle City", fps=35)
        pyxel.load("pyxeledit.pyxres")
        self.stage_level = 0  # Start from stage 0
        self.health = 2  # Initialize player health here
        self.file_name = str(input("Please enter name of stage file (e.g. stage_file.csv):"))
        self.reset()
        pyxel.run(self.update, self.draw)


    def reset(self, reset_health=False):

        self.stage = Stage(self.stage_level, self.file_name)
        self.spawn_count = 0
        self.max_spawn_per_stage = self.stage.max_spawn_per_stage
        self.enemies = []
        self.enemies_killed = 0 #to know if round is won
        self.powerUps = [] #powerups
        self.activate_powerUp = False #powerups
        self.powerUp_duration = 5 #powerups

        if reset_health:

            self.health = 2  # Reset player health only when specified

        self.player = Player(self.stage.player_x * TILE_SIZE, self.stage.player_y * TILE_SIZE, self.stage, self.enemies, self.health)
        self.last_spawn_time = time.time()
        self.spawn_cooldown = 5
        self.isGameWon = False
        self.powerUp_spawned = False
        self.playerhealth_IS_ONE = False
        self.first_enemy_spawn()
        self.home = self.stage.HOME
        self.home_state = "ACTIVE"
        self.paused = False
        self.cheat_state = False
        self.sounds = PyxelSounds()


    def update(self):

        if pyxel.btnp(pyxel.KEY_R):

            self.stage_level = 0  # Reset to stage 0
            self.reset(reset_health=True)  # Reset health on full game reset

        if pyxel.btnp(pyxel.KEY_C):

            if self.player.health == 1:

                self.player.health += 1
                self.draw_cheat()


        self.home_hit()

        if pyxel.btnp(pyxel.KEY_P):

            self.paused = not self.paused

        if self.paused:

            return
        
        if self.playerhealth_IS_ONE:

            if pyxel.btnp(pyxel.KEY_J):

                self.playerhealth_IS_ONE = not self.playerhealth_IS_ONE
        

        if self.playerhealth_IS_ONE:

            self.draw_player_hit_restart()
            return
        

        if not self.player.isGameOver and not self.isGameWon:

            self.player.player_behavior()
            self.enemy_hit()
            self.friendly_fire_delay()
            self.friendly_fire()
            self.powerUp_get()


            #power up (freezes all enemies for 5 seconds)
            if not self.activate_powerUp: #powerups

                if self.spawn_count != self.max_spawn_per_stage[self.stage_level]:

                    self.enemy_spawn()

                self.player_hit()
                self.bullet_collision()

                for enemy in self.enemies:

                    enemy.enemyBehavior()

            else:

                for enemy in self.enemies:

                    enemy.bullets.clear()

                self.powerUp_duration -= 0.01

                if self.powerUp_duration < 0:

                    self.activate_powerUp = False
                    self.powerUp_duration = 5

            if self.enemies_killed == self.max_spawn_per_stage[self.stage_level] // 2 and not self.powerUp_spawned:

                self.powerUp_spawn()

            if self.enemies_killed == self.max_spawn_per_stage[self.stage_level]:

                self.isGameWon = True
                self.sounds.play_sound(4) #round won sound

        if self.isGameWon:

            if pyxel.btn(pyxel.KEY_N): #click to proceed to next stage
                
                if self.stage_level < len(self.stage.max_spawn_per_stage) - 1:

                    self.stage_level += 1  # Move to the next stage
                    self.health = self.player.health  # Carry over player health
                    self.reset()
                    self.update_heart()

   
    def home_hit(self):

        all_bullets = self.player.bullets + [bullet for enemy in self.enemies for bullet in enemy.bullets]
        home_x, home_y = self.home
        home_x *= TILE_SIZE
        home_y *= TILE_SIZE

        for bullet in all_bullets:

            if (
                home_x + TILE_SIZE > bullet.x
                and bullet.x + bullet.WIDTH > home_x
                and home_y + TILE_SIZE > bullet.y
                and bullet.y + bullet.HEIGHT > home_y
            ):
                self.player.bullets.clear()

                for enemy in self.enemies:

                    enemy.bullets.clear()

                self.player.state = "INACTIVE"
                self.sounds.play_sound(3)
                self.home_state = "INACTIVE"
                

    def player_hit(self):

        for enemy in self.enemies:

            for bullet in enemy.bullets:

                if (
                    self.player.x + self.player.WIDTH > bullet.x
                    and bullet.x + bullet.WIDTH > self.player.x
                    and self.player.y + self.player.HEIGHT > bullet.y
                    and bullet.y + bullet.HEIGHT > self.player.y
                ):
                    
                    self.player.health -= 1

                    if self.player.health == 1:

                        self.stage.set(8, 0, StageItem.HEART_OFF, "HEART_OFF")
                        self.playerhealth_IS_ONE = True
                        
                    if self.player.health <= 0:

                        self.stage.set(7, 0, StageItem.HEART_OFF, "HEART_OFF")
                        self.player.state = "INACTIVE"
                        self.sounds.play_sound(3)

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
                    
                    if isinstance(enemy, Stronger_Enemy):

                        enemy.health -= 1

                        if enemy.health <= 0:

                            enemy.state = "INACTIVE"
                            self.enemies_killed += 1

                        bullet.state = "INACTIVE"

                    else:

                        enemy.state = "INACTIVE"
                        bullet.state = "INACTIVE"
                        self.enemies_killed += 1

                    self.sounds.play_sound(1) #enemy tank dead sound


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
                print("ae")
                self.sounds.play_sound(3)
                self.player.state = "INACTIVE"
                bullet.state = "INACTIVE"

                if self.powerUps:
                    
                    self.powerUps[0].state = "INACTIVE"


    def friendly_fire_delay(self):

        if self.player.timer < 0:

            self.player.ff_on = True

        if not self.player.bullets:

            self.player.timer = 1.5
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
                weaker_enemy = Enemy(spawn_x, spawn_y, random.choice(directions), self.stage, self.player, self.enemies)
                stronger_enemy = Stronger_Enemy(spawn_x, spawn_y, random.choice(directions), self.stage, self.player, self.enemies, 2)
                enemy_choices = [weaker_enemy, stronger_enemy]
                chosen_enemy = random.choice(enemy_choices)
                self.enemies.append(chosen_enemy)
                self.last_spawn_time = current_time
                self.spawn_count += 1
    
    def first_enemy_spawn(self):

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
            weaker_enemy = Enemy(spawn_x, spawn_y, random.choice(directions), self.stage, self.player, self.enemies)
            stronger_enemy = Stronger_Enemy(spawn_x, spawn_y, random.choice(directions), self.stage, self.player, self.enemies, 2)
            enemy_choices = [weaker_enemy, stronger_enemy]
            chosen_enemy = random.choice(enemy_choices)
            self.enemies.append(chosen_enemy)
            self.spawn_count += 1

    def draw(self):

        pyxel.cls(0)
        self.draw_stage_above()
        self.player.drawPlayer()
        self.draw_enemies()
        self.draw_powerUp()
        self.draw_stage_below() #items above the player tank (forest)
        self.draw_player_bullets()

        if self.playerhealth_IS_ONE:

            self.draw_player_hit_restart()

        if self.paused:

            self.draw_game_paused()

        if self.player.isGameOver:

            self.draw_game_over()

        if self.isGameWon:

            self.draw_game_won()


    def draw_cheat(self):

        self.stage.set(8, 0, StageItem.HEART_ON, "HEART_ON")
    
    def update_heart(self):

        if self.health == 1:
                    
                    self.stage.set(8, 0, StageItem.HEART_OFF, "HEART_OFF")

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

                if stage_item != StageItem.FOREST and stage_item != StageItem.HOME:

                    stage_item_draw(pyxel, x, y, stage_item)

                elif stage_item == StageItem.HOME:

                    if self.home_state == "ACTIVE":

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

                    if isinstance(enemy, Stronger_Enemy):

                        draw_StrongerEnemy(pyxel, enemy)

                    else:

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

        pyxel.text(128 / 2 - 20, 128 / 2 - 10, 'Game over!', 8)
        pyxel.text(128 / 2 - 35, 128 / 2, 'Press R to restart', 8)


    def draw_game_paused(self):

        pyxel.text(128 / 2 - 25, 128 / 2 - 2, 'Game is paused', 10)


    def draw_player_hit_restart(self):

        pyxel.text(128 / 2 - 30, 128 / 2 - 10, 'Player got hit!', 11)
        pyxel.text(128 / 2 - 40, 128 / 2, 'Press J to continue', 11)


    def draw_game_won(self):

        pyxel.text(128 / 2 - 15, 128 / 2 - 10, 'You Won!', 11)

        if self.stage_level + 1 < len(self.max_spawn_per_stage):

            pyxel.text(128 / 2 - 50, 128 / 2, 'Press N for the next level', 11)

        elif self.stage_level + 1 >= len(self.max_spawn_per_stage):

            pyxel.text(128 / 2 - 40, 128 / 2, 'Press R to play again', 11)


App()