import os
from PIL import Image as PILImage
import numpy as np

def extract_features(path):
    """
    Lit l'image, renvoie un dict:
      - taille (octets)
      - largeur, hauteur (px)
      - contraste (écart-type de luminance normalisé)
      - couleur_moyenne (R,G,B arrondis)
    """
    pil = PILImage.open(path).convert("RGB")
    arr = np.asarray(pil)

    # Taille du fichier
    taille = os.path.getsize(path)

    # Dimensions
    largeur, hauteur = pil.size

    # Contraste (écart-type des luminances)
    lum = (0.299 * arr[:,:,0] + 0.587 * arr[:,:,1] + 0.114 * arr[:,:,2])
    contraste = float(lum.std()) / 255.0

    # Couleur moyenne
    r, g, b = arr[:,:,0].mean(), arr[:,:,1].mean(), arr[:,:,2].mean()
    couleur_moyenne = f"{r:.1f},{g:.1f},{b:.1f}"

    return {
        "taille": taille,
        "largeur": largeur,
        "hauteur": hauteur,
        "contraste": contraste,
        "couleur_moyenne": couleur_moyenne
    }
