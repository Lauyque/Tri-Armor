import pygame

class BossFinal(pygame.sprite.Sprite):
    def __init__(self, pos,min_x, max_x):
        super().__init__()
        self.image = pygame.image.load('assets\ImagesTri-Armor\MobsTri-Armor\warden.png')  # Remplacez par l'image de votre boss
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect(topleft=pos)
        self.vie = 100  # Exemple de vie du boss
        self.speed = 2
        self.min_x = min_x
        self.max_x = max_x
        self.direction = pygame.math.Vector2(0, 0)

    def move(self):
        # Implémentez ici la logique de mouvement du boss
        pass

    def attack(self):
        # Implémentez ici les attaques du boss
        pass

    def update(self, world_shift):
        self.move()
        self.rect.x += world_shift