import unittest
from unittest.mock import patch
from src.storage_interface import load_files_dump_from_RSE
from src.log_config import logger

class TestStorageInterface(unittest.TestCase):
    @patch('src.storage_interface.os.path.exists')
    @patch('src.storage_interface.os.listdir')
    def negative_test_load_files_dump_from_RSE__empty_directory(self, mock_listdir, mock_exists):
        # Mock the necessary functions and variables
        mock_exists.return_value = False
        mock_listdir.return_value = 'empty_directory'
        mock_logger = unittest.mock.MagicMock()

        mock_open = unittest.mock.mock_open(read_data='file1\nfile2\nfile3')

        # Call the function under test
        with patch('src.storage_interface.open', mock_open):
            result = load_files_dump_from_RSE(mock_listdir, 'RSE', mock_logger)

        # Assert the expected result
        expected_result = False
        self.assertEqual(result, expected_result)

        # Assert the function calls
        mock_exists.assert_called_once_with('/path/to/directory')
        mock_listdir.assert_called_once_with('/path/to/directory')
        mock_open.assert_called_once_with('/path/to/directory/dump_file.txt', 'r')

if __name__ == '__main__':
    unittest.main()