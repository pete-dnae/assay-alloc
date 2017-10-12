import unittest

from .assay import Assay

class TestAssay(unittest.TestCase):

    def setUp(self):
        pass


    def test_construction_and_str_representation(self):
        assay = Assay('B', 3)
        self.assertEqual(str(assay), 'B3')
