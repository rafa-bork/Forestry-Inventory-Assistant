import pytest
from project import read_data
from project import validate_columns
from project import create_tree_objects
from project import Tree

def test_negative_dbh():
    file_path = r"more_tree_data\tree_data_negdap.csv"
    with pytest.raises(ValueError, match="There is a negative DBH value, please correct and restart."):
        read_data(file_path)

def main():
    test_negative_dbh()

if __name__ == "__main__":
    main()