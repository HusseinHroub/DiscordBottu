import unittest
from unittest.mock import patch, PropertyMock, MagicMock

from requestUtls import utils


class MyTestCase(unittest.TestCase):
    @patch('requests.get')
    def test_status_200(self, requests_get):
        type(requests_get.return_value).status_code = PropertyMock(return_value=200)
        type(requests_get.return_value).json = MagicMock(return_value='jsonString')
        self.assertEqual('jsonString', utils.getHTTPJsonResponse('dummyUrl'))

    @patch('requests.get')
    def test_status_404(self, requests_get):
        type(requests_get.return_value).status_code = PropertyMock(return_value=404)
        type(requests_get.return_value).json = MagicMock(return_value='jsonString')
        self.assertEqual(None, utils.getHTTPJsonResponse('dummyUrl'))

    @patch('requests.get')
    def test_exception_thrown_on_no_retry(self, requests_get):
        type(requests_get.return_value).status_code = PropertyMock(return_value=321)
        type(requests_get.return_value).json = MagicMock(return_value='jsonString')
        self.assertRaises(TimeoutError, utils.getHTTPJsonResponse, 'dummyUrl', 0)
        self.assertRaises(TimeoutError, utils.getHTTPJsonResponse, 'dummyUrl', 2)

    # TODO there has to be a way to find number of called functions, but mocking them won't do anything.



if __name__ == '__main__':
    unittest.main()
