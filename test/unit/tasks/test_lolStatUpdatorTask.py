import sys
import unittest
from unittest.mock import Mock, patch

from freezegun import freeze_time

sys.modules['db_low_level'] = Mock()
from models import SummonerDataModel

from Jobs.Tasks.LolStatUpdatorTask import LolStatUpdatorTask
import dbutils


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.lolStatsUpdator = LolStatUpdatorTask(Mock(), Mock())

    @freeze_time("2012-01-01")
    @patch('sotrageutils.getMonthAnnouncedValue')
    def test_at_start_of_month_finalizeIsCalled(self, sotrageutils_getMonthAnnouncedValue):
        sotrageutils_getMonthAnnouncedValue.return_value = 'False'
        self.lolStatsUpdator.finalizeMonthStats = Mock()
        self.lolStatsUpdator.resetStatsIfStartOfMonth(Mock())
        self.lolStatsUpdator.finalizeMonthStats.assert_called_once()

    @freeze_time("2012-01-01")
    @patch('sotrageutils.getMonthAnnouncedValue')
    def test_at_start_of_month_finalizeIsNotCalled(self, sotrageutils_getMonthAnnouncedValue):
        sotrageutils_getMonthAnnouncedValue.return_value = 'True'
        self.lolStatsUpdator.finalizeMonthStats = Mock()
        self.lolStatsUpdator.resetStatsIfStartOfMonth(Mock())
        self.lolStatsUpdator.finalizeMonthStats.assert_not_called()

    @freeze_time("2012-01-02")
    @patch('sotrageutils.markMonthAnnouncedValue')
    @patch('sotrageutils.getMonthAnnouncedValue')
    def test_at_not_start_of_month_finalizeIsCalled(self, sotrageutils_getMonthAnnouncedValue,
                                                    sotrageutils_markMonthAnnouncedValue):
        sotrageutils_getMonthAnnouncedValue.return_value = 'True'
        self.lolStatsUpdator.finalizeMonthStats = Mock()
        self.lolStatsUpdator.resetStatsIfStartOfMonth(Mock())
        sotrageutils_markMonthAnnouncedValue.assert_called_once()
        self.lolStatsUpdator.finalizeMonthStats.assert_not_called()

    @freeze_time("2012-01-02")
    @patch('sotrageutils.markMonthAnnouncedValue')
    @patch('sotrageutils.getMonthAnnouncedValue')
    def test_at_not_start_of_month_finalizeIsNotCalled(self, sotrageutils_getMonthAnnouncedValue,
                                                       sotrageutils_markMonthAnnouncedValue):
        sotrageutils_getMonthAnnouncedValue.return_value = 'False'
        self.lolStatsUpdator.finalizeMonthStats = Mock()
        self.lolStatsUpdator.resetStatsIfStartOfMonth(Mock())
        sotrageutils_markMonthAnnouncedValue.assert_not_called()
        self.lolStatsUpdator.finalizeMonthStats.assert_not_called()

    @patch('statsUtils.lolStatsMerger.mergeGamesStats')
    @patch('lolutils.lolApiUtils.getMatchesStats')
    def test_get_summoner_matches_data_timestamp(self, lolApiUtils_getMatchesStats,
                                                 lolStatsMerger_mergeGamesStats):
        result = self.lolStatsUpdator.getSummonerMatchesData([{'timestamp': 1}], 'testaccountId')
        self.assertEqual(2, result['totalStatsResult']['lastGameTimeStamp'])

    @patch('sotrageutils.updateStatCache')
    @patch('lolutils.lolApiUtils.getStatsOfGameId')
    @patch('lolutils.lolApiUtils.getMatchesByAccountId')
    @patch('dbutils.getAllSummonerData')
    def test_start_update_process_success_one_record_updated(self, summoner_data_call_mock,
                                                             lol_get_matches_api_mock,
                                                             lol_get_match_by_id_mock,
                                                             update_cache_mock):
        summoner_data_call_mock.return_value = [SummonerDataModel(accountId='testAccount',
                                                                  name='hussein',
                                                                  kills=10,
                                                                  deaths=2,
                                                                  assists=1,
                                                                  lastGameTimeStamp=1616762540733,
                                                                  avg_kda=2.3,
                                                                  farms=30,
                                                                  total_games=15)]
        lol_get_matches_api_mock.side_effect = self.lol_get_matches
        lol_get_match_by_id_mock.side_effect = self.get_match_by_id_mock
        session = Mock()
        self.lolStatsUpdator.startUpdateProcess(session)
        output = [
            {
                'kills': 16,
                'deaths': 14,
                'assists': 23,
                'farms': 368,
                'accountId': 'testAccount',
                'lastGameTimeStamp': 1616765013666,
                'avg_kda': 2.3008403361344536,
                'total_games': 17
            }
        ]
        session.bulk_update_mappings.assert_called_once_with(dbutils.SummonerData, output)

    @patch('sotrageutils.updateStatCache')
    @patch('lolutils.lolApiUtils.getStatsOfGameId')
    @patch('lolutils.lolApiUtils.getMatchesByAccountId')
    @patch('dbutils.getAllSummonerData')
    def test_start_update_process_success_one_record_updated_from_two(self, summoner_data_call_mock,
                                                                      lol_get_matches_api_mock,
                                                                      lol_get_match_by_id_mock,
                                                                      update_cache_mock):
        summoner_data_call_mock.return_value = [SummonerDataModel(accountId='testAccount',
                                                                  name='hussein',
                                                                  kills=10,
                                                                  deaths=2,
                                                                  assists=1,
                                                                  lastGameTimeStamp=1616762540733,
                                                                  avg_kda=2.3,
                                                                  farms=30,
                                                                  total_games=15),
                                                SummonerDataModel(accountId='testAccount1',
                                                                  name='omar',
                                                                  kills=1,
                                                                  deaths=2,
                                                                  assists=1,
                                                                  lastGameTimeStamp=1616762540731,
                                                                  avg_kda=1.2,
                                                                  farms=12,
                                                                  total_games=14)]
        lol_get_matches_api_mock.side_effect = self.lol_get_matches
        lol_get_match_by_id_mock.side_effect = self.get_match_by_id_mock
        session = Mock()
        self.lolStatsUpdator.startUpdateProcess(session)
        output = [
            {
                'kills': 16,
                'deaths': 14,
                'assists': 23,
                'farms': 368,
                'accountId': 'testAccount',
                'lastGameTimeStamp': 1616765013666,
                'avg_kda': 2.3008403361344536,
                'total_games': 17
            }
        ]
        session.bulk_update_mappings.assert_called_once_with(dbutils.SummonerData, output)

    @patch('sotrageutils.updateStatCache')
    @patch('lolutils.lolApiUtils.getStatsOfGameId')
    @patch('lolutils.lolApiUtils.getMatchesByAccountId')
    @patch('dbutils.getAllSummonerData')
    def test_start_update_process_success_zero_record_updated_from_two(self, summoner_data_call_mock,
                                                                       lol_get_matches_api_mock,
                                                                       lol_get_match_by_id_mock,
                                                                       update_cache_mock):
        summoner_data_call_mock.return_value = [SummonerDataModel(accountId='testAccount',
                                                                  name='hussein',
                                                                  kills=10,
                                                                  deaths=2,
                                                                  assists=1,
                                                                  lastGameTimeStamp=1616762540731,
                                                                  avg_kda=2.3,
                                                                  farms=30,
                                                                  total_games=15),
                                                SummonerDataModel(accountId='testAccount1',
                                                                  name='omar',
                                                                  kills=1,
                                                                  deaths=2,
                                                                  assists=1,
                                                                  lastGameTimeStamp=1616762540731,
                                                                  avg_kda=1.2,
                                                                  farms=12,
                                                                  total_games=14)]
        lol_get_matches_api_mock.side_effect = self.lol_get_matches
        lol_get_match_by_id_mock.side_effect = self.get_match_by_id_mock
        session = Mock()
        self.lolStatsUpdator.startUpdateProcess(session)
        session.bulk_update_mappings.assert_not_called()

    @patch('sotrageutils.updateStatCache')
    @patch('lolutils.lolApiUtils.getStatsOfGameId')
    @patch('lolutils.lolApiUtils.getMatchesByAccountId')
    @patch('dbutils.getAllSummonerData')
    def test_start_update_process_success_zero_record_updated_from_zero(self, summoner_data_call_mock,
                                                                        lol_get_matches_api_mock,
                                                                        lol_get_match_by_id_mock,
                                                                        update_cache_mock):
        summoner_data_call_mock.return_value = []
        lol_get_matches_api_mock.side_effect = self.lol_get_matches
        lol_get_match_by_id_mock.side_effect = self.get_match_by_id_mock
        session = Mock()
        self.lolStatsUpdator.startUpdateProcess(session)
        session.bulk_update_mappings.assert_not_called()

    @patch('sotrageutils.updateStatCache')
    @patch('lolutils.lolApiUtils.getStatsOfGameId')
    @patch('lolutils.lolApiUtils.getMatchesByAccountId')
    @patch('dbutils.getAllSummonerData')
    def test_start_update_process_success_tw_record_updated_from_two_first_time(self, summoner_data_call_mock,
                                                                                lol_get_matches_api_mock,
                                                                                lol_get_match_by_id_mock,
                                                                                update_cache_mock):
        summoner_data_call_mock.return_value = [SummonerDataModel(accountId='testAccount',
                                                                  name='hussein',
                                                                  kills=0,
                                                                  deaths=0,
                                                                  assists=0,
                                                                  lastGameTimeStamp=1616762540733,
                                                                  avg_kda=0,
                                                                  farms=0,
                                                                  total_games=0),
                                                SummonerDataModel(accountId='testAccount1',
                                                                  name='omar',
                                                                  kills=0,
                                                                  deaths=0,
                                                                  assists=0,
                                                                  lastGameTimeStamp=1616762540733,
                                                                  avg_kda=0,
                                                                  farms=0,
                                                                  total_games=0)]
        lol_get_matches_api_mock.side_effect = self.lol_get_matches
        lol_get_match_by_id_mock.side_effect = self.get_match_by_id_mock
        session = Mock()
        self.lolStatsUpdator.startUpdateProcess(session)
        output = [
            {
                'kills': 6,
                'deaths': 12,
                'assists': 22,
                'farms': 338,
                'accountId': 'testAccount',
                'lastGameTimeStamp': 1616765013666,
                'avg_kda': 2.314285714285714,
                'total_games': 2
            },
            {
                'kills': 1,
                'deaths': 3,
                'assists': 4,
                'farms': 21,
                'accountId': 'testAccount1',
                'lastGameTimeStamp': 1616762540735,
                'avg_kda': 1.6666666666666667,
                'total_games': 1
            }
        ]
        session.bulk_update_mappings.assert_called_once_with(dbutils.SummonerData, output)

    def lol_get_matches(self, *args, **kwargs):
        accountId = args[0]
        lastGameTimeStamp = args[1]
        if accountId == 'testAccount' and lastGameTimeStamp == 1616762540733:
            return [
                {
                    "platformId": "EUW1",
                    "gameId": 5173208166,
                    "champion": 67,
                    "queue": 440,
                    "season": 13,
                    "timestamp": 1616765013665,
                    "role": "DUO_CARRY",
                    "lane": "BOTTOM"
                },
                {
                    "platformId": "EUW1",
                    "gameId": 5173242406,
                    "champion": 64,
                    "queue": 440,
                    "season": 13,
                    "timestamp": 1616762540734,
                    "role": "NONE",
                    "lane": "JUNGLE"
                },
            ]
        elif accountId == 'testAccount1' and lastGameTimeStamp == 1616762540731:
            return None
        elif accountId == 'testAccount1' and lastGameTimeStamp == 1616762540733:
            return [
                {
                    "platformId": "EUW1",
                    "gameId": 5173242401,
                    "champion": 64,
                    "queue": 440,
                    "season": 13,
                    "timestamp": 1616762540734,
                    "role": "NONE",
                    "lane": "JUNGLE"
                },
            ]

    def get_match_by_id_mock(self, *args, **kwargs):
        game_id = args[0]
        account_id = args[1]
        if game_id == 5173208166 and account_id == 'testAccount':
            return {
                "participantId": 7,
                "win": True,
                "item0": 1055,
                "item1": 6672,
                "item2": 3006,
                "item3": 3124,
                "item4": 0,
                "item5": 0,
                "item6": 3363,
                "kills": 4,
                "deaths": 5,
                "assists": 7,
                "largestKillingSpree": 3,
                "largestMultiKill": 2,
                "killingSprees": 1,
                "longestTimeSpentLiving": 679,
                "doubleKills": 1,
                "tripleKills": 0,
                "quadraKills": 0,
                "pentaKills": 0,
                "unrealKills": 0,
                "totalDamageDealt": 109805,
                "magicDamageDealt": 0,
                "physicalDamageDealt": 86810,
                "trueDamageDealt": 22994,
                "largestCriticalStrike": 274,
                "totalDamageDealtToChampions": 12363,
                "magicDamageDealtToChampions": 0,
                "physicalDamageDealtToChampions": 8662,
                "trueDamageDealtToChampions": 3700,
                "totalHeal": 6331,
                "totalUnitsHealed": 2,
                "damageSelfMitigated": 7126,
                "damageDealtToObjectives": 17800,
                "damageDealtToTurrets": 7782,
                "visionScore": 17,
                "timeCCingOthers": 4,
                "totalDamageTaken": 14649,
                "magicalDamageTaken": 4506,
                "physicalDamageTaken": 9584,
                "trueDamageTaken": 558,
                "goldEarned": 10051,
                "goldSpent": 7850,
                "turretKills": 1,
                "inhibitorKills": 1,
                "totalMinionsKilled": 153,
                "neutralMinionsKilled": 20,
                "neutralMinionsKilledTeamJungle": 20,
                "neutralMinionsKilledEnemyJungle": 0,
                "totalTimeCrowdControlDealt": 28,
                "champLevel": 14,
                "visionWardsBoughtInGame": 0,
                "sightWardsBoughtInGame": 0,
                "wardsPlaced": 8,
                "wardsKilled": 3,
                "firstBloodKill": False,
                "firstBloodAssist": False,
                "firstTowerKill": False,
                "firstTowerAssist": False,
                "firstInhibitorKill": True,
                "firstInhibitorAssist": False,
                "combatPlayerScore": 0,
                "objectivePlayerScore": 0,
                "totalPlayerScore": 0,
                "totalScoreRank": 0,
                "playerScore0": 0,
                "playerScore1": 0,
                "playerScore2": 0,
                "playerScore3": 0,
                "playerScore4": 0,
                "playerScore5": 0,
                "playerScore6": 0,
                "playerScore7": 0,
                "playerScore8": 0,
                "playerScore9": 0,
                "perk0": 8005,
                "perk0Var1": 1069,
                "perk0Var2": 625,
                "perk0Var3": 443,
                "perk1": 9101,
                "perk1Var1": 865,
                "perk1Var2": 1189,
                "perk1Var3": 0,
                "perk2": 9104,
                "perk2Var1": 18,
                "perk2Var2": 50,
                "perk2Var3": 0,
                "perk3": 8017,
                "perk3Var1": 249,
                "perk3Var2": 0,
                "perk3Var3": 0,
                "perk4": 8139,
                "perk4Var1": 658,
                "perk4Var2": 0,
                "perk4Var3": 0,
                "perk5": 8135,
                "perk5Var1": 2455,
                "perk5Var2": 5,
                "perk5Var3": 0,
                "perkPrimaryStyle": 8000,
                "perkSubStyle": 8100,
                "statPerk0": 5005,
                "statPerk1": 5008,
                "statPerk2": 5003
            }
        elif game_id == 5173242406 and account_id == 'testAccount':
            return {
                "participantId": 5,
                "win": False,
                "item0": 6692,
                "item1": 2031,
                "item2": 3158,
                "item3": 3814,
                "item4": 3053,
                "item5": 0,
                "item6": 3340,
                "kills": 2,
                "deaths": 7,
                "assists": 15,
                "largestKillingSpree": 0,
                "largestMultiKill": 1,
                "killingSprees": 0,
                "longestTimeSpentLiving": 575,
                "doubleKills": 0,
                "tripleKills": 0,
                "quadraKills": 0,
                "pentaKills": 0,
                "unrealKills": 0,
                "totalDamageDealt": 148506,
                "magicDamageDealt": 34916,
                "physicalDamageDealt": 104343,
                "trueDamageDealt": 9246,
                "largestCriticalStrike": 0,
                "totalDamageDealtToChampions": 10109,
                "magicDamageDealtToChampions": 1230,
                "physicalDamageDealtToChampions": 8770,
                "trueDamageDealtToChampions": 108,
                "totalHeal": 12812,
                "totalUnitsHealed": 1,
                "damageSelfMitigated": 29892,
                "damageDealtToObjectives": 13004,
                "damageDealtToTurrets": 1819,
                "visionScore": 16,
                "timeCCingOthers": 14,
                "totalDamageTaken": 36081,
                "magicalDamageTaken": 9858,
                "physicalDamageTaken": 25248,
                "trueDamageTaken": 973,
                "goldEarned": 11064,
                "goldSpent": 10660,
                "turretKills": 1,
                "inhibitorKills": 0,
                "totalMinionsKilled": 57,
                "neutralMinionsKilled": 108,
                "neutralMinionsKilledTeamJungle": 81,
                "neutralMinionsKilledEnemyJungle": 1,
                "totalTimeCrowdControlDealt": 454,
                "champLevel": 16,
                "visionWardsBoughtInGame": 0,
                "sightWardsBoughtInGame": 0,
                "wardsPlaced": 10,
                "wardsKilled": 2,
                "firstBloodKill": False,
                "firstBloodAssist": False,
                "firstTowerKill": False,
                "firstTowerAssist": False,
                "firstInhibitorKill": False,
                "firstInhibitorAssist": False,
                "combatPlayerScore": 0,
                "objectivePlayerScore": 0,
                "totalPlayerScore": 0,
                "totalScoreRank": 0,
                "playerScore0": 0,
                "playerScore1": 0,
                "playerScore2": 0,
                "playerScore3": 0,
                "playerScore4": 0,
                "playerScore5": 0,
                "playerScore6": 0,
                "playerScore7": 0,
                "playerScore8": 0,
                "playerScore9": 0,
                "perk0": 8010,
                "perk0Var1": 20,
                "perk0Var2": 0,
                "perk0Var3": 0,
                "perk1": 9111,
                "perk1Var1": 926,
                "perk1Var2": 340,
                "perk1Var3": 0,
                "perk2": 9105,
                "perk2Var1": 15,
                "perk2Var2": 30,
                "perk2Var3": 0,
                "perk3": 8014,
                "perk3Var1": 181,
                "perk3Var2": 0,
                "perk3Var3": 0,
                "perk4": 8143,
                "perk4Var1": 304,
                "perk4Var2": 0,
                "perk4Var3": 0,
                "perk5": 8135,
                "perk5Var1": 2339,
                "perk5Var2": 5,
                "perk5Var3": 0,
                "perkPrimaryStyle": 8000,
                "perkSubStyle": 8100,
                "statPerk0": 5005,
                "statPerk1": 5008,
                "statPerk2": 5003
            }
        elif game_id == 5173242401 and account_id == 'testAccount1':
            return {
                "participantId": 1,
                "win": False,
                "item0": 6692,
                "item1": 2031,
                "item2": 3158,
                "item3": 3814,
                "item4": 3053,
                "item5": 0,
                "item6": 3340,
                "kills": 1,
                "deaths": 3,
                "assists": 4,
                "largestKillingSpree": 0,
                "largestMultiKill": 1,
                "killingSprees": 0,
                "longestTimeSpentLiving": 575,
                "doubleKills": 0,
                "tripleKills": 0,
                "quadraKills": 0,
                "pentaKills": 0,
                "unrealKills": 0,
                "totalDamageDealt": 148506,
                "magicDamageDealt": 34916,
                "physicalDamageDealt": 104343,
                "trueDamageDealt": 9246,
                "largestCriticalStrike": 0,
                "totalDamageDealtToChampions": 10109,
                "magicDamageDealtToChampions": 1230,
                "physicalDamageDealtToChampions": 8770,
                "trueDamageDealtToChampions": 108,
                "totalHeal": 12812,
                "totalUnitsHealed": 1,
                "damageSelfMitigated": 29892,
                "damageDealtToObjectives": 13004,
                "damageDealtToTurrets": 1819,
                "visionScore": 16,
                "timeCCingOthers": 14,
                "totalDamageTaken": 36081,
                "magicalDamageTaken": 9858,
                "physicalDamageTaken": 25248,
                "trueDamageTaken": 973,
                "goldEarned": 11064,
                "goldSpent": 10660,
                "turretKills": 1,
                "inhibitorKills": 0,
                "totalMinionsKilled": 20,
                "neutralMinionsKilled": 1,
                "neutralMinionsKilledTeamJungle": 81,
                "neutralMinionsKilledEnemyJungle": 1,
                "totalTimeCrowdControlDealt": 454,
                "champLevel": 16,
                "visionWardsBoughtInGame": 0,
                "sightWardsBoughtInGame": 0,
                "wardsPlaced": 10,
                "wardsKilled": 2,
                "firstBloodKill": False,
                "firstBloodAssist": False,
                "firstTowerKill": False,
                "firstTowerAssist": False,
                "firstInhibitorKill": False,
                "firstInhibitorAssist": False,
                "combatPlayerScore": 0,
                "objectivePlayerScore": 0,
                "totalPlayerScore": 0,
                "totalScoreRank": 0,
                "playerScore0": 0,
                "playerScore1": 0,
                "playerScore2": 0,
                "playerScore3": 0,
                "playerScore4": 0,
                "playerScore5": 0,
                "playerScore6": 0,
                "playerScore7": 0,
                "playerScore8": 0,
                "playerScore9": 0,
                "perk0": 8010,
                "perk0Var1": 20,
                "perk0Var2": 0,
                "perk0Var3": 0,
                "perk1": 9111,
                "perk1Var1": 926,
                "perk1Var2": 340,
                "perk1Var3": 0,
                "perk2": 9105,
                "perk2Var1": 15,
                "perk2Var2": 30,
                "perk2Var3": 0,
                "perk3": 8014,
                "perk3Var1": 181,
                "perk3Var2": 0,
                "perk3Var3": 0,
                "perk4": 8143,
                "perk4Var1": 304,
                "perk4Var2": 0,
                "perk4Var3": 0,
                "perk5": 8135,
                "perk5Var1": 2339,
                "perk5Var2": 5,
                "perk5Var3": 0,
                "perkPrimaryStyle": 8000,
                "perkSubStyle": 8100,
                "statPerk0": 5005,
                "statPerk1": 5008,
                "statPerk2": 5003
            }


if __name__ == '__main__':
    unittest.main()
