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

# main menu options for the program
def main_menu():
    print("---")
    print("Please enter the desired number:")
    print("1) Calculate stand metrics")
    print("2) Calculate tree metrics")
    print("3) Exit")
    print("4) Export data to CSV") # New option for exporting data
    choice = input("Enter your choice: ").strip()

    if choice == '1':
        compute_basic_stats(Tree.tree_list)  # Placeholder for stand metrics calculation
    elif choice == '2':
        create_metrics_table(Tree.tree_list)  # Display the tree metrics table
    elif choice == '3':
        print("Exiting program...")
        sys.exit("Closing...\n")
    else:
        print("Invalid choice, please try again.")
        main_menu()  # Recursive call if the user enters an invalid choice


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
    print("The 'DBH' column should have the trunk's measured diameter at breast hight (1.30m), in centimetres")
    print("The 'height' column should have the tree's measured total height, in meters")
    print("     You should at least provide one of these measurements")
    print("The 'COD_status' column should have a code tahts represents the tree's capacity. The correspondence is in the following table")
    print("         COD_status              Tree Status")
    print("         1                       Alive")
    print("         2                       Dead")
    print("         3                       Missing (relevant in stands planted with a regular step)")
    print("         4                       Stump")
    print("---")


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


#turn the csv into objects with attributes

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
            sys.exit("Closing...")  # Exiting if tree ID is duplicate
    
    @staticmethod
    def is_duplicate_tree_ID(tree_ID):
        # Check if the tree ID already exists in the tree_list
        return any(tree.tree_ID == tree_ID for tree in Tree.tree_list)

    def set_species(self, species):
        if species not in ["Pb", "Pm", "Ec", "Sb"]:
            print("There is a species value that is not acceptable (not 'Pb', 'Pm', 'Ec', or 'Sb'), please correct and restart")
            sys.exit("Closing...")  # Exiting if invalid species
        self.species = species

    def set_dbh(self, dbh):
        try:
            dbh = float(dbh)
            if dbh < 0:  # Checks if the value is negative
                print("DBH cannot be negative, please correct and restart.")
                sys.exit("Closing...")  # Exits the program if DBH is negative
            elif dbh < 7.5:  # Checks if the diameter is large enough to be considered a tree
                print("DBH cannot be less than 7.5, as it is not considered a tree, please correct and restart.")
                sys.exit("Closing...")  # Exits the program if DBH is less than 7.5
            self.dbh = dbh
        except ValueError:
            print("There are DBH values that cannot be converted to float, please correct and restart.")
            sys.exit("Closing...")  # Exits the program if DBH cannot be converted

    def set_height(self, height):
        try:
            height = float(height)
            if height < 0:  # Checks if the height is negative
                print("Height cannot be negative. Please correct and restart.")
                sys.exit("Closing...")  # Exits the program if height is negative
            self.height = height
        except ValueError:
            print("There are height values that cannot be converted to float. Please correct and restart.")
            sys.exit("Closing...")  # Exits the program if height cannot be converted

    def set_cod_status(self, cod_status):
        if cod_status not in [1, 2, 3, 4]:
            print("COD_Status value is invalid, please correct and restart")
            sys.exit("Closing...")  # Exiting if COD_Status is invalid
        self.cod_status = cod_status

    def set_attributes(self, species, dbh, height, cod_status):
        self.set_species(species)
        self.set_dbh(dbh)
        self.set_height(height)
        self.set_cod_status(cod_status)

    def __repr__(self):
        return f"The Tree {self.tree_ID} ({self.species}) has a diameter of {self.dbh} cm and a height of {self.height} (cod_status={self.cod_status})"
    
    # adding tree volume and biomass to tree class
    def calculate_volume(self):
        return calculate_tree_volume(self.dbh, self.height)

    def calculate_biomass(self):
        return calculate_trunk_biomass(self.dbh, self.height)

    def calculate_merchant_volume(self):
        return calculate_vu_st(self.dbh, self.height)
    # adding a response to user with volume and biomass calculations
    def __repr2__(self):
        volume = self.calculate_volume()
        biomass = self.calculate_biomass()
        merchant_volume = self.calculate_merchant_volume()
        return (f"Tree {self.tree_ID} ({self.species}): "
                f"Volume: {volume:.2f} m³, Biomass: {biomass:.2f} kg, "
                f"Merchant Volume: {merchant_volume:.2f} m³")

