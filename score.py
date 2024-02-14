
class Score:

    def __init__(self, score) -> None:
        self.score = score

    # Augmentation du score
    def score_add(self, nombre):
        self.score += nombre

    # Diminution du score
    def score_del(self, nombre):
        self.score -= nombre


s = Score(0)