import connexion
import mariadb
import six
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import time

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
    for id_flower, common_name, scientific_name, label_name, description, image_url in cursor:
        flower = Flor(id_flower, common_name, scientific_name, label_name, description, image_url)
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
    for id_flower, common_name, scientific_name, label_name, description, image_url in cursor:
        flower = Flor(id_plant, common_name, scientific_name, label_name, description, image_url)
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
    classes = ["carvalho", "platano", "sobreiro"]

    am = np.argmax(result[0])
    print(result[0])
    print(result[0][am])
    flower_lbl = classes[am]

    connection = mariadb.connect(user="root", host="localhost", database="shizen", password="")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flowers WHERE label_name=%s", (flower_lbl,))

    flower = None
    for id_flower, common_name, scientific_name, label_name, description, image_url in cursor:
        flower = Flor(id_flower, common_name, scientific_name, label_name, description, image_url)
        break

    cursor.close()
    connection.close()

    return flower
