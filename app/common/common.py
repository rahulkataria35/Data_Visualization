"""COMMON file"""
import random
import datetime
import base64


def get_random_dir_file_name(prefix, suffix):
    """
    generates random file/ directory name
    """
    time_stamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
    random_no = ''.join(random.sample('0123456789', 4))
    return prefix + time_stamp + random_no + suffix

def image_to_base64(f):
    with open(f, 'rb') as image:
        encoded_string = base64.b64encode(image.read())
    return encoded_string
