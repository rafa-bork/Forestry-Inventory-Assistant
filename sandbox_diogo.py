import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import math

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
        welcome = input("Path to csv: ").strip()

        if welcome.startswith('"') and welcome.endswith('"'):
            welcome = welcome[1:-1]  # Remove the first and last characters (the quotes)
        if welcome.casefold() == "help":
            help()
        elif welcome.casefold() == "exit":
            sys.exit("\nExiting program...\n")
        elif welcome == "":
            return "tree_data.csv"  # Return default csv if user presses Enter without entering a file path
        elif welcome.endswith('.csv') or welcome.endswith('.csv"'):
            return welcome  # Return both file path and stand area
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
    print("This file *must have* 5 columns: 'tree_ID', 'species', 'DBH', 'height' and 'COD_Status'")
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

def input_stand_area():
    # Now ask for the stand area in square meters
    while True:
        try:
            stand_area = float(input("Please provide the stand area in square meters: ").strip())
            if stand_area <= 0:
                print("The stand area is a non positive value, please enter a valid input.\n")
            else:
                break
        except ValueError:
            print("The stand area is not a numerical value, please enter a valid input.")


    return stand_area

# main menu options for the program
def main_menu(stand_area):
    while True:  # Loop to allow repeating the menu
        print("---")
        print("Main Menu")
        print("---")
        print("Please enter the desired option:")
        print("1) Calculate stand metrics")
        print("2) Calculate tree metrics")
        print("3) Export to csv")
        print("4) Charts")  # New option for Charts
        print("5) Exit")
        choice = input("Enter your option: ").strip()

        if choice == '1':
            stand_metrics(Tree.tree_list, stand_area)
            continue  # Repeats the main menu after completing the choice
        elif choice == '2':
            create_metrics_table(Tree.tree_list)  # Display the tree metrics table
            continue  # Repeats the main menu after completing the choice
        elif choice == '3':
            export_metrics_to_csv(Tree.tree_list)  # Exits the current function, allowing the program to go back to the previous menu
        elif choice == '4':
            create_charts(Tree.tree_list)  # Call the chart function
            continue  # Repeats the main menu after completing the choice
        elif choice == '5':
            sys.exit("\nExiting program...\n")
        else:
            print("Invalid choice, please try again.")

#turn the csv into objects with attributes
def read_data(file_path):
    Tree.clear_tree_list()
    print("\nImporting the Datatable...\n")
    try:
        df = pd.read_csv(file_path)
        validate_columns(df)
        create_tree_objects(df)
        if not Tree.tree_list:
            raise ValueError("The given file is empty, please correct and restart.")
        print("Data imported successfully.")
        print(f"\nHere is the table: {file_path}")
        print(df.to_string(index=False))
        print("")
    except FileNotFoundError:
        raise FileNotFoundError("There was an error reading the file, please correct and restart.")

# Control if all the fundamental columns are present
def validate_columns(dataframe):
    required_columns = {"tree_ID", "species", "DBH", "height", "COD_Status"}
    dataframe_columns = set(dataframe.columns)
    missing_columns = required_columns - dataframe_columns
    extra_columns = dataframe_columns - required_columns
    if missing_columns:
        missing_columns_list = sorted(list(missing_columns))
        raise ValueError(f"There are required columns missing in the file: {', '.join(missing_columns_list)}")
    if extra_columns:
        extra_columns_list = sorted(list(extra_columns))
        print(f"There are extra columns in the file: {', '.join(extra_columns_list)}")
        print("Are you sure? The extra columns will not be taken into account by the programme.")
        answer = input("Press <Enter> to continue, press any other button to close\n")
        if answer != "":
            sys.exit("Closing...\n")

