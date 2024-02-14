import pygame, sys
from pygame.locals import *
import pygame_menu
from settings import *
from level import *
import perso
from text import wrap_text
from level import *


class jeu():

    def __init__(self,map, menu_objet):
        # Pygale
        pygame.init()
        self.current_map = map  
        self.map1_completed = True  # Le monde 1 est toujours accessible
        self.map2_completed = True
        self.map3_completed = True
        self.map4_completed = True
        screen_width = 1100
        screen_height = len(level_map) * tile_size
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.current_level = Level(level_map, self.screen, self)
        # Choix de la map et definition des variables en conséquent
        self.map = map
        self.menu = menu_objet 
        self.current_level = Level(level_map, self.screen, self)
        self.fond_image = pygame.image.load('assets/ImagesTri-Armor/ArrièrePlanTri-Armor/space.png')
        self.fond_image = pygame.transform.scale(self.fond_image, (screen_width, screen_height))
        if map == 1:
            screen_height = len(level_map) * tile_size
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
            level = Level(level_map, self.screen,self)
        elif map == 2:
            screen_height = len(level_map2) * tile_size
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
            level = Level(level_map2, self.screen,self)

        elif map == 3:
            screen_height = len(level_map3) * tile_size
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
            level = Level(level_map3, self.screen,self)

                
        elif map == 4:
            screen_height = len(level_map4) * tile_size
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
            level = Level(level_map4, self.screen,self)
        else:
            print("erreur")
        # Volume de base pour la music
        self.volume = 50

        # Initialiser le mixer de pygame et jouer la musique
        pygame.mixer.init()
        pygame.mixer.music.load('assets/music/jeu.mp3')  # Remplacez par le chemin de votre fichier
        pygame.mixer.music.play(-1)  # Jouer en boucle
        pygame.mixer.music.set_volume(self.volume / 100.0) 
        
        
        self.background = pygame.image.load('assets/ImagesTri-Armor/ArrièrePlanTri-Armor/Gameplay_Background.png')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
         # Définir le volume initial

        # Nouvelle page
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
        clock = pygame.time.Clock()
        #map = level_map+self.map

        #level = Level(level_map, self.screen)
        # bg_img = pygame.image.load('assets/main_menu.png')

        # Define these variables here
        self.bouton_reprendre_rect = pygame.Rect(0, 0, 150, 50)
        self.bouton_quitter_rect = pygame.Rect(0, 0, 150, 50)

        # Lancement de l'animation de démarrage (que si monde 1)
        if self.map == 1:
            self.start_animation()
            pygame.mixer.music.load('assets/music/jeu.mp3')  # Remplacez par le chemin de votre fichier
            pygame.mixer.music.play(-1)  # Jouer en boucle
        # bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
        pause = False
        run = True
        while run :
            # screen.blit(bg_img, (0,0))
            self.screen.blit(self.background, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    run = False
                    #pygame.quit()
                    #sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    niveau = self.map +1
                    level = self.changer_niveau(niveau)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause = not pause
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.bouton_reprendre_rect.collidepoint(event.pos):
                        pause = False
                    elif self.bouton_quitter_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        run = False


            if not pause :
                # jeu

                level.run()

            if pause:
                # pause
                self.screen.fill('black')
                self.pause_jeu()

            
            if level.run_jeu == False:
                pygame.mixer.music.stop()
                level.run_jeu = True
                perso.personnage.vie = 100
                run = False
            

            pygame.display.update()
            clock.tick(60)

        
             

    def mark_map1_completed(self):
        self.map1_completed = True

    def pause_jeu(self):
        pause = True
        pygame.mixer.music.pause()  # Mettre la musique en pause

        # Police et couleurs
        police = pygame.font.Font(None, 36)
        NOIR = (0, 0, 0)
        BLANC = (255, 255, 255)
        TRANSPARENT = (0, 0, 0, 128)  # Couleur semi-transparente

        # Fond semi-transparent
        fond_pause = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        fond_pause.fill(TRANSPARENT)

        # Position du pop-up
        popup_rect = pygame.Rect(0, 0, 400, 200)
        popup_rect.center = (screen_width // 2, screen_height // 2)

        # Dessiner le pop-up
        pygame.draw.rect(fond_pause, BLANC, popup_rect)
        self.screen.blit(fond_pause, (0, 0))

        # Texte du pop-up
        texte_reprendre = police.render("Reprendre", True, NOIR)
        texte_quitter = police.render("Quitter", True, NOIR)

        # Position et dessin des boutons
        self.bouton_reprendre_rect.center = (popup_rect.centerx, popup_rect.centery - 30)
        self.bouton_quitter_rect.center = (popup_rect.centerx, popup_rect.centery + 30)
        pygame.draw.rect(self.screen, BLANC, self.bouton_reprendre_rect)
        pygame.draw.rect(self.screen, BLANC, self.bouton_quitter_rect)

        # Afficher le texte des boutons

        self.screen.blit(texte_reprendre, self.bouton_reprendre_rect.move(30, 10))
        self.screen.blit(texte_quitter, self.bouton_quitter_rect.move(30, 10))

        # Mettre à jour l'affichage
        pygame.display.flip()


        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.bouton_reprendre_rect.collidepoint(event.pos):
                        pause = False
                    elif self.bouton_quitter_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()

        pygame.mixer.music.unpause()
    def changer_niveau(self, nouveau_niveau):
        self.map = nouveau_niveau
        # Chargez les données du nouveau niveau

        if self.map == 2:
            screen_height = len(level_map2) * tile_size
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
            level = Level(level_map2, self.screen,self)
        elif self.map == 3:
            screen_height = len(level_map3) * tile_size
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
            level = Level(level_map3, self.screen,self)
        elif self.map == 4:
            screen_height = len(level_map4) * tile_size
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
            level = Level(level_map4, self.screen,self)
        return level
    def start_animation(self):
        pygame.mixer.music.load('assets/voice/ElevenLabs_2024-01-17T22_26_07_Brian - deep narrator_gen_s50_sb75_se0_b_m2.mp3')  # Remplacer avec le chemin de votre fichier audio
        pygame.mixer.music.play() 
         # Jouer l'audio
        text = ("La célèbre pâtissière bretonne, Mam’Goudig, connue pour sa grande "
                "maîtrise culinaire, cachait un grand secret. En effet, elle, qui "
                "d’ordinaire donnait toujours l’impression d’avoir la science infuse "
                "sur toute la culture bretonne, ne connaîtrait pas la recette de "
                "l’extrêmement populaire kouign-amann. Après toutes ces années à "
                "cacher cette honte, elle décida aujourd’hui d’y mettre un terme et "
                "partit donc à l’aventure, à l’endroit où la recette est gardée par "
                "le peuple celtique, le phare de Saint-Mathieu.")
        
        font = pygame.font.Font("assets\Font_arcade_classic_2\VCR_OSD_MONO_1.001.ttf", 36)
        
        wrapped_text = wrap_text(text, font, screen_width)
        y_pos = screen_height
        
        titre = "Le Secret du Kouign-Amann"  # Titre à afficher
        police_titre = pygame.font.Font(None, 50)  # Taille de police pour le titre
        texte_titre = police_titre.render(titre, True, (255, 255, 255))  # Couleur blanche
        texte_titre_rect = texte_titre.get_rect(center=(screen_width//2, 100))
        self.screen.blit(texte_titre, texte_titre_rect)
        while y_pos > -len(wrapped_text) * 40:  # 40 est la hauteur approximative d'une ligne de texte
            self.screen.blit(self.fond_image, (0, 0))  # Fond noir  # Fond noir
            for i, line in enumerate(wrapped_text):
                text_surface = font.render(line, True, (148, 148, 48))

                text_rect = text_surface.get_rect(center=(screen_width / 2, y_pos + i * 40))
                self.screen.blit(text_surface, text_rect) 
            pygame.display.update()
            y_pos -= 1  # Déplacer le texte vers le haut

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return

            pygame.time.wait(25) 
        pygame.mixer.music.stop()  


    def lancer_niveau(self,nouvelle_map):
        self.current_map = nouvelle_map
        screen_height = len(globals()[f'level_map{self.current_map}']) * tile_size
        # Affichage de l'image finale

  # Attendre 2 secondes avant de commencer le jeu