import pytest
from unittest.mock import patch
from project import *
import re

def test_empty_csv():
    file_path = r"more_tree_data\tree_data_empty.csv"
    with pytest.raises(ValueError, match="The given file is empty, please correct and restart."):
        read_data(file_path)

def test_extra_column_csv_stop():
    file_path = r"more_tree_data\tree_data_extracolumn.csv"
    with patch('builtins.input', return_value="X"), patch('sys.exit') as mock_exit:
        read_data(file_path)
        mock_exit.assert_called_once_with("Closing...\n")

def test_extra_column_csv_continue():
    file_path = r"more_tree_data\tree_data_extracolumn.csv"
    with patch('builtins.input', return_value=" "):
        read_data(file_path)
    expected_attributes = {"tree_ID", "species", "dbh", "height", "cod_status"}
    for tree in Tree.tree_list:
        tree_attributes = set(vars(tree).keys())  
        assert tree_attributes == expected_attributes

def test_duplicate_id():
    file_path = r"more_tree_data\tree_data_idduplicate.csv"
    with pytest.raises(ValueError, match="Tree ID 4 is duplicate in the table, please correct and restart."):
        read_data(file_path)

def test_missing_attributes():
    file_path = r"more_tree_data\tree_data_missingattributes.csv"
    with pytest.raises(ValueError, match="There are required columns missing in the file: DBH"):
        read_data(file_path)

def test_missing_cod_status():
    file_path = r"more_tree_data\tree_data_missingcodstatus.csv"
    read_data(file_path)
    treefinder = any(tree.tree_ID == 2 and 
                         tree.species == "Pb" and 
                         tree.dbh == 40.0 and 
                         tree.height == 21 and 
                         tree.cod_status == 1 for tree in Tree.tree_list)
    assert treefinder 

#def test_missing_dbh():
#    file_path = r"more_tree_data\tree_data_missingdbh.csv"
#    read_data(file_path)
#    treefinder = any(tree.tree_ID == 4 and 
#                         tree.species == "Pb" and 
#                         tree.dbh == ##### and 
#                         tree.height == 19.5 and 
#                         tree.cod_status == 1 for tree in Tree.tree_list)
#    assert treefinder 

#def test_missing_height():
#    file_path = r"more_tree_data\tree_data_missingheight.csv"
#    read_data(file_path)
#    treefinder = any(tree.tree_ID == 3 and 
#                         tree.species == "Pb" and 
#                         tree.dbh == 35.3 and 
#                         tree.height == ####.5 and 
#                         tree.cod_status == 1 for tree in Tree.tree_list)
#    assert treefinder 

def test_missing_species():
    file_path = r"more_tree_data\tree_data_missingspecies.csv"
    with pytest.raises(ValueError, match="There is a missing species value, please correct and restart"):
        read_data(file_path)

def test_missing_tree_id():
    file_path = r"more_tree_data\tree_data_missingtreeid.csv"
    with pytest.raises(ValueError, match="There is a missing tree_id value, please correct and restart"):
        read_data(file_path)

def test_mixed_atributes():
    file_path = r"more_tree_data\tree_data_mixedattributes.csv"
    read_data(file_path)
    treefinder = any(tree.tree_ID == 2 and 
                         tree.species == "Pb" and 
                         tree.dbh == 40.0 and 
                         tree.height == 21 and 
                         tree.cod_status == 1 for tree in Tree.tree_list)
    assert treefinder 

def test_negative_dbh():
    file_path = r"more_tree_data\tree_data_negdbh.csv"
    with pytest.raises(ValueError, match="There is a negative DBH value, please correct and restart."):
        read_data(file_path)

def test_negative_height():
    file_path = r"more_tree_data\tree_data_negheight.csv"
    with pytest.raises(ValueError, match="There is a negative height value, Please correct and restart."):
        read_data(file_path)

