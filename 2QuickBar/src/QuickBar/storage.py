# ok well this file should be self explanatory
# JSOn list of images (JSON is good for transporting info or something)
import json
import shutil   #for moving files fast
from pathlib import Path

from .config import IMAGES_DIR, LIBRARY_JSON #path to get images


def ensure_dirs(): #making sure it exist (?)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def load_library():
    #return ordered list of paths, skipping removed ones
    if not LIBRARY_JSON.exists(): #I hate this syntax
        return []
    try:
        paths = json.loads(LIBRARY_JSON.read_text(encoding="utf-8")) #translates text to machine code
    except json.JSONDecodeError: #if error, skip
        return []
    return [p for p in paths if Path(p).exists()] #return path if exists


def save_library(paths):
    LIBRARY_JSON.write_text(json.dumps(paths, indent=2), encoding="utf-8")


def import_image(src):
    #copy image to folder
    src = Path(src) #source
    dest = IMAGES_DIR / src.name #destination sub name
    i = 1
    while dest.exists():
        dest = IMAGES_DIR / f"{src.stem}_{i}{src.suffix}" #WHAT THE HECK (changed for age appropriateness)
        i += 1
    shutil.copy2(src, dest)
    return str(dest) 
