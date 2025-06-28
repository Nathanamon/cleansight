import os

def explore_dir(base_dir):
    summary = {}
    for root, dirs, files in os.walk(base_dir):
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff'))]
        if image_files:
            summary[root] = len(image_files)
    return summary

if __name__ == "__main__":
    base_dir = "Data/train"  # <- adapte ici !
    result = explore_dir(base_dir)
    for folder, count in result.items():
        print(f"{folder} : {count} images")
