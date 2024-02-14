# inventaire.py
import pygame

class Inventaire:
    def __init__(self, surface):
        self.surface = surface
        self.items = {"beurre": 0, "egg": 0, "flour": 0, "water": 0}
        self.visible = False
        self.toggle_key = pygame.K_e  # Touche pour ouvrir/fermer l'inventaire

        # Définir la taille de l'inventaire
        self.width, self.height = 300, 200

        # Calculer la position centrale pour l'inventaire
        screen_width, screen_height = surface.get_size()
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2

    def toggle(self):
        # Basculez la visibilité de l'inventaire en appuyant sur la touche définie
        keys = pygame.key.get_pressed()
        if keys[self.toggle_key]:
            self.visible = not self.visible

    def draw(self):
        if self.visible:
            # Dessiner la surface de l'inventaire
            fond = pygame.Surface((self.width, self.height))
            fond.fill((0, 0, 0))  # Fond noir
            fond.set_alpha(180)  # Transparence
            self.surface.blit(fond, (self.x, self.y))

            # Afficher les éléments de l'inventaire
            police = pygame.font.Font(None, 24)
            x, y = self.x + 10, self.y + 10
            for item, count in self.items.items():
                texte = f"{item}: {count}"
                rendu = police.render(texte, True, (255, 255, 255))
                self.surface.blit(rendu, (x, y))
                y += 30  # Espacement entre les lignes

    def add_item(self, item_name):
        if item_name in self.items:
            self.items[item_name] += 1
