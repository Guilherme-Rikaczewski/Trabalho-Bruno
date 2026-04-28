import string
import random


def generate_code(lenght=6):
    code_str = string.ascii_letters + string.digits
    code = ''.join(random.choices(code_str, k=lenght)).upper()
    return code
