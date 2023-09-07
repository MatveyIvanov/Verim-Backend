import random
import string


def get_random_string(length: int = 20):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
