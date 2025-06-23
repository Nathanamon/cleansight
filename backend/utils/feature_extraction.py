"""
Extraction de caractéristiques visuelles simples pour chaque image.

Fonctions renvoyées dans un dict prêt à être envoyé à l’API ou inséré
en BDD.  Toutes les valeurs sont primitives (int / float / list) afin
d’être directement sérialisables en JSON.

Dépendances :
    Pillow   (pip install pillow)
    numpy    (pip install numpy)
    opencv   (pip install opencv-python-headless)  # version headless conseillée
"""

import os
import math
import json
from typing import Dict, Optional, Tuple, List

import numpy as np
from PIL import Image, UnidentifiedImageError
import cv2  # type: ignore

from .image_tools import process_image  # resize + compress (optionnel)


# ────────────────────────────────────────────────────────────────────────────────
# Helpers bas niveau
# ────────────────────────────────────────────────────────────────────────────────
def _file_size(path: str) -> int:
    """Renvoie la taille du fichier en octets."""
    return os.path.getsize(path)


def _dimensions(img: Image.Image) -> Tuple[int, int]:
    """Largeur, hauteur en pixels."""
    return img.size  # (width, height)


def _mean_color(img: Image.Image) -> Tuple[float, float, float]:
    """Moyenne R, G, B sur l’ensemble de l’image (0-255)."""
    arr = np.array(img)
    # Si l’image est en niveaux de gris → étendre sur 3 canaux
    if arr.ndim == 2:
        arr = np.stack([arr] * 3, axis=-1)
    mean_rgb = arr.mean(axis=(0, 1))
    return tuple(float(x) for x in mean_rgb)


def _histogram(img: Image.Image, bins: int = 256) -> List[int]:
    """Histogramme global (R+G+B concaténés) – 256*3 = 768 valeurs."""
    arr = np.array(img)
    hist = []
    for ch in range(3):
        h, _ = np.histogram(arr[:, :, ch], bins=bins, range=(0, 255))
        hist.extend(h.tolist())
    return hist


def _rms_contrast(img: Image.Image) -> float:
    """Contraste RMS : racine de la variance des intensités globales."""
    arr = np.array(img.convert("L"), dtype=np.float32)
    mean = arr.mean()
    return float(math.sqrt(np.mean((arr - mean) ** 2)))


def _contour_count(img: Image.Image) -> int:
    """Nombre de contours détectés via Canny + findContours."""
    arr = np.array(img.convert("L"))
    edges = cv2.Canny(arr, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return len(contours)


# ────────────────────────────────────────────────────────────────────────────────
# Fonction publique
# ────────────────────────────────────────────────────────────────────────────────
def extract_features(
    path: str,
    resize: bool = True,
    size: Tuple[int, int] = (400, 400),
    quality: int = 75,
) -> Optional[Dict]:
    """
    Pipeline complet d’extraction.

    1. (Optionnel) resize + compress via image_tools.process_image.
    2. Extraction de :
        - file_size            (int, octets)
        - width, height        (int, pixels)
        - mean_r/g/b           (float, 0-255)
        - rms_contrast         (float)
        - contour_count        (int)
        - histogram            (liste[int] longueur 768)

    Args:
        path: Chemin vers l’image source.
        resize: Si True, passe d’abord par process_image().
        size: Paramètre de redimensionnement.
        quality: Paramètre de compression JPEG.

    Returns:
        dict ou None si erreur.
    """
    try:
        processed_path = (
            process_image(path, size=size, quality=quality) if resize else path
        )
        if processed_path is None:
            return None

        with Image.open(processed_path) as img:
            w, h = _dimensions(img)
            mean_r, mean_g, mean_b = _mean_color(img)
            features = {
                "file_size": _file_size(processed_path),
                "width": w,
                "height": h,
                "mean_r": round(mean_r, 2),
                "mean_g": round(mean_g, 2),
                "mean_b": round(mean_b, 2),
                "rms_contrast": round(_rms_contrast(img), 2),
                "contour_count": _contour_count(img),
                "histogram": _histogram(img),
            }
            return features

    except FileNotFoundError:
        print(f"[extract_features] Fichier introuvable : {path}")
    except UnidentifiedImageError:
        print(f"[extract_features] Format non reconnu : {path}")
    except Exception as ex:
        print(f"[extract_features] Erreur inattendue : {ex}")

    return None


# ────────────────────────────────────────────────────────────────────────────────
# Utilisation rapide (debug)
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    import pprint

    parser = argparse.ArgumentParser(description="Extract features from an image.")
    parser.add_argument("image_path", help="Chemin vers l’image à analyser")
    args = parser.parse_args()

    feats = extract_features(args.image_path, resize=False)
    if feats:
        pprint.pprint(feats)
        # Exemple de sérialisation JSON
        print("\nJSON compact :")
        print(json.dumps(feats, separators=(",", ":")))
