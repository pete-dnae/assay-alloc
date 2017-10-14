import unittest

from model.setcomparisons import SetComparisons

class TestSetDifference(unittest.TestCase):

    def setUp(self):
        pass

    def test_how_similar(self):
        # No similarity
        a = {1}
        b = {2}
        similarity = SetComparisons.how_similar_are_ab(a, b)
        self.assertEqual(similarity, 0)

        # Identical with one member.
        a = {1}
        b = {1}
        similarity = SetComparisons.how_similar_are_ab(a, b)
        self.assertEqual(similarity, 1)

        # Foo
        a = {1}
        b = {1,2}
        similarity = SetComparisons.how_similar_are_ab(a, b)
        self.assertEqual(similarity, 1)

