import unittest

from .assay import Assay

class TestAssay(unittest.TestCase):

    def setUp(self):
        pass

    def test_override_methods(self):
        a1 = Assay('A', 1)
        a1_copy = Assay('A', 1)
        a2 = Assay('A', 2)

        self.assertEqual(str(a1), 'A1')
        self.assertEqual(a1, a1_copy)
        self.assertNotEqual(a1, a2)
        self.assertEqual(hash(a1), hash(a1_copy))
        self.assertNotEqual(hash(a1), hash(a2))
