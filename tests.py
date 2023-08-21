'''unittests to ensure my code works as intended'''

import unittest
from unittest.mock import MagicMock, patch
from LoginCheck.RapidApiSport import * 


class TestSportsOdds(unittest.TestCase): # for testing the 'sports_odds' function

    # 'patch' decorator to mock the 'requests.get' function
    @patch('LoginCheck.RapidApiSport.requests.get')
    def test_sports_odds(self, mock_get):
        # a mock response object and configure its behaviour 
        mock_response = MagicMock()
        mock_response.json.return_value = {"mocked_data": "here"}
        mock_get.return_value = mock_response

        # call the function being tested
        result = sports_odds()

        # assert that the result matches the expected mocked response
        self.assertEqual(result, {"mocked_data": "here"})
        
        # assert that the 'requests.get' function was called exactly once
        mock_get.assert_called_once()


class TestSaveSports(unittest.TestCase): # for testing the 'save_sports' function

    @patch('LoginCheck.RapidApiSport.sqlite3.connect')
    def test_save_sports(self, mock_connect):
        # mock objects for database connection and cursor
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # test input data, for now just place holder
        key = { ... }  

        # call the function being tested
        save_sports(key, "test.db")

        # assert that the cursor's 'execute' method was called
        mock_cursor.execute.assert_called()

        # assert that the connection's 'commit' and 'close' methods were called
        mock_conn.commit.assert_called()
        mock_conn.close.assert_called()


class TestBookmakersTable(unittest.TestCase): # for testing the 'bookmakers_table' function

    @patch('LoginCheck.RapidApiSport.sqlite3.connect')
    def test_bookmakers_table(self, mock_connect):
        # create mock objects for database connection and cursor
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # test input data, for now just place holder
        response_data = [ ... ]  

        # call the function being tested
        bookmakers_table("test.db", response_data)

        # assert that the cursor's 'execute' method was called
        mock_cursor.execute.assert_called()

        # assert that the connection's 'commit' and 'close' methods were called exactly once each
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

# Main execution to run the tests
if __name__ == '__main__':
    unittest.main()
