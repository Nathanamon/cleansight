"""
Classification de caractéristiques visuelles par règles conditionnelles modifiables.
Chaque règle est définie sous forme de dictionnaire avec :
    - un nom
    - une condition (fonction booléenne prenant les features)
    - un message ou tag associé

Les règles peuvent être modifiées dynamiquement : ajout, suppression, désactivation.
Elles peuvent aussi être chargées dynamiquement depuis un fichier JSON.
"""
from typing import Callable, Dict, List, Any, Optional
import json
import operator

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
RULES: List[Rule] = []


# ────────────────────────────────────────────────────────────────────────────────
# Chargement des règles depuis un fichier JSON
# ────────────────────────────────────────────────────────────────────────────────
OPERATORS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
}

def load_rules_from_json(json_path: str):
    """Charge des règles depuis un fichier JSON"""
    global RULES
    RULES.clear()
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for rule_data in data:
            name = rule_data["name"]
            message = rule_data["message"]
            enabled = rule_data.get("enabled", True)
            conditions = rule_data["conditions"]  # liste de conditions simples

            def make_condition(conds):
                return lambda features: all(
                    OPERATORS[c["op"]](features[c["key"]], c["value"]) for c in conds
                )

            RULES.append(Rule(name, make_condition(conditions), message, enabled))


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


def classify_image(features: Dict[str, Any]) -> Optional[str]:
    """
    Classification simple : retourne "pleine", "vide" ou None.
    Basé sur les règles définies.
    """
    if any(rule.name == "poubelle_pleine" and rule.evaluate(features) for rule in RULES):
        return "pleine"
    elif any(rule.name == "poubelle_vide" and rule.evaluate(features) for rule in RULES):
        return "vide"
    return None


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
    from feature_extraction import extract_features
    import argparse

    parser = argparse.ArgumentParser(description="Appliquer des règles sur une image.")
    parser.add_argument("image_path", help="Chemin vers l’image à analyser")
    parser.add_argument("--rules", help="Chemin vers un fichier JSON de règles", required=True)
    args = parser.parse_args()

    load_rules_from_json(args.rules)
    features = extract_features(args.image_path, resize=True)
    if features:
        label = classify_image(features)
        actions = apply_rules(features)
        print("\n\n✅ Recommandations :")
        for a in actions:
            print(" -", a)
        print(f"\n🧾 Label automatique : {label or 'non déterminé'}")
    else:
        print("❌ Extraction impossible")
