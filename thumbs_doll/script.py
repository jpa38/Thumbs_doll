import random
import urllib.request
from urllib.parse import urlparse
from PIL import Image
import glob, os
from pathlib import Path
import shutil


global img_travail
img_travail = 'image_doll_working_img'
global img_name
img_name = ''

def set_image_name(url):
    # TODO veriier utilité
    global img_name
    img_name = get_img_name(url)+get_url_extension(url)

def get_full_image_name(url):
    """Get the name + extension

    Args:
        url (str): the entry

    Returns:
        str : The name and extension about an URL / Path
    """
    return str(get_img_name(url) + get_url_extension(url))

def set_path_destination(path):
    # TODO veriier utilité

    global path_destination
    # path_destination = Path(path)
    # path = "'''r" + path + "'''"
    path_destination = path
    print(path_destination)

def get_path_destination():
    #  TODO veriier utilité
    return path_output

def get_path_input():
    return path_input

def download_image(url,name):

    # fullname = get_img_name(url)+get_url_extension(url)
    try:
        urllib.request.urlretrieve(url,name)
    except:
        reset_preview()
        print("Probleme URL")
    # global img_name
    #     # img_name = fullname

def get_url_extension(url):
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    return str(ext)

def get_img_name(url):
    path = urlparse(url).path
    filename_w_ext = os.path.basename(path)
    filename, file_extension = os.path.splitext(filename_w_ext)

    return str(filename)

def get_full_destination():
    pass

def is_url(input):

    if "http" in input :
        return True
    else :
        return False

def is_file(input):

    if os.path.isfile(input) and os.access(input, os.R_OK):
        return True
    else:
        return False

def get_image_size(img):
    im = Image.open(img)
    # width, height = im.size
    return max(im.size)

def resize(img,size,destination, name):
    thumb_size = size, size

    file, ext = os.path.splitext(img)
    im = Image.open(img)

    im.thumbnail(thumb_size)

    new_destination = os.path.join(destination, (str(name) + "_"+ str(size)+"px"+ext))

    print(new_destination)

    im.save(new_destination, format=None)


def conditions_initiales():
    # set_path_destination(r'''.\output''')

    global path_initial
    path_initial = os.getcwd()

    global path_input
    path_input = os.path.join(path_initial,"input\\")
    global path_output
    path_output = os.path.join(path_initial,"output\\")
    # shutil.rmtree(path_input)

    reset_folder(path_input)

    reset_preview()


    # todo verifier les dossiers existes
    print("conditions initiales Done")


def reset_preview():

    source = os.path.join(path_initial,'img','icon.png')
    destination = os.path.join(path_initial,'preview.jpg')

    shutil.copyfile(source, destination)


def reset_folder(folder):

    try :
        shutil.rmtree(folder)
    except:
        pass

    if not os.path.exists(folder):
        os.makedirs(folder)


# Keep presets


# set_path_destination(r'''C:\Users\J.PALANCA\Desktop''')

conditions_initiales()

# TODO gerer les paths pour l'execution via commande line

if __name__ == '__main__':

    if True:

        pass

    else:
        url = "http://www.planetrock.fr/wp-content/uploads/2019/01/chaton.png"

        rename = "test_img"

        download_image(url, str(rename))

        for px in [512, 256, 128, 64, 32, 24, 16]:
            manip(rename + get_url_extension(url), px, url)