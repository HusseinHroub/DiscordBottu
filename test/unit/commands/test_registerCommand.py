import sys
import unittest
from unittest.mock import Mock, patch

sys.modules['db_low_level'] = Mock()
patch('dbutils.SessionManager', lambda x: x).start()

from Commands.base_commands.RegisterCommand import RegisterCommand


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.session = Mock()

    def test_args_empty(self):
        registerCommand = RegisterCommand()
        self.assertRaises(ValueError, registerCommand.execute, [], self.session)

    @patch('dbutils.isSummonerNameExist')
    def test_summoner_not_exist(self, dbutils_isSummonerNameExist):
        registerCommand = RegisterCommand()
        dbutils_isSummonerNameExist.return_value = True
        self.assertRaises(AttributeError, registerCommand.execute, ['hussein'], self.session)

    @patch('dbutils.isSummonerNameExist')
    @patch('dbutils.updateSummonerNameByAccountId')
    @patch('dbutils.isAccountIdExist')
    @patch('lolutils.lolApiUtils.getAccountIdByName')
    def test_summoner_already_exist_account(self, lolApiUtils_getAccountIdByName, dbutils_isAccountIdExist,
                                            dbutils_updateSummonerNameByAccountId,
                                            dbutils_isSummonerNameExist
                                            ):
        registerCommand = RegisterCommand()
        dbutils_isSummonerNameExist.return_value = True
        lolApiUtils_getAccountIdByName.return_value = 'testaccount'
        dbutils_isAccountIdExist.return_value = True
        self.assertRaises(AttributeError, registerCommand.execute, ['hussein'], self.session)


if __name__ == '__main__':
    unittest.main()
