from thefuzz import fuzz
import dtb
from google_images_search import GoogleImagesSearch
from io import BytesIO
from PIL import Image


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
