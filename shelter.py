import pygame

class Shelter(pygame.sprite.Sprite):
    def __init__(self, pos, internal_temp, max_creatures, current_creatures, groups, main):
        super().__init__(groups)
        self.pos = pos
        self.internal_temp = internal_temp
        self.max_creatures = max_creatures

        self.main = main

        self.rect = pygame.Rect((pos), (25, 25))
        self.draw_rect = self.main.image_loader.shelter_image.get_rect(center=self.rect.center)

        self.current_creatures = []
        self.past_creatures = current_creatures
        self.full = False
    
    def add_past_creatures(self):
        for index in self.past_creatures:
            self.current_creatures.append(self.main.creatures[index])

    def update(self):
        if len(self.current_creatures) >= self.max_creatures:
            self.full = True
        else:
            self.full = False

        self.main.screen.blit(self.main.image_loader.shelter_image, self.draw_rect)