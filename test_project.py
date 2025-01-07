import pytest
from sandbox_rafa import read_data
from sandbox_rafa import validate_columns
from sandbox_rafa import create_tree_objects
from sandbox_rafa import Tree

def test_negative_dbh():
    file_path = r"more_tree_data\tree_data_negdap.csv"
    with pytest.raises(ValueError, match="There is a negative DBH value, please correct and restart."):
        read_data(file_path)


def main():
    test_negative_dbh()

main()