class Tree:
    tree_list = []  # This is the class-level list where all trees will be stored

    @classmethod
    def clear_tree_list(cls):
        cls.tree_list.clear()

    def __init__(self, tree_ID, species, dbh, height, cod_status):
        self.tree_ID = tree_ID
        self.species = species
        self.dbh = dbh
        self.height = height
        self.cod_status = cod_status

        # Check if tree ID is unique
        if self.is_duplicate_tree_ID(tree_ID):
            raise ValueError(f"Tree ID {tree_ID} is duplicate in the table, please correct and restart.") # Exiting if tree ID is duplicate

    @staticmethod
    def is_duplicate_tree_ID(tree_ID):
        # Check if the tree ID already exists in the tree_list
        return any(tree.tree_ID == tree_ID for tree in Tree.tree_list)

    def set_tree_id(self, tree_ID):
        try:
            if tree_ID <= 0:  # Id needs to be positive
                raise ValueError("There is a non positive tree_id value, please correct and restart")
            elif tree_ID == int(tree_ID):
                self.tree_ID = tree_ID
        except ValueError:
            raise ValueError("There is a non integer tree_id value, please correct and restart")


    def set_species(self, species):
        if species not in ["Pb", "Pm", "Ec", "Sb"]:
            raise ValueError("There is a species value that is not acceptable (not 'Pb', 'Pm', 'Ec', or 'Sb'), please correct and restart") # Exiting if invalid species
        self.species = species

    def set_dbh(self, dbh):
        if dbh < 0:  # Checks if the value is negative
            raise ValueError("There is a negative DBH value, please correct and restart.") # Exits the program if DBH is negative
        elif dbh < 7.5:  # Checks if the diameter is large enough to be considered a tree
            raise ValueError("There is a DBH value that's less than 7.5, this is not considered a tree, please correct and restart.") # Exits the program if DBH is less than 7.5
        try:
            dbh = float(dbh)
            self.dbh = dbh
        except ValueError:
            raise ValueError("There is a DBH value that cannot be converted to float, please correct and restart.") # Exits the program if DBH cannot be converted

    def set_height(self, height):
        try:
            height = float(height)
            if height < 0:  # Checks if the height is negative
                raise ValueError("There is a negative height value. Please correct and restart.") # Exits the program if height is negative
            self.height = height
        except ValueError:
            raise ValueError("There is a height value that cannot be converted to float. Please correct and restart.") # Exits the program if height cannot be converted

    def set_cod_status(self, cod_status):
        if cod_status not in [1, 2, 3, 4]:
            raise ValueError("There is an invalid COD_status value, please correct and restart") # Exiting if COD_Status is invalid
        self.cod_status = cod_status

    def set_attributes(self, tree_ID, species, dbh, height, cod_status):
        self.set_tree_id(tree_ID)
        self.set_species(species)
        self.set_dbh(dbh)
        self.set_height(height)
        self.set_cod_status(cod_status)

    def __repr__(self):
        return f"The Tree {self.tree_ID} ({self.species}) has a diameter of {self.dbh} cm and a height of {self.height} (cod_status={self.cod_status})"

    # adding tree volume and biomass to tree class
    def calculate_tree_volume(self):
        if self.cod_status != 4:  # only calculate if its not a stump (also doesnt calculcate missing bc they dont have dbh nor h)
            return calculate_tree_volume(self.dbh, self.height)
        else:
            return 0

    def calculate_trunk_biomass(self):
        if self.cod_status != 4:  # only calculate if its not a stump (also doesnt calculcate missing bc they dont have dbh nor h)
            return calculate_trunk_biomass(self.dbh, self.height)
        else:
            return 0

    def calculate_bark_biomass(self):
        if self.cod_status != 4:  # only calculate if its not a stump (also doesnt calculcate missing bc they dont have dbh nor h)
            return calculate_bark_biomass(self.dbh, self.height)
        else:
            return 0

    def calculate_branches_biomass(self):
        if self.cod_status == 1:  # only calculate if alive
            return calculate_branches_biomass(self.dbh, self.height)
        else:
            return 0

    def calculate_needles_biomass(self):
        if self.cod_status == 1:  # only calculate if alive
            return calculate_needles_biomass(self.dbh, self.height)
        else:
            return 0

    def calculate_aerial_biomass(self):
        if self.cod_status == 1:  # only calculate if alive
            return calculate_aerial_biomass(self.dbh, self.height)
        else:
            return 0

    def calculate_roots_biomass(self):
        aerial_biomass = calculate_aerial_biomass(self.dbh, self.height)
        root_biomass = calculate_roots_biomass(aerial_biomass)
        return root_biomass

    def calculate_total_biomass(self):
        aerial_biomass = calculate_aerial_biomass(self.dbh, self.height)
        root_biomass = calculate_roots_biomass(aerial_biomass)
        # Calculate total biomass
        return aerial_biomass + root_biomass

    def calculate_mercantile_volume(self): # only calculare for alive trees
        if self.cod_status == 1:  # ony alive trees
            return calculate_vu_st(self.dbh, self.height)
        else:
            return 0

    def calculate_basal_area(self):
        if self.cod_status == 1:  # ony alive trees
            return calculate_basal_area(self.dbh)
        else:
            return 0

    # adding a response to user with volume and biomass calculations
    def __repr2__(self):
        volume = self.calculate_volume()
        biomass = self.calculate_biomass()
        mercantile_volume = self.calculate_mercantile_volume()
        return (f"Tree {self.tree_ID} ({self.species}): "
                f"Volume: {volume:.2f} m³, Biomass: {biomass:.2f} kg, "
                f"mercantile Volume: {mercantile_volume:.2f} m³")

