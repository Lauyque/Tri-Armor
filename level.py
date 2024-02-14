from time import sleep
import pygame
from GameState import GameState
from mouette import Mouette

from tiles import Tile
from settings import *
from player import Player
import score
import perso
import objets
from objets import Beurre
from objets import Egg
from objets import Flour
from objets import Water

from inventaire import Inventaire
from inventaire import Inventaire
from objets import Beurre
from enemy import Enemy
from boss import *


class Level:
    def __init__(self, level_data, surface,game_instance):

        self.surface = surface
        screen_height = len(level_map) * tile_size
        # Enregistrer le temps de début
        self.surface = surface
        self.temps_debut = pygame.time.get_ticks()
        self.perso_image = 'assets\ImagesTri-Armor\MobsTri-Armor\Mam_gouding.png'
        self.image_beurre = pygame.image.load(objets.beurre.url)
        self.image_egg = pygame.image.load(objets.egg.url)
        self.image_flour = pygame.image.load(objets.flour.url)
        self.image_water = pygame.image.load(objets.water.url)
        self.pop_up_beurre = pygame.image.load('assets/ImagesTri-Armor/ArrierePlanTri-Armor/popup_beurre.png')
        self.pop_up_egg = pygame.image.load('assets/ImagesTri-Armor/ArrierePlanTri-Armor/popup_egg.png')
        self.pop_up_flour = pygame.image.load('assets/ImagesTri-Armor/ArrierePlanTri-Armor/popup_flour.png')
        self.pop_up_water = pygame.image.load('assets/ImagesTri-Armor/ArrierePlanTri-Armor/popup_water.png')
        self.pop_up_fin = pygame.image.load('assets/ImagesTri-Armor/ArrierePlanTri-Armor/popup_fin.png')
        

        self.image_fond = pygame.image.load('assets/ImagesTri-Armor/ArrierePlanTri-Armor/space.png')
        self.image_fond_rect = self.image_fond.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2))


        teleporter_x = 500  # Coordonnée X du téléporteur
        teleporter_y = 200 
        teleporter_width = 100  # Largeur du téléporteur en pixels
        teleporter_height = 100 # Largeur du téléporteur en pixels
        self.teleporter_rect = pygame.Rect(teleporter_x, teleporter_y, teleporter_width, teleporter_height)
        self.teleporting = False  # Flag to track if the player is teleporting
        self.teleport_time = 1000  # Time for teleportation animation (milliseconds)
        self.teleport_start_time = 0 

        # Remplacez (x, y) par les coordonnées désirées
        self.popup_image = None
        self.popup_start_time = 0
        self.popup_duration = 2000
        self.world_shift = 0
        self.inventaire = Inventaire(surface)
        #level setup
        self.vies_restantes = 3
        self.coeurs_pleins = []  
        self.coeurs_vides = [] 
        
        for i in range(self.vies_restantes):
            coeur_plein = pygame.image.load('assets/ImagesTri-Armor/EffetsTri-Armor/coeur.png')
            coeur_plein = pygame.transform.scale(coeur_plein, (50, 50))
            self.coeurs_pleins.append(coeur_plein)

            coeur_vide = pygame.image.load('assets/ImagesTri-Armor/EffetsTri-Armor/coeur_vide.png')
            coeur_vide = pygame.transform.scale(coeur_vide, (50, 50))
            self.coeurs_vides.append(coeur_vide)
        self.player_start_pos = (232, 232)  # Mettez à jour avec la position de départ réelle
        self.game_instance = game_instance
        self.niveau_termine = False
        self.message_temporaire = None    
        self.complete_flour = True
        self.complete_egg = True
        self.complete_water = True
        self.complete_beurre = True
        self.player = pygame.sprite.GroupSingle(Player(self.player_start_pos, self.inventaire)) # Définit le nombre initial de vies restantes
        self.perdu = False 

        self.enemies = pygame.sprite.Group()
        self.mouette = pygame.sprite.Group()
        self.boss_final = pygame.sprite.GroupSingle()

        self.texture_X = pygame.image.load('assets/sand.png')
        self.texture_X = pygame.transform.scale(self.texture_X, (tile_size, tile_size))
        #level setup
        self.screen = surface
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.run_jeu = True

 # Remplacez {} par votre structure de données d'inventaire réelle
    def retourner_au_menu_principal(self):
        self.game_instance.menu()

    def setup_level(self, layout):
        

        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.beurres = pygame.sprite.Group()
        self.egg = pygame.sprite.Group()
        self.flour = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.boss_final = pygame.sprite.Group()
        self.mouette = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    tile.image = self.texture_X
                    self.tiles.add(tile)
                elif cell == 'P':
                    player_sprite = Player((x, y), self.inventaire)  # Passez self.inventaire ici
                    self.player = pygame.sprite.GroupSingle(player_sprite)
                    print(f'x{x} ,{y}')
                elif cell == 'B':
                    
                    beurre_instance = Beurre(x, y, 'assets/ImagesTri-Armor/ItemsTri-Armor/butter.png')
                    self.beurres.add(beurre_instance)
                elif cell == 'E':
                    beurre_instance = Egg(x, y, 'assets/ImagesTri-Armor/ItemsTri-Armor/egg.png')
                    self.egg.add(beurre_instance)
                elif cell == 'F':
                    beurre_instance = Flour(x, y, 'assets/ImagesTri-Armor/ItemsTri-Armor/flour.png')
                    self.flour.add(beurre_instance)
                elif cell == 'W':
                    beurre_instance = Water(x, y, 'assets/ImagesTri-Armor/ItemsTri-Armor/water.png')
                    self.water.add(beurre_instance)
                
                elif cell == 'C':  # Supposons que 'C' représente un ennemi dans votre layout
                    x = col_index * tile_size  # Obtenez la position X de l'emplacement actuel
                    y = row_index * tile_size # Obtenez la position Y de l'emplacement actuel
                    min_x = x-100
                    max_x = x+100
                    enemy = Enemy((x, y), min_x, max_x)
                    self.enemy.add(enemy)
                elif cell == 'M':  # Supposons que 'C' représente un ennemi dans votre layout
                    x = col_index * tile_size  # Obtenez la position X de l'emplacement actuel
                    y = row_index * tile_size # Obtenez la position Y de l'emplacement actuel
                    min_x = x-100
                    max_x = x+100
                    mouette = Mouette((x, y), min_x, max_x)
                    
                    self.enemy.add(mouette)
                
                elif cell == 'Z':  # Utilisez une lettre spécifique pour représenter le boss dans votre niveau
                    x = col_index * tile_size  # Obtenez la position X de l'emplacement actuel
                    y = row_index * tile_size # Obtenez la position Y de l'emplacement actuel
                    min_x = x-100
                    max_x = x+100

                    boss = BossFinal((x, y), min_x, max_x)
                    self.boss_final.add(boss)
                
                
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5


    def horizontal_mouvement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right 
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left


    def vertical_mouvement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        enemy = self.enemy.sprites()
        mouette = self.mouette.sprites()
        # player.rect.y += player.direction.y * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.rect.colliderect(enemy.rect):
                    perso.personnage.vie -= 1
        for enemy in self.enemy.sprites():  # Utilisez .sprites() pour obtenir une liste des sprites dans le groupe
            if player.rect.colliderect(enemy.rect):
                perso.personnage.vie -= 1
    def score_jeu(self):
        # Couleur du texte
        couleur_texte = (148, 148, 48)  # Blanc
        # Police du texte
        police = pygame.font.Font(None, 36)

        # Créer le texte
        texte_score = police.render(f"Score: {self.player.sprite.score}", True, couleur_texte)
        # Position du texte (en haut à gauche)
        position = (10, 10)
        # Afficher le texte sur l'écran
        self.display_surface.blit(texte_score, position)
        # Exemple d'utilisation : score.s.score = 10
        
    def timer_jeu(self, temps_debut):
        temps_actuel = pygame.time.get_ticks()
        temps_ecoule = (temps_actuel - temps_debut) / 1000  # Convertir en secondes
        # Couleur du texte
        couleur_texte = (255, 255, 255)  # Blanc
        # Police du texte
        police = pygame.font.Font(None, 36)

        # Convertir le temps en minutes:secondes
        minutes = int(temps_ecoule / 60)
        secondes = int(temps_ecoule % 60)
        texte_timer = f"Temps: {minutes:02d}:{secondes:02d}"

        # Créer le texte
        surface_texte = police.render(texte_timer, True, couleur_texte)
        # Position du texte (en haut à droite)
        position = (self.display_surface.get_width() - surface_texte.get_width() - 10, 10)
        # Afficher le texte sur l'écran
        self.display_surface.blit(surface_texte, position)

    def vie_jeu(self):
        # Nombre total de vies
        nombre_total_vies = 3

        # Taille de l'image du coeur
        taille_coeur = (50, 50)
        espacement = 10  # Espace entre les cœurs

        # Calculer la largeur totale de tous les cœurs avec l'espacement
        largeur_totale_coeurs = nombre_total_vies * taille_coeur[0] + (nombre_total_vies - 1) * espacement

        # Position de départ des cœurs pour les centrer
        x = (self.display_surface.get_width() - largeur_totale_coeurs) // 2
        y = 10  # Position Y (en haut de l'écran)

        # Afficher les cœurs
        for i in range(self.vies_restantes):
            x_position = x + i * (taille_coeur[0] + espacement - 20)
            if i < self.vies_restantes:
                self.display_surface.blit(self.coeurs_pleins[i], (x_position, y))
            else:
                self.display_surface.blit(self.coeurs_vides[i], (x_position, y))
                # Vérifiez si le joueur est mort
        if perso.personnage.vie <= 0:
            # Décrémentez le nombre de vies restantes
            self.vies_restantes -= 1
            if self.vies_restantes <= 0:
                # Si le joueur n'a plus de vies, affichez un écran de défaite
                self.afficher_message_perdu()
            else:
                # S'il reste des vies, réinitialisez le niveau
                self.reset_level()

    def compteur(self):
        espacement = 10  # Espace entre les images
        taille_image = (50, 50)  # Taille des images
        x_base = espacement  # Position de départ en x
        y_base = self.display_surface.get_height() - taille_image[1] - espacement  # Position en y

        # Police pour les nombres
        police = pygame.font.Font(None, 24)

        # Liste des images et des nombres à afficher
        images_et_nombres = [

            (self.image_beurre, objets.beurre.nombre),
            (self.image_egg, objets.egg.nombre),
            (self.image_flour, objets.flour.nombre),
            (self.image_water, objets.water.nombre)
        ]

        for i, (image_surface, nombre) in enumerate(images_et_nombres):
            # Position de l'image
            x = x_base + (taille_image[0] + espacement) * i +10
            y = y_base - 20

            # Redimensionner et afficher l'image
            image_redimensionnee = pygame.transform.scale(image_surface, taille_image)
            self.display_surface.blit(image_redimensionnee, (x, y))

            # Afficher le nombre
            texte_nombre = police.render(str(nombre)+ "/10", True, (255, 255, 255))
            self.display_surface.blit(texte_nombre, (x, y + taille_image[1]))


    def en_vie(self):
        player = self.player.sprite
        # Vérifier si le joueur est sorti de l'écran
        if player.rect.top > self.display_surface.get_height() or player.rect.right < 0 or player.rect.left > self.display_surface.get_width():
            self.game_over()
        if perso.personnage.vie <= 0:
            self.vies_restantes -= 1  # Décrémente le nombre de vies restantes
            if self.vies_restantes <= 0:
                self.game_over()


    def game_over(self):
        self.vies_restantes -= 1  # Réduit le nombre de vies restantes
        if self.vies_restantes <= 0:
            # Si le joueur n'a plus de vies, définissez la variable perdu à True
            self.perdu = True
            self.reset_level()
        else:
            # S'il reste des vies, réinitialisez le niveau
            pass
        # Paramètres de l'écran de fin
        font = pygame.font.Font("assets\Font_arcade_classic_2\VCR_OSD_MONO_1.001.ttf", 50)
        text = font.render('Vous êtes mort', True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.display_surface.get_width() / 2, self.display_surface.get_height() / 2))

        # Paramètres du bouton de sortie
        bouton_font = pygame.font.Font("assets\Font_arcade_classic_2\VCR_OSD_MONO_1.001.ttf", 36)
        bouton_quit_text = bouton_font.render('Quitter', True, (255, 255, 255))
        bouton_quit_rect = bouton_quit_text.get_rect(center=(self.display_surface.get_width() / 2, self.display_surface.get_height() / 2 + 50))

        # Paramètres du bouton "Réessayer"
        font = pygame.font.Font("assets\Font_arcade_classic_2\VCR_OSD_MONO_1.001.ttf", 50)
        bouton_retry_text = bouton_font.render('Utiliser une vie', True, (255, 255, 255))
        bouton_retry_rect = bouton_retry_text.get_rect(center=(self.display_surface.get_width() / 2, self.display_surface.get_height() / 2 + 100))

        # Dessiner l'écran de fin
        self.display_surface.fill((0, 0, 0))  # Fond noir
        self.display_surface.blit(text, text_rect)
        self.display_surface.blit(bouton_quit_text, bouton_quit_rect)
        self.display_surface.blit(bouton_retry_text, bouton_retry_rect)

        # Vérifier les interactions de l'utilisateur
        run = True
        while run:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_quit_rect.collidepoint(event.pos):
                        self.run_jeu = False
                        run = False
                    elif bouton_retry_rect.collidepoint(event.pos):
                        self.reset_game()
                        run = False
    def reset_level(self):
        perso.personnage.vie = 100
        self.run_jeu = True  # Recréer une nouvelle instance de Level
        objets.flour.nombre = 0
        objets.water.nombre = 0
        objets.beurre.nombre = 0
        objets.egg.nombre = 0
    def reset_game(self):
        # Réinitialiser la position du joueur et sa vie
        self.player.sprite.rect.topleft = self.player_start_pos
        perso.personnage.vie = 100  # Réinitialiser la vie
        self.run_jeu = True     


    def check_map_completion(self):

        if objets.flour.nombre >= 10 and self.complete_flour == True:
            self.complete_map()
            self.complete_flour = False
        elif objets.beurre.nombre >= 10 and self.complete_beurre == True:
            self.complete_map()
            self.complete_beurre = False
        elif objets.water.nombre >= 10 and self.complete_water == True:
            self.complete_map()
            self.complete_water = False
        elif objets.egg.nombre >= 10 and self.complete_egg == True:
            self.complete_map()
            self.complete_egg = False


    def check_item_collisions(self):
        player = self.player.sprite
        for beurre in self.beurres.copy():
            if player.rect.colliderect(beurre.rect):
                player.collect_item("beurre")  # Collecte l'objet
                self.beurres.remove(beurre)
                objets.beurre.nombre += 1
                self.pop_up_items(self.pop_up_beurre)
        for egg in self.egg.copy():
            if player.rect.colliderect(egg.rect):
                player.collect_item("egg")  # Collecte l'objet
                self.egg.remove(egg)
                objets.egg.nombre += 1
                self.pop_up_items(self.pop_up_egg)
        for flour in self.flour.copy():
            if player.rect.colliderect(flour.rect):
                player.collect_item("flour")  # Collecte l'objet
                self.flour.remove(flour)
                objets.flour.nombre += 1
                self.pop_up_items(self.pop_up_flour)
        for water in self.water.copy():
            if player.rect.colliderect(water.rect):
                player.collect_item("water")  # Collecte l'objet
                self.water.remove(water)
                objets.water.nombre += 1
                self.pop_up_items(self.pop_up_water)
        
        for enemy in self.enemy: 
            if player.rect.colliderect(enemy.rect):
                player.collect_item("enemy")  # Collecte l'objet
                if player.rect.colliderect(enemy.rect):
                    perso.personnage.vie -= 1
        for mouette in self.mouette: 
            if player.rect.colliderect(mouette.rect):
                player.collect_item("mouette")  # Collecte l'objet
                if player.rect.colliderect(mouette.rect):
                    perso.personnage.vie -= 1

        self.check_map_completion()
       #self.game_instance.changer_niveau(prochain_niveau)
        
    def verification(self):
        if objets.flour.nombre == 10 and objets.water.nombre == 10 and objets.beurre.nombre == 10 and objets.egg.nombre == 10:
            self.pop_up_items(self.pop_up_fin)
            # Définir un fond noir pour l'écran
            self.display_surface.fill((0, 0, 0))
            # Créer le texte de félicitations
            font = pygame.font.Font(None, 50)
            message_felicitation = font.render("Félicitations ! Vous avez récupéré la recette secrète.", True, (255, 255, 255))

            message_rect = message_felicitation.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2 - 100))
            pygame.mixer.music.load('assets\music\Tri-Yann-Le-Loup_-le-Renard-et-la-Belette-_La-Jument-de-Michao_.mp3')  # Remplacer avec le chemin de votre fichier audio
            pygame.mixer.music.play() 
            # Créer le bouton de sortie
            bouton_font = pygame.font.Font(None, 36)
            bouton_text = bouton_font.render('Quitter', True, (255, 255, 255))
            bouton_rect = bouton_text.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2 + 50))

            # Afficher l'image de fond, le texte et le bouton
            self.display_surface.blit(self.image_fond , self.image_fond_rect)
            self.display_surface.blit(message_felicitation, message_rect)
            self.display_surface.blit(bouton_text, bouton_rect)

            pygame.display.flip()
        else: 
            print("Vous avez pas les objets")

    def boss_colision(self):
        player = self.player.sprite
        for boss in self.boss_final:
            if player.rect.colliderect(boss.rect):
                print("Collision avec le boss détectée!")
                self.verification()
                # Afficher l'image du téléporteur
                self.popup_start_time = pygame.time.get_ticks()
            
    def complete_map(self):
        if not self.niveau_termine:
            self.niveau_termine = True
            
            # Afficher un message de victoire
            font = pygame.font.Font("assets\Font_arcade_classic_2\VCR_OSD_MONO_1.001.ttf", 50)

            message_victoire = pygame.image.load('assets/ImagesTri-Armor/ArrierePlanTri-Armor/popup_niveau-termine.png')
            message_rect = message_victoire.get_rect(center=(self.display_surface.get_width() / 2, self.display_surface.get_height() / 2))
            self.display_surface.blit(message_victoire, message_rect)
            pygame.display.update()
            
            # Jouer un son de    victoire (remplacer 'chemin_vers_son_victoire.wav' par le chemin de votre fichier son)
            son_victoire = pygame.mixer.Sound('assets/music/4991.mp3')
            son_victoire.play()
            pygame.time.wait(3000)
            GameState.maps_deverrouillees[2] = True

        # Attendre un moment avant de passer à l'écran suivant
        

        # Changer l'état du jeu pour passer à l'écran suivant
        # Par exemple, si vous avez une méthode pour changer de niveau :
        # self.changer_niveau_suivant()

        # Ou revenir au menu principal
            

        # Si vous avez un système de sauvegarde, sauvegarder la progression
        # self.sauvegarder_progression()    
            
    def afficher_message_perdu(self):
        font = pygame.font.Font("assets\Font_arcade_classic_2\VCR_OSD_MONO_1.001.ttf", 50)
        message_perdu = font.render('Vous avez perdu', True, (255, 255, 255))
        message_rect = message_perdu.get_rect(center=(self.display_surface.get_width() / 2, self.display_surface.get_height() / 2))

        font = pygame.font.Font("assets\Font_arcade_classic_2\VCR_OSD_MONO_1.001.ttf", 36)
        bouton_menu_text = font.render('Menu', True, (255, 255, 255))
        bouton_menu_rect = bouton_menu_text.get_rect(center=(self.display_surface.get_width() / 2, self.display_surface.get_height() / 2 + 100))
        # Dessiner l'écran de perte
        self.display_surface.fill((0, 0, 0))  # Fond noir
        self.display_surface.blit(message_perdu, message_rect)
        self.display_surface.blit(bouton_menu_text, bouton_menu_rect)

        # Vérifier les interactions de l'utilisateur
        run = True
        while run:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_menu_rect.collidepoint(event.pos):
                        self.run_jeu = False  # Ajoutez cette fonction pour revenir au menu
                        run = False
            
    def pop_up_items(self, popup_image):
        """Affiche une pop-up en haut de l'écran avec l'image spécifiée."""

        scaled_size = (popup_image.get_width() // 2, popup_image.get_height() // 2)
        self.popup_image = pygame.transform.scale(popup_image, scaled_size)
        self.popup_start_time = pygame.time.get_ticks()
    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5
  
    
    def run(self):

        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        
        self.scroll_x()
        self.player.update()
        self.compteur()
        self.horizontal_mouvement_collision()
        self.vertical_mouvement_collision()
        self.player.draw(self.display_surface)

        self.enemy.update(self.world_shift)
        self.enemy.draw(self.display_surface)

        self.mouette.update(self.world_shift)
        self.mouette.draw(self.display_surface)

        self.boss_final.update(self.world_shift)
        self.boss_final.draw(self.display_surface)
        
        self.beurres.update(self.world_shift)
        self.beurres.draw(self.display_surface)

        self.egg.update(self.world_shift)
        self.egg.draw(self.display_surface)
        self.flour.update(self.world_shift)
        self.flour.draw(self.display_surface)

# Permet de passer les vérifications pour passer les niveaux avec la touche "P"         
#        objets.flour.nombre = 10
#        objets.water.nombre = 10
#        objets.beurre.nombre = 10
#        objets.egg.nombre = 10

        self.water.update(self.world_shift)
        self.water.draw(self.display_surface)

        if self.perdu:
            self.afficher_message_perdu()
            
        self.check_item_collisions()
        
        if self.niveau_termine and self.message_temporaire:
            message_victoire, message_rect, start_time, duree = self.message_temporaire
            if pygame.time.get_ticks() - start_time < duree:
                self.display_surface.blit(message_victoire, message_rect)
            else:
                self.message_temporaire = None

        

        self.boss_colision()
        
        self.score_jeu()
        self.timer_jeu(self.temps_debut)
        self.vie_jeu()
        self.en_vie()


        current_time = pygame.time.get_ticks()
        if self.popup_image and current_time - self.popup_start_time < self.popup_duration:
            # Afficher la pop-up
            popup_rect = self.popup_image.get_rect(center=(self.display_surface.get_width() // 2, 100))
            self.display_surface.blit(self.popup_image, popup_rect)
        else:
            self.popup_image = None  # Réinitialiser la pop-up une fois le temps écoulé