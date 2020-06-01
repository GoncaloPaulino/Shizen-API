import connexion
import six

from shizen.models.flor import Flor  # noqa: E501
from shizen import util


def get_all_flower():  # noqa: E501
    """get_all_flower

    Returns every flower in the database. # noqa: E501


    :rtype: List[Flor]
    """
    return 'do some magic!'


def get_flower(idx):  # noqa: E501
    """get_flower

    Returns info about a specific flower. # noqa: E501

    :param idx: The flower ID
    :type idx: int

    :rtype: Flor
    """
    return 'do some magic!'


def recognize(body=None):  # noqa: E501
    """recognize

    Recognizes which flower is in a specific image. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Flor
    """
    if connexion.request.is_json:
        body = Object.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
