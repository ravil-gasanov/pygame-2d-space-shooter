import pygame

EXPLOSION_END = pygame.USEREVENT + 5

class Explosion(pygame.rect.Rect):
    def __init__(self, canvas, left, top):
        self.canvas = canvas
        self.left, self.top, self.width, self.height = left, top, 100, 100
        super().__init__(self.left, self.top, self.width, self.height)

        filename = 'sprites/explosion/explosion_{}.png'
        self.NUM_OF_SPRITES = 3
        self.sprites = []
        self.current_sprite_idx = 0

        self.start_time = pygame.time.get_ticks()

        for i in range(0, self.NUM_OF_SPRITES):
            sprite = pygame.image.load(filename.format(i))
            rescaled_sprite = pygame.transform.scale(sprite, (self.width, self.height))
            self.sprites.append(rescaled_sprite)
        
    def draw(self):
        self.canvas.blit(self.sprites[int(self.current_sprite_idx)], (self.left, self.top))
        self.current_sprite_idx += 0.25
        if self.current_sprite_idx >= self.NUM_OF_SPRITES:
            self.current_sprite_idx = 0
        
        if pygame.time.get_ticks() - self.start_time >= 3000:
            pygame.event.post(pygame.event.Event(EXPLOSION_END))
