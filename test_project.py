import pytest
from unittest import mock
from project import *

def test_empty_csv():
    file_path = r"more_tree_data\tree_data_empty.csv"
    with pytest.raises(ValueError, match="The given file is empty, please correct and restart."):
        read_data(file_path)

def test_extra_column_csv():
    file_path = r"more_tree_data\tree_data_extracolumn.csv"
    with mock.patch('builtins.input', return_value='x'), mock.patch('sys.exit') as mock_exit:
        with pytest.raises(SystemExit):  # Verifica se o código levanta a exceção de SystemExit
            read_data(file_path)
        mock_exit.assert_called_once()  # Verifica se sys.exit foi chamado


def test_negative_dbh():
    file_path = r"more_tree_data\tree_data_negdap.csv"
    with pytest.raises(ValueError, match="There is a negative DBH value, please correct and restart."):
        read_data(file_path)

def main():
    test_empty_csv()
    test_extra_column_csv()
    test_negative_dbh()
    
if __name__ == "__main__":
    main()