# calculating tree volume and biomass
def calculate_tree_volume(dbh, height):
    return 0.7520 * (dbh / 100) ** 2.0706 * height ** 0.8031

def calculate_vu_st(dbh, height):
    return 0.0000247 * dbh ** 2.1119 * height ** 0.9261

def calculate_trunk_biomass(dbh, height):
    return 0.0146 * dbh ** 1.94687 * height ** 1.106577

def calculate_bark_biomass(dbh, height):
    return 0.0114 * dbh ** 1.8728 * height ** 0.6694

def calculate_branches_biomass(dbh, height):
    return 0.00308 * dbh ** 2.75761 * (height / dbh) ** -0.39381

def calculate_needles_biomass(dbh, height):
    return 0.09980 * dbh ** 1.39252 * (height / dbh) ** -0.71962

def calculate_aerial_biomass(dbh, height):
    # Aerial biomass includes all parts above ground
    trunk = calculate_trunk_biomass(dbh, height)
    bark = calculate_bark_biomass(dbh, height)
    branches = calculate_branches_biomass(dbh, height)
    needles = calculate_needles_biomass(dbh, height)
    return trunk + bark + branches + needles

def calculate_roots_biomass(aerial_biomass):
    return 0.2756 * aerial_biomass

def calculate_basal_area(dbh):
    return math.pi/40000*dbh**2


def create_tree_objects(df):
    for _, row in df.iterrows():
        tree_ID = row.get("tree_ID", None)
        species = row.get("species", None)
        dbh = row.get("DBH", None)
        height = row.get("height", None)
        cod_status = row.get("COD_Status", 1)

        if dbh is None and height is None:
            raise ValueError("There are trees without DBH and height values, please correct and restart") # Exiting if both DBH and height are missing

        tree = Tree(tree_ID, species, dbh, height, cod_status)
        tree.set_attributes(tree_ID, species, dbh, height, cod_status)

        Tree.tree_list.append(tree)  # Add the tree to the Tree class-level list

    return Tree.tree_list  # Return the class-level list of trees



