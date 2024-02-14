# fichier pour les objets
import pygame
class Objets:

    def __init__(self, nom, hp, vitesse, degats, nombre, url) -> None:
        self.nom = nom
        self.hp = hp
        self.vitesse = vitesse
        self.degats = degats
        self.nombre = nombre #{quantitée pour faire la recette}
        self.url = url

    # Vérification de la quantité de condiments
    def recette_beurre(self):
        if self.nom == "beurre":
            if self.nombre == 1:
                print("Assez de beurre")
                return True
    # Vérification de la quantité de condiments    
    def recette_egg(self):
        if self.nom == "egg":
            if self.nombre == 1:
                print("Assez d'oeuf")
                return True
    # Vérification de la quantité de condiments        
    def recette_flour(self):
        if self.nom == "flour":
            if self.nombre == 1:
                print("Assez de farine")
                return True
    # Vérification de la quantité de condiments            
    def recette_water(self):
        if self.nom == "water":
            if self.nombre == 1:
                print("Assez de d'eau")
                return True

    # Ajoute d'un condiments      
    def recette_add(self):
        self.nombre += 1
        print(self.nombre)

    def item_add(self, perso):
        perso.degats += self.degats
        perso.vitesse += self.vitesse
        perso.vie += self.hp

    def item_del(self, perso):
        perso.degats -= self.degats
        perso.vitesse -= self.vitesse
        perso.vie -= self.hp

# Comment uyiliser les items
# import le fichier avec le personnage et les objets
# objets.epee.item_add(perso.personnage) # Appel de la fonction "item_add" avec en paramètre self -> l'epee de dans les parentèses le personnage 
# print(perso.personnage.degats) # pour tester
# Meme chose pour "item_del"


# Condiments, nourriture, ...
class Beurre(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()

        original_image = pygame.image.load(image_path)
        new_width = 50  # Exemple de nouvelle largeur
        new_height = 50
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, world_shift):
        self.rect.x += world_shift

class Egg(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()

        original_image = pygame.image.load(image_path)
        new_width = 50  # Exemple de nouvelle largeur
        new_height = 50
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, world_shift):
        self.rect.x += world_shift
class Flour(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()

        original_image = pygame.image.load(image_path)
        new_width = 50  # Exemple de nouvelle largeur
        new_height = 50
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, world_shift):
        self.rect.x += world_shift
class Water(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()

        original_image = pygame.image.load(image_path)
        new_width = 50  # Exemple de nouvelle largeur
        new_height = 50
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, world_shift):
        self.rect.x += world_shift

beurre = Objets("beurre",0,0,0,0,"assets/ImagesTri-Armor/ItemsTri-Armor/butter.png")     
egg = Objets("egg",0,0,0,0,"assets/ImagesTri-Armor/ItemsTri-Armor/egg.png")
flour = Objets("flour",0,0,0,0,"assets/ImagesTri-Armor/ItemsTri-Armor/flour.png")
water = Objets("water",0,0,0,0,"assets/ImagesTri-Armor/ItemsTri-Armor/water.png")
galette = Objets("galette",0,0,0,0,"assets/ImagesTri-Armor/ItemsTri-Armor/galette.png")
kouignamann = Objets("kouignamann.png",0,0,0,0,"assets/ImagesTri-Armor/ItemsTri-Armor/kouignamann.png")

# objets
bouclier = Objets("bouclier",0,0,0,0,"")
epee = Objets("eppe",0,0,100,0,"")
rolling_pin = Objets("Rolling Pin",0,0,100,0,"assets/ImagesTri-Armor/ItemsTri-Armor/rolling-pin.png")
lance_pierres = Objets("Lance pierres",0,0,0,0,"assets/ImagesTri-Armor/ItemsTri-Armor/lance-pierres.png")
parchemin = Objets("parchemin",0,0,0,0,"assets/ImagesTri-Armor/ItemsTri-Armor/parchemin.png")