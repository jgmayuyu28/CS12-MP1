from player import Player
from stage import Stage, StageItem, stage_item_draw, TILE_SIZE
from bullet import drawBullet
from enemy import Enemy, drawEnemy
import pyxel
import time
import random

class App:
    def __init__(self):

        pyxel.init(128, 128, title = "Battle City", fps = 40)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        pyxel.load("pyxeledit.pyxres")
        self.stage = Stage(pyxel.tilemap(0))
        self.enemies = []
        self.player = Player(self.stage, self.enemies)
        self.enemy_1 = Enemy(32, 72, "DOWN", self.stage, self.player, self.enemies)
        self.enemies.append(self.enemy_1)
        self.last_spawn_time = time.time()
        self.spawn_cooldown = 10

        pyxel.playm(0, loop=True)

    def update(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
            
        if not self.player.isGameOver and not self.player.isGameWon:

            self.player.player_behavior()
            self.enemy_spawn()
            self.player_hit()
            self.enemy_hit()

            self.friendly_fire()
            self.friendly_fire_delay()

            self.bullet_collision()

            for enemy in self.enemies:

                enemy.enemyBehavior()


    def player_hit(self):

        for enemy in self.enemies:

            for bullet in enemy.bullets:

                if (
                    self.player.x + self.player.WIDTH > bullet.x
                    and bullet.x + bullet.WIDTH > self.player.x
                    and self.player.y + self.player.HEIGHT > bullet.y
                    and bullet.y + bullet.HEIGHT > self.player.y
                ):
                    
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
                    
                    enemy.state = "INACTIVE"
                    bullet.state = "INACTIVE"


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

            print(spawn_places)
            chosen_spawn = random.choice(spawn_places)

            tile_x, tile_y = chosen_spawn

            if self.stage.stage_map[tile_x][tile_y] == StageItem.SPAWNER:

                spawn_x, spawn_y = tile_y * TILE_SIZE, tile_x * TILE_SIZE
                chosen_enemy = Enemy(spawn_x, spawn_y, random.choice(directions), self.stage, self.player, self.enemies)
                self.enemies.append(chosen_enemy)
                self.last_spawn_time = current_time

    
    def draw(self):

        pyxel.cls(0)
        
        self.draw_stage()
        self.player.drawPlayer()
        self.draw_player_bullets()
        self.draw_enemies()

        if self.player.isGameOver:

            self.draw_game_over()
        
        if self.player.isGameWon:

            self.draw_game_won()


    def draw_stage(self):

        for y in range(self.stage.HEIGHT): 

            for x in range(self.stage.WIDTH):

                Stage_item = self.stage.stage_map[y][x]
                stage_item_draw(pyxel, x, y, Stage_item)


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


    def draw_game_over(self):

        pyxel.text(128 / 2 - 17, 128 / 2 - 2, 'Game over!', 8)

    
    def draw_game_won(self):

        pyxel.text(128 / 2 - 15, 128 / 2 - 2, 'You Won!', 11)


App()
