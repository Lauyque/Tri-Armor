import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,inventaire):
        super().__init__()
        self.image_droite = pygame.image.load('assets/ImagesTri-Armor/MobsTri-Armor/Mam_gouding.png')
        self.image_gauche = pygame.image.load('assets/ImagesTri-Armor/MobsTri-Armor/Mam_gouding gauche.png')
        self.collected_objects = {"beurre": 0, "egg": 0, "flour": 0, "water": 0}  # inventaire du joueur

        self.image = pygame.transform.scale(self.image_droite, (45, 60))
        self.rect = self.image.get_rect(topleft=pos)
        #self.image = pygame.Surface((32,58))
        #self.image.fill('red')
        self.collect_sound = pygame.mixer.Sound("assets/music/coin-collect.mp3")
        self.show_inventory = False
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 3

        self.score = 0
        self.gravity = 1
        self.jump_speed = -16
        self.inventaire = inventaire 

    #     character_path = 'assets/perso.png'
    #     self.animations = {'run':[], 'jump':[], 'idle':[], 'fall':[]}

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.image = pygame.transform.scale(self.image_droite, (45, 60))
        elif keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.direction.x = -1
            self.image = pygame.transform.scale(self.image_gauche, (45, 60))
        else:
            self.direction.x = 0


        if keys[pygame.K_SPACE]:
            self.jump()
        if keys[pygame.K_e]:

            self.inventaire.toggle()
                 # Bascule l'état du flag
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        #self.direction.y = self.jump_speed
        #self.on_ground = False  # Le personnage n'est plus au sol
        if self.direction.y == 0:
            self.direction.y = self.jump_speed


    def collect_item(self, item_name):
        if item_name in self.collected_objects:
            self.collected_objects[item_name] += 1
            print(f"Vous avez collecté {item_name} !")
            self.inventaire.add_item(item_name) 
            self.score += 100
            self.collect_sound.play()
    def update(self):
        self.get_input()