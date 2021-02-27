import random


def get_random_photo(seed=None):
    url = "https://picsum.photos/400/400?random="
    if seed == None or type(seed) is not int:
        url = url + random.randint(0, 31337)
    else:
        url = url + str(seed)
    return url