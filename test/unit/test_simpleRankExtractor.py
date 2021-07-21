import sys
import unittest
from unittest.mock import Mock, patch

sys.modules['db_low_level'] = Mock()

from models import SummonerDataModel

from RankExtractors.SimpleRankExtractor import SimpleRankExtractor


class MyTestCase(unittest.TestCase):
    @patch('dbutils.getSummonersSortedByStat')
    def test_exception_on_no_summoner_exist(self, dbutils_getSummonersSortedByStat):
        simpleRankExtractor = SimpleRankExtractor(None)
        session = Mock()
        dbutils_getSummonersSortedByStat.return_value = []
        self.assertRaises(LookupError, simpleRankExtractor.extract, 'hussein', session)

    def test_rank_detail(self):
        simpleRankExtractor = SimpleRankExtractor(None)
        summoner_data_array = [SummonerDataModel(name='Hussein'), SummonerDataModel(name='Omar'), SummonerDataModel(name='Saleh')]
        self.assertEqual(1, simpleRankExtractor.getSummonerRankDetails(summoner_data_array, "hussein")[0])
        self.assertEqual(2, simpleRankExtractor.getSummonerRankDetails(summoner_data_array, "omar")[0])
        self.assertEqual(3, simpleRankExtractor.getSummonerRankDetails(summoner_data_array, "saleh")[0])
        self.assertEqual(None, simpleRankExtractor.getSummonerRankDetails(summoner_data_array, "not_found")[0])


if __name__ == '__main__':
    unittest.main()
