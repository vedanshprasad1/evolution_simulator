import pygame
from random import random

class Shrubs(pygame.sprite.Sprite):
    def give_resource(self):
        resource = int(self.resource)
        self.resource = 0
        return resource
    
    def check_if_dead(self):
        if random() <= self.dying_probability:
            self.main_list.remove(self)
            self.main.all_sprites.remove(self)
            self.kill()

class Bush(Shrubs):
    def __init__(self, pos, growth_rate, dying_probability, resource, groups, main):
        super().__init__(groups)
        self.pos = pos
        self.resource = resource
        self.growth_rate = growth_rate
        self.dying_probability = dying_probability

        self.rect = pygame.Rect((self.pos), (50, 25))
        self.main = main
        self.main_list = self.main.bushes

        self.draw_rect = self.main.image_loader.berry_image.get_rect(center=self.rect.center)

    def update(self):
        if not self.main.paused:
            if self.main.day_timer <= 0:
                self.check_if_dead()
                self.resource += self.growth_rate

        if self.resource >= 1:
            self.main.screen.blit(self.main.image_loader.berry_image, self.draw_rect)
        else:
            self.main.screen.blit(self.main.image_loader.bush_image, self.draw_rect)

        if self.resource > 10:
            self.resource = 10

class Tree(Shrubs):
    def __init__(self, pos, growth_rate, dying_probability, resource, groups, main):
        super().__init__(groups)
        self.pos = pos
        self.resource = resource
        self.growth_rate = growth_rate
        self.dying_probability = dying_probability

        self.rect = pygame.Rect((self.pos), (25, 25))
        self.main = main
        self.main_list = self.main.trees
        
    def draw_tree(self):
        if self.resource <= 25:
            self.rect.size = (25, 25)
            self.rect.top = self.pos[1]
            self.main.screen.blit(self.main.image_loader.short_tree_image, self.rect)
        elif self.resource <= 50:
            self.rect.size = (25, 50)
            self.rect.top = self.pos[1] - 12
            self.main.screen.blit(self.main.image_loader.medium_tree_image, self.rect)
        else: 
            self.rect.size = (25, 75)
            self.rect.top = self.pos[1] - 25
            self.main.screen.blit(self.main.image_loader.tall_tree_image, self.rect)

    def update(self):
        if not self.main.paused:
            if self.main.day_timer <= 0:
                self.check_if_dead()
                self.resource += self.growth_rate * 25
                if self.resource > 100:
                    self.resource = 100

        self.draw_tree()