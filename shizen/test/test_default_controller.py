# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from shizen.models.flor import Flor  # noqa: E501
from shizen.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_all_flower(self):
        """Test case for get_all_flower

        
        """
        response = self.client.open(
            '/flowers',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_flower(self):
        """Test case for get_flower

        
        """
        response = self.client.open(
            '/flower/{idx}'.format(idx=2),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_recognize(self):
        """Test case for recognize

        
        """
        body = Object()
        response = self.client.open(
            '/recognize',
            method='POST',
            data=json.dumps(body),
            content_type='image/png')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
