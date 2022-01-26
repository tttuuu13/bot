from thefuzz import fuzz
from thefuzz import process
import dtb

def search(name):
    names = []
    for i in dtb.get_names():
        ratio = fuzz.token_sort_ratio(name, i)
        if ratio != 0:
            names.append((i, ratio))
    names.sort(key=lambda x: x[1], reverse=True)
    return names[:5]