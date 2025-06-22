from PIL import Image, UnidentifiedImageError
import os

def resize_image(path, size=(400, 400)):
    """
    Redimensionne une image à la taille spécifiée et enregistre le résultat au format JPEG.

    Args:
        path (str): Chemin du fichier image à redimensionner.
        size (tuple, optional): Dimensions cibles (largeur, hauteur) en pixels. Par défaut (400, 400).

    Returns:
        str or None: Chemin du nouveau fichier image redimensionné si réussi, sinon None.

    Exceptions gérées:
        FileNotFoundError: Si le fichier image n'est pas trouvé.
        UnidentifiedImageError: Si le format de l'image n'est pas reconnu.
        Exception: Pour toute autre erreur inattendue.
    """
    try:
        img = Image.open(path)
        resized = img.resize(size, Image.ANTIALIAS)
        new_path = os.path.splitext(path)[0] + "_resized.jpg"
        resized.save(new_path, format='JPEG')
        return new_path
    except FileNotFoundError:
        print(f"Fichier introuvable : {path}")
        return None
    except UnidentifiedImageError:
        print(f"Format d’image non reconnu pour : {path}")
        return None
    except Exception as e:
        print(f"Erreur inattendue dans resize_image : {e}")
        return None

def compress_image(path, quality=75):
    """
    Compresse une image JPEG à partir du chemin spécifié avec une qualité donnée.

    Ouvre l'image à l'emplacement `path`, la compresse au format JPEG avec le niveau de qualité spécifié,
    puis enregistre l'image compressée sous un nouveau nom (suffixé par "_compressed.jpg").
    Gère les erreurs courantes telles que le fichier introuvable ou un format d'image non reconnu.

    Args:
        path (str): Chemin du fichier image à compresser.
        quality (int, optional): Niveau de qualité de la compression JPEG (de 1 à 95). Par défaut à 75.

    Returns:
        str or None: Chemin du nouveau fichier image compressé si réussi, sinon None.
    """
    try:
        img = Image.open(path)
        new_path = os.path.splitext(path)[0] + "_compressed.jpg"
        img.save(new_path, format='JPEG', quality=quality)
        return new_path
    except FileNotFoundError:
        print(f"Fichier introuvable : {path}")
        return None
    except UnidentifiedImageError:
        print(f"Format d’image non reconnu pour : {path}")
        return None
    except Exception as e:
        print(f"Erreur inattendue dans compress_image : {e}")
        return None

def process_image(path, size=(400, 400), quality=75):
    """
    Processes an image by resizing and compressing it.

    Args:
        path (str): The file path to the image to be processed.
        size (tuple, optional): The target size for resizing the image as (width, height). Defaults to (400, 400).
        quality (int, optional): The quality level for image compression (typically 0-100). Defaults to 75.

    Returns:
        object or None: The processed (resized and compressed) image object, or None if resizing fails.
    """
    resized = resize_image(path, size)
    if resized is None:
        return None
    compressed = compress_image(resized, quality)
    return compressed