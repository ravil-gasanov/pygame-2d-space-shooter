import pygame

MISSILE_LOST = pygame.USEREVENT + 3

class Missile(pygame.rect.Rect):
    def __init__(self, canvas, player):
        self.canvas = canvas
        left, top = player.x, player.y
        self.left, self.top, self.width, self.height = left + 15 + player.missile_side * 40, top, 120, 180
        player.missile_side = player.missile_side * (-1)

        super().__init__(self.left, self.top, self.width, self.height)

        self.SPEED = 15

        filename = 'assets/sprites/missile/missile_{}.png'
        self.NUM_OF_SPRITES = 4
        self.sprites = []
        self.current_sprite_idx = 0

        for i in range(0, self.NUM_OF_SPRITES):
            sprite = pygame.image.load(filename.format(i))
            rescaled_sprite = pygame.transform.scale(sprite, (self.width, self.height))
            self.sprites.append(rescaled_sprite)

    def fly(self):
        self.top -= self.SPEED

        if self.top <= -self.height:
            pygame.event.post(pygame.event.Event(MISSILE_LOST))

    def draw(self):
        self.canvas.blit(self.sprites[int(self.current_sprite_idx)], (self.left, self.top))
        self.current_sprite_idx += 0.25
        if self.current_sprite_idx >= self.NUM_OF_SPRITES:
            self.current_sprite_idx = 0