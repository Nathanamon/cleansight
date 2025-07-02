# backend/classification.py

def classify_image(features):
    # Règles simples d’exemple : à ajuster ou remplacer par ML
    if features["taille"] > 100_000 and features["contraste"] < 0.3:
        return "pleine"
    return "vide"
