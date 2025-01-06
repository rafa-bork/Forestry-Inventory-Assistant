import pandas as pd

def read_my_data(filepath=None):
    """
    Reads a CSV file and outputs its contents as a table using pandas.
    
    Parameters:
        filepath (str): Path to the CSV file. If None, prompts the user for input.
        
    Returns:
        pandas.DataFrame: The DataFrame containing the CSV data.
    """
    if filepath is None:
        filepath = input("Enter the path to the CSV file: ")
    
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(filepath)
        print("\nHere is the table:\n")
        print(df.to_string(index=False))  # Display the DataFrame as a formatted table
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    df = read_my_data()  # Call the function to display the table and return the DataFrame





import pytest
from project.pye import import_trees_from_csv

def test_import_trees_from_csv(tmp_path):
    # 1. Create a temporary CSV file
    test_csv = tmp_path / "test_data.csv"
    test_csv.write_text(
        "species,dbh_cm,height_m,bark_width,COD_Status\n"
        "Pinus pinaster,30,15,2,ALIVE\n"
        "Pinus pinaster,25,12,2,DEAD\n"
    )
    
    # 2. Call the function
    trees = import_trees_from_csv(str(test_csv))
    
    # 3. Check the results
    assert len(trees) == 2
    assert trees[0].species == "Pinus pinaster"
    assert trees[0].dbh == 30.0
    assert trees[1].cod_status == "DEAD"
