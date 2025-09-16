import random

import effects
import enemies
import player
import projectiles
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
GREEN = (0, 255, 0)

ASPHALT = (128, 126, 120)

BACKGROUND_PATH = "assets/background.jpg"
GAMEOVER_SOUND_PATH = "assets/sounds/gameover.wav"
EXPLOSION_SOUND_PATH = "assets/sounds/explosion.wav"
THEME_SOUND_PATH = "assets/sounds/theme.mp3"


GAME_OVER = pygame.USEREVENT + 1
MUSIC_END = pygame.USEREVENT + 2
MISSILE_LOST = pygame.USEREVENT + 3
PLAYER_TAKES_DAMAGE = pygame.USEREVENT + 4
EXPLOSION_END = pygame.USEREVENT + 5


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h

        self.canvas = pygame.display.set_mode(size=(self.WIDTH, self.HEIGHT))
        self.background = pygame.transform.scale(
            pygame.image.load(BACKGROUND_PATH), (self.WIDTH, self.HEIGHT)
        )

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.player = player.Player(self.canvas)
        self.missiles = []
        self.enemies = []
        self.explosions = []
        self.game_score = 0

        self.cooldown = 0
        self.enemy_cooldown = 50

        self.GAME_OVER_FONT = pygame.font.SysFont("gothic", 80)
        self.GAME_OVER_SOUND = pygame.mixer.Sound(GAMEOVER_SOUND_PATH)

        self.EXPLOSION_SOUND = pygame.mixer.Sound(EXPLOSION_SOUND_PATH)

    def run(self):
        pygame.mixer.music.load(THEME_SOUND_PATH)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(MUSIC_END)
        game_over = False

        while not game_over:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == GAME_OVER:
                    game_over = True
                elif event.type == MISSILE_LOST:
                    self.missiles.pop(0)
                elif event.type == PLAYER_TAKES_DAMAGE:
                    self.player.health -= 1
                    if self.player.health <= 0:
                        game_over = True
                    self.enemies.pop(0)
                elif event.type == EXPLOSION_END:
                    self.explosions.pop(0)
                elif event.type == MUSIC_END:
                    pygame.mixer.music.play()

            self.handle_keypresses(pygame.key.get_pressed())
            self.check_collisions()
            self.game_updates()

            if game_over:
                pygame.mixer.music.stop()
                self.GAME_OVER_SOUND.play()
                game_over_text = self.GAME_OVER_FONT.render("GAME OVER", 1, BLACK)
                self.canvas.blit(
                    game_over_text,
                    (
                        self.WIDTH // 2 - game_over_text.get_width() // 2,
                        self.HEIGHT // 2 - game_over_text.get_height(),
                    ),
                )

            self.draw()

        pygame.time.wait(2500)

    def game_updates(self):
        if not self.enemy_cooldown and len(self.enemies) <= 5:
            left, top = int(random.uniform(0, self.WIDTH - self.player.width)), 0
            enemy = enemies.EnemyJet(self.canvas, left, top)
            self.enemies.append(enemy)
            self.enemy_cooldown = int(random.uniform(50, 80))

        for missile in self.missiles:
            missile.fly()

        for enemy in self.enemies:
            enemy.fly()

        self.cooldown = max(0, self.cooldown - 1)
        self.enemy_cooldown = max(0, self.enemy_cooldown - 1)

    def handle_keypresses(self, keys_pressed):
        directions = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

        for direction in directions:
            if keys_pressed[direction]:
                self.player.move(direction)

        if keys_pressed[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if not self.cooldown:
            self.missiles.append(projectiles.Missile(self.canvas, self.player))
            self.cooldown = 20

    def check_collisions(self):
        for enemy_idx, enemy in enumerate(self.enemies):
            for missile_idx, missile in enumerate(self.missiles):
                if enemy.colliderect(missile):
                    left, top = enemy.x, enemy.y
                    explosion = effects.Explosion(self.canvas, left, top)
                    self.explosions.append(explosion)
                    self.EXPLOSION_SOUND.play()

                    self.enemies.pop(enemy_idx)
                    self.game_score += 1
                    self.missiles.pop(missile_idx)

            if enemy.colliderect(self.player):
                pygame.event.post(pygame.event.Event(PLAYER_TAKES_DAMAGE))

                left, top = enemy.x, enemy.y
                explosion = effects.Explosion(self.canvas, left, top)
                self.explosions.append(explosion)
                self.EXPLOSION_SOUND.play()

    def draw(self):
        self.draw_background()

        for missile in self.missiles:
            missile.draw()

        self.player.draw()

        for enemy in self.enemies:
            enemy.draw()

        for explosion in self.explosions:
            explosion.draw()

        pygame.display.update()

    def draw_background(self):
        self.canvas.blit(self.background, (0, 0))

        score_text = self.GAME_OVER_FONT.render(str(self.game_score), 1, WHITE)
        self.canvas.blit(score_text, (10, 10))


if __name__ == "__main__":
    Game().run()
