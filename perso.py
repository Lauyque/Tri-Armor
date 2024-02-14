class Perso:

    def __init__(self, vie, degats, vitesse) -> None:
        self.vie = vie
        self.degats = degats
        self.vitessse = vitesse
        self.bouclier = False # Pas de bouclier au début


personnage = Perso(100,0,0)