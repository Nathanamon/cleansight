"""
Classification de caractéristiques visuelles par règles conditionnelles modifiables.
Chaque règle est définie sous forme de dictionnaire avec :
    - un nom
    - une condition (fonction booléenne prenant les features)
    - un message ou tag associé

Les règles peuvent être modifiées dynamiquement : ajout, suppression, désactivation.
"""
from typing import Callable, Dict, List, Any

# ────────────────────────────────────────────────────────────────────────────────
# Définition d'une règle : nom, condition (fonction), message
# ────────────────────────────────────────────────────────────────────────────────
class Rule:
    def __init__(self, name: str, condition: Callable[[Dict], bool], message: str, enabled: bool = True):
        self.name = name
        self.condition = condition
        self.message = message
        self.enabled = enabled

    def evaluate(self, features: Dict[str, Any]) -> bool:
        return self.enabled and self.condition(features)


# ────────────────────────────────────────────────────────────────────────────────
# Liste de règles simples (modifiable dynamiquement)
# ────────────────────────────────────────────────────────────────────────────────
RULES: List[Rule] = [
    Rule(
        name="image_trop_petite",
        condition=lambda f: f["width"] < 300 or f["height"] < 300,
        message="Image trop petite – vérifier la résolution de la caméra",
    ),
    Rule(
        name="faible_contraste",
        condition=lambda f: f["rms_contrast"] < 20,
        message="Contraste faible – possible flou ou obscurité",
    ),
    Rule(
        name="peu_de_contours",
        condition=lambda f: f["contour_count"] < 5,
        message="Peu de contours – contenu mal détecté ou vide",
    ),
    Rule(
        name="dominante_rouge",
        condition=lambda f: f["mean_r"] > 180 and f["mean_r"] > f["mean_g"] + 40,
        message="Dominante rouge – vérifier conditions d’éclairage",
    ),
    Rule(
        name="fichier_lourd",
        condition=lambda f: f["file_size"] > 300_000,
        message="Fichier trop lourd – compression ou redimensionnement recommandé",
    ),
]


# ────────────────────────────────────────────────────────────────────────────────
# Application des règles à un dictionnaire de features
# ────────────────────────────────────────────────────────────────────────────────
def apply_rules(features: Dict[str, Any]) -> List[str]:
    """
    Applique toutes les règles activées au dictionnaire de caractéristiques.

    Returns:
        Liste de messages correspondant aux règles déclenchées.
    """
    return [rule.message for rule in RULES if rule.evaluate(features)]


# ────────────────────────────────────────────────────────────────────────────────
# Interface de modification dynamique (optionnelle)
# ────────────────────────────────────────────────────────────────────────────────
def enable_rule(name: str):
    for rule in RULES:
        if rule.name == name:
            rule.enabled = True


def disable_rule(name: str):
    for rule in RULES:
        if rule.name == name:
            rule.enabled = False


def add_rule(name: str, condition: Callable[[Dict], bool], message: str):
    RULES.append(Rule(name, condition, message))


def remove_rule(name: str):
    global RULES
    RULES = [r for r in RULES if r.name != name]


# ────────────────────────────────────────────────────────────────────────────────
# Utilisation rapide (debug/test)
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from extract_features import extract_features
    import argparse

    parser = argparse.ArgumentParser(description="Appliquer des règles sur une image.")
    parser.add_argument("image_path", help="Chemin vers l’image à analyser")
    args = parser.parse_args()

    features = extract_features(args.image_path, resize=True)
    if features:
        actions = apply_rules(features)
        print("\n\n✅ Recommandations :")
        for a in actions:
            print(" -", a)
    else:
        print("❌ Extraction impossible")
