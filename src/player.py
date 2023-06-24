import os
import pygame

WHITE = (255, 255, 255)

class Player(pygame.rect.Rect):
    def __init__(self, canvas):
        self.canvas = canvas
        self.width, self.height = 150, 150
        self.left, self.top = self.canvas.get_width() // 2 - self.width // 2,\
            self.canvas.get_height() - self.height
        super().__init__(self.left, self.top, self.width, self.height)

        self.health = 10
        self.SPEED = 10
        self.missile_side = -1

        filename = 'sprites/jet/jet_{}.png'
        self.NUM_OF_SPRITES = 4
        self.sprites = []
        self.current_sprite_idx = 0

        for i in range(0, self.NUM_OF_SPRITES):
            sprite = pygame.image.load(filename.format(i))
            rescaled_sprite = pygame.transform.scale(sprite, (self.width, self.height))
            self.sprites.append(rescaled_sprite)

    def move(self, direction):
        if direction == pygame.K_RIGHT:
            self.left += self.SPEED
            self.left = min(self.canvas.get_width() - self.width, self.left)
        elif direction == pygame.K_LEFT:
            self.left -= self.SPEED
            self.left = max(0, self.left)
        elif direction == pygame.K_UP:
            self.top -= self.SPEED
            self.top = max(0, self.top)
        elif direction == pygame.K_DOWN:
            self.top += self.SPEED
            self.top = min(self.canvas.get_height() - self.height, self.top)
    
    def get_position(self):
        return self.left, self.top

    def draw(self):
        self.canvas.blit(self.sprites[int(self.current_sprite_idx)], (self.left, self.top))
        self.current_sprite_idx += 0.25
        if self.current_sprite_idx >= self.NUM_OF_SPRITES:
            self.current_sprite_idx = 0
        
        health_font = pygame.font.SysFont('gothic', 80)
        health_text = health_font.render(str(self.health), 1, WHITE)
        self.canvas.blit(health_text, (10, self.canvas.get_height() - 60))

