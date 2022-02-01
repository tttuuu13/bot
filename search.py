from thefuzz import fuzz
import dtb
from google_images_search import GoogleImagesSearch
from io import BytesIO
from PIL import Image
import requests


gis = GoogleImagesSearch("AIzaSyAjWZxqnIHmZ5iBngkqOZeKBvtV2uiMWlE",
                         "77f8f97ec10f04714")

def search(name):
    names = []
    for i in dtb.get_names():
        ratio = fuzz.token_sort_ratio(name, i)
        if ratio != 0:
            names.append((i, ratio))
    names.sort(key=lambda x: x[1], reverse=True)
    return names[:5]

def google_search(name):
    search_params = {
        "q": name.lower() + " формула",
        "safe": "high",
        "num": 1,
        "fileType": "png|jpg"
    }
    gis.search(search_params)
    my_bytes_io = BytesIO()
    my_bytes_io.seek(0)
    image = gis.results()[0]
    image.copy_to(my_bytes_io)
    my_bytes_io.seek(0)
    img = Image.open(my_bytes_io)
    return img

def gdz_search(num):
    try:
        images = []
        n = num.replace(".", " ").split()
        for i in range(1, 2):
            r = requests.get(f"https://reshak.ru/reshebniki/algebra/10/mordkovich2/images{i}/{n[0]}-{n[1]}.png")
            if r.content == b'Access Denied':
                break
            else:
                image_bytes = BytesIO(r.content)
                img = Image.open(image_bytes)
                images.append(img)
            r = requests.get(f"https://reshak.ru/reshebniki/algebra/10/mordkovich2/images{i}/{n[0]}-{n[1]}-.png")
            if r.content == b'Access Denied':
                continue
            else:
                image_bytes = BytesIO(r.content)
                img = Image.open(image_bytes)
                images.append(img)
        """
        r = requests.get(f"https://reshak.ru/reshebniki/algebra/10/mordkovich2/images/{n[0]}-{n[1]}.png")
        if r.content == b'Access Denied':
            pass
        else:
            image_bytes = BytesIO(r.content)
            img = Image.open(image_bytes)
            images.append(img)"""
        return images
    except:
        return []
