from thefuzz import fuzz
import dtb
from google_images_search import GoogleImagesSearch
from io import BytesIO
from PIL import Image
import requests
import string


gis = GoogleImagesSearch("AIzaSyAjWZxqnIHmZ5iBngkqOZeKBvtV2uiMWlE",
                         "77f8f97ec10f04714")

def search(name):
    names = []
    for i in dtb.get_names():
        score = 0
        mutual_words = []
        for word1 in name.split():
            word1 = word1.translate(str.maketrans(dict.fromkeys(string.punctuation)))
            repeating_word = False
            for word2 in i.split():
                word2 = word2.translate(str.maketrans(dict.fromkeys(string.punctuation)))
                ratio = fuzz.ratio(word1.lower(), word2.lower())
                if ratio > 80:
                    for w in mutual_words:
                        if fuzz.ratio(word1.lower(), w.lower()) > 80:
                            repeating_word = True
                            break
                    if not repeating_word:
                        score += ratio
                        mutual_words.append(word2)
        names.append((i, score))
    names.sort(key=lambda x: x[1], reverse=True)
    return names[:10]


def google_search(name):
    search_params = {
        "q": name.lower(),
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
        int(num)
        images = []
        try:
            images = []
            r = requests.get(f"https://reshak.ru/reshebniki/geometriya/10/atanasyan10-11/{num}.png")
            if r.content == b'Access Denied':
                return []
            else:
                image_bytes = BytesIO(r.content)
                img = Image.open(image_bytes)
                images.append(img)
            r = requests.get(f"https://reshak.ru/reshebniki/geometriya/10/atanasyan10-11/{num}-.png")
            if r.content == b'Access Denied':
                return images
            else:
                image_bytes = BytesIO(r.content)
                img = Image.open(image_bytes)
                images.append(img)
            r = requests.get(f"https://reshak.ru/reshebniki/geometriya/10/atanasyan10-11/{num}--.png")
            if r.content == b'Access Denied':
                return images
            else:
                image_bytes = BytesIO(r.content)
                img = Image.open(image_bytes)
                images.append(img)
            return images
        except:
            return []

    except:
        try:
            images = []
            n = num.replace(".", " ").split()
            r = requests.get(f"https://reshak.ru/reshebniki/algebra/11/mordkovich2/images1/{n[0]}-{n[1]}.png")
            if r.content == b'Access Denied':
                return []
            else:
                image_bytes = BytesIO(r.content)
                img = Image.open(image_bytes)
                images.append(img)
            r = requests.get(f"https://reshak.ru/reshebniki/algebra/11/mordkovich2/images1/{n[0]}-{n[1]}-.png")
            if r.content == b'Access Denied':
                return images
            else:
                image_bytes = BytesIO(r.content)
                img = Image.open(image_bytes)
                images.append(img)
            r = requests.get(f"https://reshak.ru/reshebniki/algebra/11/mordkovich2/images1/{n[0]}-{n[1]}--.png")
            if r.content == b'Access Denied':
                return images
            else:
                image_bytes = BytesIO(r.content)
                img = Image.open(image_bytes)
                images.append(img)
            return images
        except:
            return []
