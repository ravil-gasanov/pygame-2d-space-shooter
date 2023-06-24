import pygame

PLAYER_TAKES_DAMAGE = pygame.USEREVENT + 4

class EnemyJet(pygame.rect.Rect):
    def __init__(self, canvas, left, top):
        self.canvas = canvas
        self.left, self.top, self.width, self.height = left, top, 100, 100
        super().__init__(self.left, self.top, self.width, self.height)

        self.SPEED = 3
        self.right_side_missile = 0

        filename = 'sprites/jet/jet_{}.png'
        self.NUM_OF_SPRITES = 4
        self.sprites = []
        self.current_sprite_idx = 0

        for i in range(0, self.NUM_OF_SPRITES):
            sprite = pygame.image.load(filename.format(i))
            rescaled_sprite = pygame.transform.scale(sprite, (self.width, self.height))
            self.sprites.append(rescaled_sprite)
    
    def fly(self):
        self.top += self.SPEED

        if self.top >= self.canvas.get_height() + self.height:
            pygame.event.post(pygame.event.Event(PLAYER_TAKES_DAMAGE))
    
    def draw(self):
        self.canvas.blit(self.sprites[int(self.current_sprite_idx)], (self.left, self.top))
        self.current_sprite_idx += 0.25
        if self.current_sprite_idx >= self.NUM_OF_SPRITES:
            self.current_sprite_idx = 0