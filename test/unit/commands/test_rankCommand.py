import sys
import unittest
from unittest.mock import Mock, patch

sys.modules['db_low_level'] = Mock()
patch('dbutils.SessionManager', lambda x: x).start()

from Commands.base_commands.RankCommand import RankCommand


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.session = Mock()

    @patch('dbutils.isSummonerNameExist')
    def test_exception_on_no_summoner_exist(self, dbutils_isSummonerEist):
        rankCommand = RankCommand()
        dbutils_isSummonerEist.return_value = False
        self.assertRaises(LookupError, rankCommand.execute, ['hussein'], self.session)

    def test_on_empty_args(self):
        rankCommand = RankCommand()
        self.assertRaises(ValueError, rankCommand.execute, [], self.session)


if __name__ == '__main__':
    unittest.main()
