import pandas as pd
import sys

def welcome_message():
    print("---")
    print("Welcome to the Forest Inventory Companion Program!")
    print("---")
    print("Please add your tree data to the tree_data.csv file in the correct format")
    while True:
        print("If help is needed type 'help'")
        print("If the information was correctly added press <Enter>")
        print('If you prefer, write the file\'s path in the following format: "C:\\Users\\rafael\\Downloads\\tree_data.csv"')
        print("If you want to close the program type 'exit'.")
        welcome = input("  ").strip()

        if welcome.startswith('"') and welcome.endswith('"'):
            welcome = welcome[1:-1]  # Remove the first and last characters (the quotes)
        
        if welcome.casefold() == "help":
            help()
        elif welcome.casefold() == "exit":
            print("Exiting program...")
            sys.exit("Closing...\n\n")
        elif welcome == "":
            return
        elif welcome.endswith('.csv') or welcome.endswith('.csv"'):
            return welcome
        else:
            print("The file is not a Comma Separated Values (.csv) file, please correct and try again.")
            print("---")
            

def help():
    print("---")
    print("This Program is a tool to help in the characterization and analysis of a tree stand")
    print("This tool uses mathematical and statistical tools to calculate and infer the features of the stand from a short grouping of the tree's accurate measurements")
    print("These measurements, the height and the diameter of each tree in the plot, need to be inserted into the tree_data.csv file in the correct order")
    print("This file is in the same folder as this python script")
    print("")
    print("This file has 5 columns: 'tree_ID', 'species', 'DBH', 'height' and 'COD_Status'")
    print("The 'tree_ID' column must have a sequential numerical order to uniquely identify each tree in the plot")
    print("The 'species' column must have a code that corresponds to the tree's species")
    print("         species Code             Common Name                Scientific Name")
    print("         Pb                       Maritime Pine              Pinus pinaster")
    print("         Pm                       Stone Pine                 Pinus pinea")
    print("         Ec                       Southern Blue Gum          Eucalyptus globulus")
    print("         Sb                       Cork Oak                   Quercus suber")
    print("The 'DBH' column must have the trunk's measured diameter at breast height (1.30m), in centimetres")
    print("The 'height' column must have the tree's measured total height, in meters")
    print("     You should at least provide one of these measurements")
    print("The 'COD_status' column must have a code that represents the tree's capacity. The correspondence is in the following table")
    print("         COD_status              Tree Status")
    print("         1                       Alive")
    print("         2                       Dead")
    print("         3                       Missing (relevant in stands planted with a regular step)")
    print("         4                       Stump")
    print("---")

def read_data(file_path):
    print("")
    print("Importing the Datatable...")
    if file_path is None:
        file_path = "tree_data.csv"
    try:
        df = pd.read_csv(file_path)
        validate_columns(df)
        tree_objects = create_tree_objects(df)
        print(f"\nHere is the table: {file_path}")
        print(df.to_string(index=False))
        print("")
        return tree_objects
    except Exception as e:
        print("")
        print(f"There was an error reading the file, {e}")
        sys.exit("Closing...\n")

# Control if all the fundamental columns are present
def validate_columns(dataframe):
    required_columns = {"tree_ID", "species", "DBH", "height", "COD_Status"}
    dataframe_columns = set(dataframe.columns)
    missing_columns = required_columns - dataframe_columns
    extra_columns = dataframe_columns - required_columns
    if missing_columns:
        print(f"There are required columns missing in the file: {missing_columns}")
        sys.exit("Closing...\n")
    if extra_columns:
        print(f"There are extra columns in the file: {extra_columns}")
        print("Are you sure? The extra columns will not be taen into account by the programme.")
        answer = input("Press <Enter> to continue, press any other butten to close")
        if answer != "":
            sys.exit("Closing...\n")
    return


class Tree:
    tree_list = []  # This is the class-level list where all trees will be stored

    def __init__(self, tree_ID, species, dbh, height, cod_status):
        self.tree_ID = tree_ID
        self.species = species
        self.dbh = dbh
        self.height = height
        self.cod_status = cod_status

        # Check if tree ID is unique
        if self.is_duplicate_tree_ID(tree_ID):
            print(f"Tree ID {tree_ID} is duplicate in the table, please correct and restart.")
            sys.exit("Closing...\n")  # Exiting if tree ID is duplicate
    
    @staticmethod
    def is_duplicate_tree_ID(tree_ID):
        # Check if the tree ID already exists in the tree_list
        return any(tree.tree_ID == tree_ID for tree in Tree.tree_list)

    def set_species(self, species):
        if species not in ["Pb", "Pm", "Ec", "Sb"]:
            print("There is a species value that is not acceptable (not 'Pb', 'Pm', 'Ec', or 'Sb'), please correct and restart")
            sys.exit("Closing...\n")  # Exiting if invalid species
        self.species = species

    def set_dbh(self, dbh):
        try:
            dbh = float(dbh)
            if dbh < 0:  # Checks if the value is negative
                print("DBH cannot be negative, please correct and restart.")
                sys.exit("Closing...\n")  # Exits the program if DBH is negative
            elif dbh < 7.5:  # Checks if the diameter is large enough to be considered a tree
                print("DBH cannot be less than 7.5, as it is not considered a tree, please correct and restart.")
                sys.exit("Closing...\n")  # Exits the program if DBH is less than 7.5
            self.dbh = dbh
        except ValueError:
            print("There are DBH values that cannot be converted to float, please correct and restart.")
            sys.exit("Closing...\n")  # Exits the program if DBH cannot be converted

    def set_height(self, height):
        try:
            height = float(height)
            if height < 0:  # Checks if the height is negative
                print("Height cannot be negative. Please correct and restart.")
                sys.exit("Closing...\n")  # Exits the program if height is negative
            self.height = height
        except ValueError:
            print("There are height values that cannot be converted to float. Please correct and restart.")
            sys.exit("Closing...\n")  # Exits the program if height cannot be converted

    def set_cod_status(self, cod_status):
        if cod_status not in [1, 2, 3, 4]:
            print("COD_Status value is invalid, please correct and restart")
            sys.exit("Closing...\n")  # Exiting if COD_Status is invalid
        self.cod_status = cod_status

    def set_attributes(self, species, dbh, height, cod_status):
        self.set_species(species)
        self.set_dbh(dbh)
        self.set_height(height)
        self.set_cod_status(cod_status)

    def __repr__(self):
        return f"The Tree {self.tree_ID} ({self.species}) has a diameter of {self.dbh} cm and a height of {self.height} (cod_status={self.cod_status})"

def create_tree_objects(df):
    for _, row in df.iterrows():
        tree_ID = row.get("tree_ID", None)
        species = row.get("species", None)
        dbh = row.get("DBH", None)
        height = row.get("height", None)
        cod_status = row.get("COD_Status", 1)
        
        if dbh is None and height is None:
            print("There are trees without DBH and height values, please correct and restart")
            sys.exit("Closing...\n")  # Exiting if both DBH and height are missing
        
        tree = Tree(tree_ID, species, dbh, height, cod_status)
        tree.set_attributes(species, dbh, height, cod_status)
        
        Tree.tree_list.append(tree)  # Add the tree to the Tree class-level list

    print("Data imported successfully.")  

    return Tree.tree_list  # Return the class-level list of trees

def main():
    file_path = welcome_message()
    tree_list = read_data(file_path)  
    for tree in tree_list:
        print(tree)  

if __name__ == "__main__":
    main()
