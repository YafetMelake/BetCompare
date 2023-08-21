import unittest
from unittest.mock import MagicMock, patch
from LoginCheck.RapidApiSport import *

class TestSportsOdds(unittest.TestCase):

    @patch('LoginCheck.RapidApiSport.requests.get')
    def test_sports_odds(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"mocked_data": "here"}
        mock_get.return_value = mock_response

        result = sports_odds()

        self.assertEqual(result, {"mocked_data": "here"})
        mock_get.assert_called_once()

class TestSaveSports(unittest.TestCase):

    @patch('LoginCheck.RapidApiSport.sqlite3.connect')
    def test_save_sports(self, mock_connect):
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        key = {
            "bookmakers": [
                {
                    "markets": [
                        {
                            "key": "h2h",
                            "outcomes": [
                                {"name": "HomeTeam", "price": 1.5},
                                {"name": "AwayTeam", "price": 2.0}
                            ]
                        }
                    ],
                    "key": "bookie_key"
                }
            ],
            "sport_key": "soccer_key",
            "home_team": "HomeTeam",
            "away_team": "AwayTeam"
        }

        save_sports(key, "test.db")

        # Modify these assertions based on the actual behavior of the code
        # You may need to adjust the number of times execute is called and the order of calls
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
        mock_conn.close.assert_called()


class TestBookmakersTable(unittest.TestCase):

    @patch('LoginCheck.RapidApiSport.sqlite3.connect')
    def test_bookmakers_table(self, mock_connect):
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response_data = [{"bookmakers": [{"title": "Bookie 1"}]}]

        bookmakers_table("test.db", response_data)

        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

# Similar tests can be created for the other functions: matches_table, price_table, and sportssoddss.

if __name__ == '__main__':
    unittest.main()