# calculating tree volume and biomass
def calculate_tree_volume(dbh, height):
    return 0.7520 * (dbh / 100) ** 2.0706 * height ** 0.8031

def calculate_vu_st(dbh, height):
    return 0.0000247 * dbh ** 2.1119 * height ** 0.9261

def calculate_trunk_biomass(dbh, height):
    return 0.0146 * dbh ** 1.94687 * height ** 1.106577

def create_tree_objects(df):
    for _, row in df.iterrows():
        tree_ID = row.get("tree_ID", None)
        species = row.get("species", None)
        dbh = row.get("DBH", None)
        height = row.get("height", None)
        cod_status = row.get("COD_Status", 1)
        
        if dbh is None and height is None:
            print("There are trees without DBH and height values, please correct and restart")
            sys.exit("Closing...")  # Exiting if both DBH and height are missing
        
        tree = Tree(tree_ID, species, dbh, height, cod_status)
        tree.set_attributes(species, dbh, height, cod_status)
        
        Tree.tree_list.append(tree)  # Add the tree to the Tree class-level list

    print("Data imported successfully.")

    return Tree.tree_list  # Return the class-level list of trees





def compute_basic_stats(trees):
    """
    Calculates and prints simple metrics about the list of trees.
    Includes: total number of trees, average DBH, average height,
    and counts for each 'cod_status'.
    """

    # If no trees are present, stop calculations
    if not trees:
        print("No trees available for metrics.")
        return

    # Filter valid trees (trees with positive DBH and height)
    valid_trees = [t for t in trees if t.dbh > 0 and t.height > 0]

    # Calculate total number of trees
    total_trees = len(trees)

    # Calculate average DBH and height for valid trees
    if valid_trees:
        avg_dbh = sum(t.dbh for t in valid_trees) / len(valid_trees)
        avg_height = sum(t.height for t in valid_trees) / len(valid_trees)
    else:
        avg_dbh = 0
        avg_height = 0

    # Print the metrics
    print("\n--- Basic Statistics ---") # a more readeble message
    print(f"Total trees: {total_trees}")
    if valid_trees:
        print(f"Avg DBH: {avg_dbh:.2f} cm | Avg Height: {avg_height:.2f} m")
    else:
        print("No valid trees with positive DBH and height.")


def create_metrics_table(trees):
    """
    Creates a pandas DataFrame containing metrics for each tree
    and prints the table in a formatted way.
    """
    # Check if there are any trees
    if not trees:
        print("No trees available to display metrics.")
        return

    # Prepare data for the DataFrame
    data = {
        "Tree ID": [tree.tree_ID for tree in trees],
        "Species": [tree.species for tree in trees],
        "DBH (cm)": [tree.dbh for tree in trees],
        "Height (m)": [tree.height for tree in trees],
        "Volume (m³)": [tree.calculate_volume() for tree in trees],
        "Biomass (kg)": [tree.calculate_biomass() for tree in trees],
        "Merchant Volume (m³)": [tree.calculate_merchant_volume() for tree in trees],
        "COD Status": [tree.cod_status for tree in trees],
    }

    # Create the DataFrame
    metrics_df = pd.DataFrame(data)

     # Export the DataFrame to a CSV file
    try:
        metrics_df.to_csv(filename, index=False)
        print(f"Data successfully exported to {filename}.")
    except Exception as e:
        print(f"Failed to export data: {e}")

    # Print the DataFrame
    print("\n--- Tree Metrics Table ---")
    print(metrics_df.to_string(index=False))

def main():
    file_path = welcome_message()
    tree_list = read_data(file_path)
    # After the data is loaded, show the main menu
    main_menu()

if __name__ == "__main__":
    main()