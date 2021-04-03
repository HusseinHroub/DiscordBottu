import sys
import unittest
from unittest.mock import Mock

sys.modules['db_low_level'] = Mock()
from SortedListExtractors.SimpleSortedListExtractor import SimpleSortedListExtractor, ModeTypes


class MyTestCase(unittest.TestCase):
    def test_kills_rank_data_top_mode(self):
        simple_sorted_list = SimpleSortedListExtractor(ModeTypes.top, 'kills')
        ranks_data = simple_sorted_list.get_ranks_data([['Hussein', 29], ['Omar', 13], ['Ahmad', 10]])
        self.assertEqual(ranks_data[1], [1, 'Hussein', 29])
        self.assertEqual(ranks_data[2], [2, 'Omar', 13])
        self.assertEqual(ranks_data[3], [3, 'Ahmad', 10])

    def test_deaths_rank_data_top_mode(self):
        simple_sorted_list = SimpleSortedListExtractor(ModeTypes.top, 'deaths')
        ranks_data = simple_sorted_list.get_ranks_data([['Hussein', 29], ['Omar', 13], ['Ahmad', 10]])
        self.assertEqual(ranks_data[1], [1, 'Ahmad', 10])
        self.assertEqual(ranks_data[2], [2, 'Omar', 13])
        self.assertEqual(ranks_data[3], [3, 'Hussein', 29])

    def test_kills_rank_data_worst_mode(self):
        simple_sorted_list = SimpleSortedListExtractor(ModeTypes.worst, 'kills')
        ranks_data = simple_sorted_list.get_ranks_data([['Hussein', 29], ['Omar', 13], ['Ahmad', 10]])
        self.assertEqual(ranks_data[1], [1, 'Ahmad', 10])
        self.assertEqual(ranks_data[2], [2, 'Omar', 13])
        self.assertEqual(ranks_data[3], [3, 'Hussein', 29])

    def test_deaths_rank_data_worst_mode(self):
        simple_sorted_list = SimpleSortedListExtractor(ModeTypes.worst, 'deaths')
        ranks_data = simple_sorted_list.get_ranks_data([['Hussein', 29], ['Omar', 13], ['Ahmad', 10]])
        self.assertEqual(ranks_data[1], [1, 'Hussein', 29])
        self.assertEqual(ranks_data[2], [2, 'Omar', 13])
        self.assertEqual(ranks_data[3], [3, 'Ahmad', 10])


if __name__ == '__main__':
    unittest.main()
