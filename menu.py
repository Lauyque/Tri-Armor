
import pygame
import pygame_menu
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import pygame_widgets
import pygame.freetype
import mainNathan


class Menu:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.largeur_surface = 900
        self.hauteur_surface = 800

        self.surface = pygame.display.set_mode((self.largeur_surface, self.hauteur_surface))

        self.screen = pygame.display.set_mode((self.largeur_surface, self.hauteur_surface))
        
        self.mondes_debloques = {
            1: True,  # Le monde 1 est toujours débloqué
            2: False,
            3: False,
            4: False
        }

        # Volume de base pour la music
        self.volume = 50

        # Initialiser le mixer de pygame et jouer la musique
        pygame.mixer.init()
        pygame.mixer.music.load('assets/music/Everdell _ Ambiance Music __ Musique dambiance _.mp3')  # Remplacez par le chemin de votre fichier
        pygame.mixer.music.play(-1)  # Jouer en boucle
        pygame.mixer.music.set_volume(self.volume / 100.0)  # Définir le volume initial

        # Chargement de l'image de fond
        self.background_image = pygame.image.load("assets/ImagesTri-Armor/ArrièrePlanTri-Armor/Menu.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.largeur_surface, self.hauteur_surface))

       # Police
        font_path = "assets/Font_arcade_classic_2/ARCADECLASSIC.TTF"
        self.font = pygame.font.Font(font_path, 30)

        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.TRANSPARENT = (0,0,0,128)
        

        self.afficher_menu()


    def afficher_menu(self):
        running = True
        while running:
            self.surface.blit(self.background_image, (0, 0))

            # Dessiner les boutons
            jouer_button = self.draw_button('Jouer', (self.largeur_surface // 2, 180),self.WHITE, self.BLACK)
            niveau_button = self.draw_button('Niveaux', (self.largeur_surface // 2, 285),self.WHITE, self.BLACK)
            option_button = self.draw_button('Option', (self.largeur_surface // 2, 377),self.WHITE, self.BLACK)
            quitter_button = self.draw_button('Quitter', (self.largeur_surface // 2, 471),self.WHITE, self.BLACK)
            titre_button = self.draw_button("Tri Armor", (100, 25),self.WHITE, self.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if jouer_button.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        self.Jouer()
                        pygame.mixer.music.load('assets/music/Everdell _ Ambiance Music __ Musique dambiance _.mp3')  # Remplacez par le chemin de votre fichier
                        pygame.mixer.music.play(-1)  # Jouer en boucle
                    elif niveau_button.collidepoint(event.pos):
                        self.Niveau()
                        pygame.mixer.music.load('assets/music/Everdell _ Ambiance Music __ Musique dambiance _.mp3')  # Remplacez par le chemin de votre fichier
                        pygame.mixer.music.play(-1)  # Jouer en boucle
                    elif option_button.collidepoint(event.pos):
                        self.Option()
                    elif quitter_button.collidepoint(event.pos):
                        running = False # Quitter le jeu
                    elif titre_button.collidepoint(event.pos):
                        self.titre()
                
                pygame.display.flip()  # Mise à jour de l'écran après avoir dessiné les boutons
        pygame.quit()

    def Jouer(self ):
        mainNathan.jeu(1, self)
        pygame.display.set_mode((self.largeur_surface, self.hauteur_surface))



    def Niveau(self):
        # Initialiser les widgets
        self.surface.fill((135,206,250))
        # Background
        # Charger l'image de fond
        background_image = pygame.image.load('assets/ImagesTri-Armor/ArrièrePlanTri-Armor/parchemin.png')
        # Redimensionner l'image pour qu'elle s'adapte à la taille de la surface
        background_image = pygame.transform.scale(background_image, (self.largeur_surface, self.hauteur_surface))
        self.surface.blit(background_image, (0, 0))

        # Créer une police pour les titres
        font = pygame.font.Font("assets\Font_arcade_classic_2\VCR_OSD_MONO_1.001.ttf", 40)
        # Titre de la page des options
        niveau_title = font.render('Niveaux', True, (0, 0, 0))

        worlds = []
        for i, (title, image_path) in enumerate([
            ('Monde 1', 'assets/ImagesTri-Armor/ArrièrePlanTri-Armor/daytime.png'), 
            ('Monde 2', 'assets/ImagesTri-Armor/ArrièrePlanTri-Armor/sunset2.png'),
            ('Monde 3', 'assets/ImagesTri-Armor/ArrièrePlanTri-Armor/MoonNight.png'), 
            ('Monde 4', 'assets/ImagesTri-Armor/ArrièrePlanTri-Armor/MoonNight2.png')]):
            
            x, y = [150, 550][i % 2], [150, 410][i // 2]
            if self.mondes_debloques[i + 1]:
                rect = self.draw_square(x, y, title, image_path)
            else:
                rect = self.draw_square_with_effect(x, y, title, image_path)  # Appliquer un effet visuel
            worlds.append(rect)


        run = True
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False  # Quitter les options avec la touche ECHAP
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(worlds):
                        if rect.collidepoint(event.pos):  # Vérifier si le monde est débloqué
                            pygame.mixer.music.stop()
                            mainNathan.jeu(i + 1, self)  # Passer 'self' comme argument
                            pygame.display.set_mode((self.largeur_surface, self.hauteur_surface))
                            run = False
            # Afficher les titres
            self.surface.blit(niveau_title, (325, 50))

            pygame_widgets.update(events)
            pygame.display.update()

    def debloquer_monde(self, monde_num):
        if monde_num in self.mondes_debloques:
            self.mondes_debloques[monde_num] = True

    def draw_square_with_effect(self, x, y, text, image_path):
        font = pygame.font.Font("assets\Font_arcade_classic_2\VCR_OSD_MONO_1.001.ttf", 28)
        rect = pygame.Rect(x, y, 200, 200)
        pygame.draw.rect(self.surface, (255, 255, 255), rect)  # dessiner le carré

        # Charger l'image
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (200, 200))  # Redimensionner l'image

        # Appliquer un effet de réduction de l'opacité
        image.set_alpha(128)  # Réduire l'opacité (valeur entre 0 et 255)

        self.surface.blit(image, (x, y))  # Dessiner l'image modifiée

        # Dessiner le texte en bas du carré
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x + 100, y + 220))  # Position ajustée pour le bas du carré
        self.surface.blit(text_surface, text_rect)

        return rect

    def Option(self):
    # Définir la couleur de fond
        self.surface.fill((210, 180, 140))  # Couleur beige pour le fond
        
        # Créer une police pour les titres
        font = pygame.font.Font(None, 40)  # Utilisez la police souhaitée ici
        
        # Créer un thème pour les sliders
        theme = pygame_menu.Theme(
            background_color=(210, 180, 140, 100),  # Couleur de fond (RGBA)
            title=False,  # Désactiver l'affichage du titre
            widget_font_color=(0, 0, 0),
            widget_background_color=(255, 255, 255, 0),  # Fond transparent pour les widgets
            selection_color=(0, 0, 0)  # Couleur de sélection noire pour les sliders
        )
        
        # Créer un menu d'options avec le thème personnalisé
        options_menu = pygame_menu.Menu(
            title='',
            width=300,
            height=400,
            theme=theme,
            center_content=False
        )
        
        # Ajouter les sliders de musique et d'effets sonores au menu
        options_menu.add.label('Musique', max_char=-1, font_size=25)
        options_menu.add.range_slider('', default=self.volume, range_values=(0, 100), increment=1, onchange=self.on_volume_change, slider_id='music_slider')
        options_menu.add.label('SFX', max_char=-1, font_size=25)
        options_menu.add.range_slider('', default=self.volume, range_values=(0, 100), increment=1, onchange=self.on_volume_change, slider_id='sfx_slider')
        while True:
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return  # Retourner au menu principal
            
            # Dessiner le fond à chaque frame
            self.surface.fill((210, 180, 140))  # Couleur beige pour le fond

            # Exécuter le menu d'options
            options_menu.update(events)
            options_menu.draw(self.surface)
            
            pygame.display.flip()  # Mettre à jour l'écran
    def draw_background(self):
            self.surface.fill((210, 180, 140)) # Couleur beige pour le fond

    def on_volume_change(self, value, **kwargs):
        # Mettre à jour le volume
            self.volume = value
            pygame.mixer.music.set_volume(value / 100.0)

    
# Fonctions pour dessiner les boutons
    def draw_button(self, text, position, button_color, text_color):
        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=position)
        button_rect = text_surf.get_rect(center=position)  # Utilisez inflate() si vous voulez un bouton plus grand que le texte
        button_rect.inflate_ip(20, 10)  # Inflation pour avoir un peu d'espace autour du texte
        pygame.draw.rect(self.surface, button_color, button_rect)  # Dessine un rectangle pour le bouton
        self.surface.blit(text_surf, text_rect)  # Dessine le texte
        return button_rect  # Renvoie le rectangle si vous avez besoin de gérer les clics

    # Fonction pour dessiner un carré
    def draw_square(self, x, y, text, image_path):

        font = pygame.font.Font("assets\Font_arcade_classic_2\VCR_OSD_MONO_1.001.ttf", 28)
        rect = pygame.Rect(x, y, 200, 200)
        pygame.draw.rect(self.surface, (255, 255, 255), rect)  # dessiner le carré

        # Charger et dessiner l'image
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (200, 200))  # Redimensionner l'image pour qu'elle s'adapte au carré
        self.surface.blit(image, (x, y))

        # Dessiner le texte en bas du carré
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x + 100, y + 220))  # Position ajustée pour le bas du carré
        self.surface.blit(text_surface, text_rect)

        return rect
    
    def titre(self):
        # Initialiser les widgets
        self.surface.fill((135,206,250))
        # Background
        # Charger l'image de fond
        background_image = pygame.image.load('assets/ImagesTri-Armor/ArrièrePlanTri-Armor/parchemin.png')
        # Redimensionner l'image pour qu'elle s'adapte à la taille de la surface
        background_image = pygame.transform.scale(background_image, (self.largeur_surface, self.hauteur_surface))
        self.surface.blit(background_image, (0, 0))

        # Créer une police pour les titres
        font = pygame.font.Font("assets\Font_arcade_classic_2\VCR_OSD_MONO_1.001.ttf", 40)
        # Titre de la page des options
        niveau_title = font.render('Credits', True, (0, 0, 0))
        c1 = font.render('LE DOHER Loic', True, (0, 0, 0))
        c2 = font.render('LABARCHE Nathan', True, (0, 0, 0))
        c3 = font.render('LAAKAD Yanis', True, (0, 0, 0))
        c4 = font.render('TURNA Musa', True, (0, 0, 0))
        c5 = font.render('PORLIER Florent', True, (0, 0, 0))

        run = True
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False  # Quitter les options avec la touche ECHAP

            # Afficher les titres
            self.surface.blit(niveau_title, (325, 50))
            self.surface.blit(c1, (150, 200))
            self.surface.blit(c2, (150, 275))
            self.surface.blit(c3, (150, 350))
            self.surface.blit(c4, (150, 425))
            self.surface.blit(c5, (150, 500))

            pygame_widgets.update(events)
            pygame.display.update()