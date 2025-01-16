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
    with patch('builtins.input', return_value=""):
        read_data(file_path)
    expected_attributes = {"tree_ID", "species", "est_dbh", "dbh", "height", "est_height", "cod_status", "basal_area", "tree_volume", "merc_volume", "trunk_biom", "bark_biom", "branch_biom", "leaves_biom", "aerial_biom", "roots_biom", "total_biom", "wood_value"}
    for tree in Tree.tree_list:
        tree_attributes = set(vars(tree).keys())  
        assert expected_attributes == tree_attributes

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

def test_missing_dbh():
    file_path = r"more_tree_data\tree_data_missingdbh.csv"
    read_data(file_path)
    calculate_missing_dbh_h()
    treefinder = any(tree.tree_ID == 4 and 
                         tree.species == "Pb" and 
                         tree.est_dbh == 36.6 and 
                         tree.height == 19.5 and 
                         tree.cod_status == 1 for tree in Tree.tree_list)
    assert treefinder

def test_missing_height():
    file_path = r"more_tree_data\tree_data_missingheight.csv"
    read_data(file_path)
    calculate_missing_dbh_h()
    treefinder = any(tree.tree_ID == 3 and 
                         tree.species == "Pb" and 
                         tree.dbh == 35.3 and 
                         tree.est_height == 19.10 and 
                         tree.cod_status == 1 for tree in Tree.tree_list)
    assert treefinder 

def test_missing_dbh_and_height():
    file_path = r"more_tree_data\tree_data_missingdbhheight.csv"
    with pytest.raises(ValueError, match="There are trees without DBH and height values, please correct and restart"):
        read_data(file_path)

def test_missing_species():
    file_path = r"more_tree_data\tree_data_missingspecies.csv"
    with pytest.raises(ValueError, match="There is a missing species value, please correct and restart"):
        read_data(file_path)

def test_missing_tree_id():
    file_path = r"more_tree_data\tree_data_missingtreeid.csv"
    with pytest.raises(ValueError, match="There is a missing tree_id value, please correct and restart"):
        read_data(file_path)

def test_mixed_attributes():
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
    with pytest.raises(ValueError, match="There is a non-integer tree_id value, please correct and restart"):
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

def test_short_dbh_Ec():
    file_path = r"more_tree_data\tree_data_shortdbhEc.csv"
    with pytest.raises(ValueError, match="There is a Eucalyptus' DBH value that's less than 5cm, this is not considered a tree, please correct and restart."):
        read_data(file_path)

def test_wrong_cod_status():
    file_path = r"more_tree_data\tree_data_wrongcodstatus.csv"
    with pytest.raises(ValueError, match="There is an invalid COD_status value, please correct and restart"):
        read_data(file_path)

def test_zero_tree_id():
    file_path = r"more_tree_data\tree_data_zerotreeid.csv"
    with pytest.raises(ValueError, match="There is a non-positive tree_id value, please correct and restart"):
        read_data(file_path)

def test_missing_csv():
    file_path = r"more_tree_data\this_file_does_not_exist.csv"
    with pytest.raises(FileNotFoundError, match="There was an error reading the file, please correct and restart."):
        read_data(file_path)

def test_values():
    file_path = r"more_tree_data/tree_data__perfect_short_Pb_Ec.csv"
    read_data(file_path)
    with patch('builtins.input', return_value=""):
        input_stand_area()
    calculate_missing_dbh_h()
    with patch('builtins.input', return_value=""):
        stand_metrics()
    
    treefinder_1 = any(
            tree.tree_ID == 1 and
            tree.species == "Pb" and
            tree.dbh == 12 and
            tree.est_dbh == 12 and
            tree.height == 14 and
            tree.est_height ==  14 and
            tree.cod_status == 1 and
            round(tree.basal_area, 4) == 0.0113 and
            round(tree.tree_volume, 4) == 0.0776 and
            round(tree.merc_volume, 4) == 0.0541 and
            round(tree.wood_value, 2) == 0.94 and
            round(tree.trunk_biom, 4) == 34.1710 and
            round(tree.bark_biom, 4) == 7.0019 and
            round(tree.branch_biom, 4) == 2.7425 and
            round(tree.leaves_biom, 4) == 2.8427 and
            round(tree.aerial_biom, 4) == 46.7581 and
            round(tree.roots_biom, 4) == 12.8865 and
            round(tree.total_biom, 4) == 59.6446
            for tree in Tree.tree_list
        )
    assert treefinder_1, "Tree with ID 1 does not have the expected values."

    treefinder_2 = any(
        tree.tree_ID == 4 and
        tree.species == "Ec" and
        tree.dbh == 12 and
        tree.est_dbh == 12 and
        tree.height == 90 and
        tree.est_height == 90 and
        tree.cod_status == 1 and
        round(tree.basal_area, 4) == 0.0113 and
        round(tree.tree_volume, 4) == 0.5493 and
        round(tree.merc_volume, 4) == 0.5151 and
        round(tree.wood_value, 2) == 14.34 and
        round(tree.trunk_biom, 4) == 394.8548 and
        round(tree.bark_biom, 4) == 34.3069 and
        round(tree.branch_biom, 4) == 1.1048 and
        round(tree.leaves_biom, 4) == 1.3712 and
        round(tree.aerial_biom, 4) == 431.6377 and
        round(tree.roots_biom, 4) == 107.3483 and
        round(tree.total_biom, 4) == 538.9860
        for tree in Tree.tree_list
        )
    assert treefinder_2, "Tree with ID 2 does not have the expected values."
    
    assert Stand.Main_species == "Pb"
    assert Stand.Area == 0.1*10000
    assert Stand.Age == 0
    assert Stand.Total == 6
    assert Stand.N == 60
    assert Stand.N_dead == 0
    assert Stand.n_dom_trees == 5
    assert Stand.hdom == 14
    assert Stand.ddom == 12
    assert round(Stand.G_pov, 4) == 0.6786
    assert round(Stand.V_pov, 4) == 9.3746
    assert round(Stand.Value_pov, 4) == 190.6585
    assert round(Stand.dg, 2) == 12
    assert round(Stand.Fw, 2) == 0.92
    assert Stand.Site_index == 0 
    assert round(Stand.SDI, 4) == 14.9096