def test_new_species():
    file_path = r"more_tree_data\tree_data_newspecies.csv"
    with pytest.raises(ValueError, match=re.escape("There is a species value that is not acceptable (not 'Pb', 'Pm', 'Ec', or 'Sb'), please correct and restart")):
        read_data(file_path)

def test_float_tree_id():
    file_path = r"more_tree_data\tree_data_noninttreeid_.csv"
    with pytest.raises(ValueError, match="There is a decimal tree_id value, please correct and restart"):
        read_data(file_path)

def test_char_tree_id():
    file_path = r"more_tree_data\tree_data_noninttreeid.csv"
    with pytest.raises(ValueError, match="There is a non integer tree_id value, please correct and restart"):
        read_data(file_path)

def test_char_dbh():
    file_path = r"more_tree_data\tree_data_nonnumberdbh.csv"
    with pytest.raises(ValueError, match="There is a DBH value that cannot be converted to float, please correct and restart."):
        read_data(file_path)

def test_char_height():
    file_path = r"more_tree_data\tree_data_nonnumberheight.csv"
    with pytest.raises(ValueError, match="There is a height value that cannot be converted to float. Please correct and restart."):
        read_data(file_path)

def test_short_dbh():
    file_path = r"more_tree_data\tree_data_shortdbh.csv"
    with pytest.raises(ValueError, match="There is a DBH value that's less than 7.5cm, this is not considered a tree, please correct and restart."):
        read_data(file_path)

def test_wrong_cod_status():
    file_path = r"more_tree_data\tree_data_wrongcodstatus.csv"
    with pytest.raises(ValueError, match="There is an invalid COD_status value, please correct and restart"):
        read_data(file_path)

def test_zero_tree_id():
    file_path = r"more_tree_data\tree_data_zerotreeid.csv"
    with pytest.raises(ValueError, match="There is a non positive tree_id value, please correct and restart"):
        read_data(file_path)

def test_missing_csv():
    file_path = r"more_tree_data\this_file_does_not_exist.csv"
    with pytest.raises(FileNotFoundError, match="There was an error reading the file, please correct and restart."):
        read_data(file_path)

# The format of the file should be in CSV
def test_invalid_file_format():
    file_path = r"more_tree_data\invalid_file.txt"
    with pytest.raises(ValueError, match="The file is not a Comma Separated Values (.csv) file, please correct and try again."):
        read_data(file_path)


# Test if the calculated metrics are correct 

def test_calculate_metrics():
    # Path to the CSV file with test data
    file_path = r"more_tree_data\tree_data_test.csv"
    
    # Read the data from the file and create Tree objects
    read_data(file_path)
    
    # Expected data for metric calculations
    expected_metrics = [
        {
            "tree_ID": 1,
            "volume": 0.6521,  # Expected value for volume
            "basal_area": 0.0123,  # Expected value for basal area
            "total_biomass": 35.67  # Expected value for total biomass
        },
        {
            "tree_ID": 2,
            "volume": 1.2458,
            "basal_area": 0.0251,
            "total_biomass": 48.92
        }
    ]

    # Perform calculations for each tree and compare with expected results
    for tree, expected in zip(Tree.tree_list, expected_metrics):
        assert tree.tree_ID == expected["tree_ID"], \
            f"Tree ID mismatch: expected {expected['tree_ID']}, got {tree.tree_ID}"
        assert round(tree.calculate_volume(), 4) == expected["volume"], \
            f"Volume mismatch for Tree {tree.tree_ID}: expected {expected['volume']}, got {round(tree.calculate_volume(), 4)}"
        assert round(tree.calculate_basal_area(), 4) == expected["basal_area"], \
            f"Basal area mismatch for Tree {tree.tree_ID}: expected {expected['basal_area']}, got {round(tree.calculate_basal_area(), 4)}"
        assert round(tree.calculate_total_biomass(), 2) == expected["total_biomass"], \
            f"Total biomass mismatch for Tree {tree.tree_ID}: expected {expected['total_biomass']}, got {round(tree.calculate_total_biomass(), 2)}"