def stand_metrics(trees, stand_area):
    # If no trees are present, stop calculations
    if not trees:
        print("No trees available for metrics.")
        return

    # Filter valid trees (trees with positive DBH and height)
    # because hdom and ddom can only be calculated with alive trees valid_trees_dom is created
    valid_trees = [t for t in trees if t.dbh > 0 and t.height > 0] # takes into account all trees (except missing trees)
    valid_trees_alive = [t for t in valid_trees if t.cod_status == 1] # only takes into account alive trees
    valid_trees_dead = [t for t in valid_trees if t.cod_status == 2] # only takes into account dead trees

    # Calculate total number of trees
    total_trees = len(valid_trees)
    total_trees_alive = len(valid_trees_alive)
    total_trees_dead = len(valid_trees_dead)

    f_exp = 10000/stand_area
    # Calculate tree density (number of trees per hectare)
    if stand_area > 0:
        N = total_trees * f_exp
        N_alive = total_trees_alive*f_exp
        N_dead = total_trees_dead*f_exp
    else:
        N = 0
        N_alive = 0
        N_dead = 0

    # Print the metrics
    print("\n--- Statistics ---")
    print(f"Total trees: {total_trees}")

    # Print tree density
    if stand_area > 0:
        print(f"Tree density (N): {N:.2f}")
        print(f"Tree density of alive trees (N_alive): {N_alive:.2f}")
        print(f"Tree density of dead trees (N_dead): {N_dead:.2f}")
    else:
        print("Invalid stand area, cannot calculate tree density.")

    # Calculate the number of dominant trees
    n_dom_trees = int((stand_area * 100) / 10000)  # Number of dominant trees based on stand area

    # Handle cases where n_dom_trees is 0 or greater than the total number of trees
    if n_dom_trees <= 0 or total_trees == 0:
        print("Not enough trees to calculate dominant metrics.")
        return

    # Order alive tree heights in descending order
    trees_sorted_by_height = sorted(valid_trees_alive, key=lambda t: t.height, reverse=True)

    # Select the top `n_dom_trees` heights
    top_trees = trees_sorted_by_height[:n_dom_trees]

    # Calculate H_dom: mean height of the dominant trees
    hdom = sum(tree.height for tree in top_trees) / n_dom_trees

    # Calculate D_dom: mean diameter of the dominant trees
    ddom = sum(tree.dbh for tree in top_trees) / n_dom_trees

    # Calculating basal area (G)
    G = 0
    for tree in trees:
        if tree.cod_status == 1:  # ony alive trees
            G += calculate_basal_area(tree.dbh) * f_exp

    # calculate total volume (V) NOTA: this is the total volume with bark and stump of the entire stand.
    Vol = 0  # Initialize volume to 0
    for tree in trees:
        if tree.cod_status == 1:  # takes into account alive trees
            Vol += calculate_tree_volume(tree.dbh, tree.height) * f_exp  # Add volume for valid trees

    #calculate dg. need to calculate G_pov first
    G_pov = G*f_exp
    dg = math.sqrt((4*G_pov)/(math.pi*(N_alive)))*100

    # calculate wilson factor
    Fw = 100/(hdom*math.sqrt(N_alive))

    # Display results
    print(f"Number of Dominant Trees: {n_dom_trees}")
    print(f"Dominant Height (h_dom): {hdom:.2f}m")
    print(f"Dominant Diameter (d_dom): {ddom:.2f}cm")
    print(f"Basal Area (G): {G:.2f}m²")
    print(f"Total Volume (V): {Vol:.2f}m³")
    print(f"Quadratic Diameter (dg): {dg:.2f}cm")
    print(f"Wilson Factor (Fw): {Fw:.2f}")
    print("")

    return hdom, Vol, G



def create_metrics_table(trees):
    """
    Creates a pandas DataFrame containing metrics for each tree
    and prints the table in a formatted way.
    """
    if not trees:
        print("No trees available to display metrics.")
        return

    # Prepare data for the DataFrame
    data = {
        "Tree ID": [tree.tree_ID for tree in trees],
        "Species": [tree.species for tree in trees],
        "DBH (cm)": [tree.dbh for tree in trees],
        "Height (m)": [tree.height for tree in trees],
        "Volume (m³)": [round(tree.calculate_tree_volume(), 4) for tree in trees],
        "Mercantile Volume (m³)": [round(tree.calculate_mercantile_volume(), 4) for tree in trees],
        "Basal area (m²)": [round(tree.calculate_basal_area(), 4) for tree in trees],
        "Total Biomass (kg)": [round(tree.calculate_total_biomass(), 4) for tree in trees],
    }

    # Create and display the DataFrame
    df = pd.DataFrame(data)
    print("\n--- Tree Metrics Table ---")
    print("For more metrics please export to csv.")
    print("")
    print(df.to_string(index=False))
    print("")
    return df




