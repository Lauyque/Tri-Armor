

def wrap_text(text, font, max_width, margin=100):
    """ Diviser un texte en lignes en fonction de la largeur maximale moins la marge. """
    max_width -= margin  # Réduire la largeur maximale par la marge
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:  # S'assurer que la ligne courante n'est pas vide
                lines.append(current_line)
            current_line = word + ' '
    if current_line:  # Ajouter la dernière ligne si elle n'est pas vide
        lines.append(current_line)
    return lines


