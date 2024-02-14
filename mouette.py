import pygame

class Mouette(pygame.sprite.Sprite):
    def __init__(self, pos,min_x, max_x):
        super().__init__()
        self.image = pygame.image.load('assets\ImagesTri-Armor\MobsTri-Armor\crab.png')  # Assurez-vous que le chemin d'accès est correct
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=pos)

        self.vie = 100  # Exemple de vie de l'ennemi
        self.speed = 2
        self.min_x = min_x
        self.max_x = max_x
        self.direction = 1

  # 1 pour droite, -1 pour gauche

    def move(self):
        # Déplacement simple de gauche à droite
        self.rect.x += self.speed * self.direction
        if self.rect.right >= self.max_x or self.rect.left <= self.min_x:
            self.direction *= -1  # Changez de direction

    def attack(self):
        # Exemple d'attaque (peut être étendu)
        pass

    def update(self, world_shift):
        self.move()
        self.rect.x += world_shift

 