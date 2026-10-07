import pygame
from os.path import join

class Image_loader():
    def __init__(self):
        self.bush_image = pygame.image.load(join("images", "bush.png")).convert_alpha()
        self.bush_image = pygame.transform.scale(self.bush_image, (50, 50))

        self.berry_image = pygame.image.load(join("images", "berrybush.png")).convert_alpha()
        self.berry_image = pygame.transform.scale(self.berry_image, (50, 50))

        self.short_tree_image = pygame.image.load(join("images", "short_tree.png")).convert_alpha()
        self.short_tree_image = pygame.transform.scale(self.short_tree_image, (30, 25))

        self.medium_tree_image = pygame.image.load(join("images", "medium_tree.png")).convert_alpha()
        self.medium_tree_image = pygame.transform.scale(self.medium_tree_image, (30, 50))

        self.tall_tree_image = pygame.image.load(join("images", "tall_tree.png")).convert_alpha()
        self.tall_tree_image = pygame.transform.scale(self.tall_tree_image, (30, 75))

        self.shelter_image = pygame.image.load(join("images", "shelter.png")).convert_alpha()
        self.shelter_image = pygame.transform.scale(self.shelter_image, (50, 50))