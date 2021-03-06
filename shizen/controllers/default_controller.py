import connexion
import mariadb
import six
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import time

import os

from shizen.models.flor import Flor  # noqa: E501
from shizen import util


def get_all_flower():  # noqa: E501
    """get_all_flower

    Returns every flower in the database. # noqa: E501


    :rtype: List[Flor]
    """
    connection = mariadb.connect(user="root", host="localhost", database="shizen", password="")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flowers")

    flower_list = []
    for id_flower, common_name, scientific_name, label_name, description, min_height, max_height, native, classifiable, \
        more_info in cursor:
        flower = Flor(id_flower, common_name, scientific_name, label_name, description, min_height, max_height, native,
                      classifiable, more_info)
        flower_list.append(flower)

    cursor.close()
    connection.close()

    return flower_list


def get_flower(idx):  # noqa: E501
    """get_flower

    Returns info about a specific flower. # noqa: E501

    :param idx: The flower ID
    :type idx: int

    :rtype: Flor
    """
    connection = mariadb.connect(user="root", host="localhost", database="shizen", password="")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flowers WHERE id=%s", (idx,))

    flower = None
    for id_flower, common_name, scientific_name, label_name, description, min_height, max_height, native, classifiable, more_info in cursor:
        flower = Flor(id_flower, common_name, scientific_name, label_name, description, min_height, max_height, native,
                      classifiable, more_info)
        break

    cursor.close()
    connection.close()

    return flower


def recognize(body=None):  # noqa: E501
    """recognize

    Recognizes which flower is in a specific image. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Flor
    """
    flower_path = "imgs/" + str(int(round(time.time() * 1000))) + ".png"

    with open(flower_path, 'wb') as file:
        file.write(body)

    IMG_SIZE = 224
    loaded_model = load_model('tf_model/model.h5')
    img_holder = np.zeros((1, IMG_SIZE, IMG_SIZE, 3))

    img = image.load_img(flower_path, target_size=(IMG_SIZE, IMG_SIZE))
    img = np.array(img) / 255.0
    img_holder[0, :] = img

    result = loaded_model.predict(img_holder)
    os.remove(flower_path)
    classes = ["daisy", "dandelion", "roses", "sunflowers", "tulips"]

    am = np.argmax(result[0])
    print(result[0])
    print(result[0][am])
    flower_lbl = classes[am]

    connection = mariadb.connect(user="root", host="localhost", database="shizen", password="")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flowers WHERE label_name=%s", (flower_lbl,))

    flower = None
    for id_flower, common_name, scientific_name, label_name, description, min_height, max_height, native, classifiable, more_info in cursor:
        flower = Flor(id_flower, common_name, scientific_name, label_name, description, min_height, max_height, native,
                      classifiable, more_info)
        break

    cursor.close()
    connection.close()

    return flower


def get_fav_usr(idu):
    """get_fav_usr

    Returns a user favourites list. # noqa: E501

    :param idu: The user ID
    :type idu: int

    :rtype: Array of Int
    """
    connection = mariadb.connect(user="root", host="localhost", database="shizen", password="")
    cursor = connection.cursor()
    cursor.execute("SELECT id_flower FROM favourites WHERE id_user=%s", (idu,))

    favs = []
    for id_flower in cursor:
        favs.append(int(id_flower[0]))
        continue

    cursor.close()
    connection.close()

    return favs


def toggle_fav_usr(idu, idf):
    """get_fav_usr

    Toggle the favourite status of a plant as a user. # noqa: E501

    :param idu: The user ID
    :type idu: int

    :param idf: The flower ID
    :type idf: int

    :rtype: New toggle status
    """
    connection = mariadb.connect(user="root", host="localhost", database="shizen", password="")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM favourites WHERE id_user=%s AND id_flower=%s", (idu,idf,))
    cursor.fetchone()

    res = 2

    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO favourites VALUES (%s, %s)", (idu, idf,))
        res = 1
    else:
        cursor.execute("DELETE FROM favourites WHERE id_user=%s AND id_flower=%s", (idu,idf,))
        res = 0

    cursor.close()
    connection.close()

    return res
