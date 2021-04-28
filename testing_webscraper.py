import unittest
from webscraper import *


class TestExceptions(unittest.TestCase):
    def test_Exception1(self):
        with self.assertRaises(AttributeError):
            r = Retriever()
            search_ab = r.get_result_obj("Clairvoyance")
            p = Parser(search_ab)
            p.gather_attributes()

    def test_Exception2(self):
        with self.assertRaises(AttributeError):
            r = Retriever()
            search_ab = r.get_result_obj("xDxDXXD")
            p = Parser(search_ab)
            p.gather_attributes()


if __name__ == '__main__':
    unittest.main()