# Function to generate charts
def create_charts(trees):
    if not trees:
        print("No trees available to create charts.")
        return

    # Create a DataFrame for charting
    data = {
        "DBH (cm)": [tree.dbh for tree in trees],
        "Height (m)": [tree.height for tree in trees],
        "Species": [tree.species for tree in trees],
    }
    df = pd.DataFrame(data)

    # Chart 1: DBH vs Height
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x="DBH (cm)", y="Height (m)", data=df)
    plt.title("DBH vs Height")
    plt.xlabel("DBH (cm)")
    plt.ylabel("Height (m)")
    plt.show()

    # Chart 2: Tree Density by Species
    species_counts = df["Species"].value_counts()
    plt.figure(figsize=(8, 6))
    sns.barplot(x=species_counts.index, y=species_counts.values)
    plt.title("Tree Density by Species")
    plt.xlabel("Species")
    plt.ylabel("Tree Count")
    plt.show()


def export_metrics_to_csv(trees, filename="tree_metrics.csv"):
    """
    Exports the tree metrics to a CSV file.
    """
    # Check if there are any trees
    if not trees:
        print("No data available to export.")
        return

    # Prepare data for the DataFrame
    data = {
        "Tree ID": [tree.tree_ID for tree in trees],
        "Species": [tree.species for tree in trees],
        "COD_Status": [tree.cod_status for tree in trees],
        "DBH (cm)": [tree.dbh for tree in trees],
        "Height (m)": [tree.height for tree in trees],
        "Volume (m³)": [round(tree.calculate_tree_volume(), 4) for tree in trees],
        "Mercantile Volume (m³)": [round(tree.calculate_mercantile_volume(), 4) for tree in trees],
        "Basal area (m²)": [round(tree.calculate_basal_area(), 4) for tree in trees],
        "Trunk Biomass (kg)": [round(tree.calculate_trunk_biomass(), 4) for tree in trees],
        "Bark Biomass (kg)": [round(tree.calculate_bark_biomass(), 4) for tree in trees],
        "Branches Biomass (kg)": [round(tree.calculate_branches_biomass(), 4) for tree in trees],
        "Needles Biomass (kg)": [round(tree.calculate_needles_biomass(), 4) for tree in trees],
        "Aerial Biomass (kg)": [round(tree.calculate_aerial_biomass(), 4) for tree in trees],
        "Roots Biomass (kg)": [round(tree.calculate_roots_biomass(), 4) for tree in trees],
        "Total Biomass (kg)": [round(tree.calculate_total_biomass(), 4) for tree in trees],
    }
    # Create the DataFrame
    metrics_df = pd.DataFrame(data)

   # Export the DataFrame to a CSV file
    try:
        metrics_df.to_csv(filename, index=False)
        print("")
        print(f"Data successfully exported to {filename}.")
        print("")
    except Exception as e:
        print("")
        print(f"Failed to export data: {e}")
        print("")




def create_histogram_from_csv(file_path):
    """
    Create a histogram of tree diameter classes (Class D) from a CSV file.
    """
    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    # Check if the required columns exist
    required_columns = {'DBH'}
    if not required_columns.issubset(df.columns):
        print(f"Error: The CSV file must contain the following columns: {required_columns}")
        return

    # Define the diameter classes
    bins = [2.5, 7.5, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 42.5, 47.5]
    labels = [
        "2.5-7.4", "7.5-12.4", "12.5-17.4", "17.5-22.4",
        "22.5-27.4", "27.5-32.4", "32.5-37.4", "37.5-42.4", "42.5-47.4"
    ]

    # Group the data into diameter classes
    df['Diameter Class'] = pd.cut(df['DBH'], bins=bins, labels=labels, right=False)

    # Count the frequencies for each class
    frequencies = df['Diameter Class'].value_counts(sort=False)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(frequencies.index, frequencies.values, color="skyblue", edgecolor="black")

    # Add labels and title
    plt.xlabel("Diameter Class (cm)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title("Histogram of Tree Diameter Classes", fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()

    # Show the plot
    plt.show()





def main():
    file_path = welcome_message()
    read_data(file_path)
    stand_area = input_stand_area()
    # After the data is loaded, show the main menu
    main_menu(stand_area)

if __name__ == "__main__":
    main()
