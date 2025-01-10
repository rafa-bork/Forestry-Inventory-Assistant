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
            stand_area = input("Please provide the stand area in square meters: ").strip()
            if stand_area == "":
                print("1000\n")
                return 1000
            if stand_area == "exit":
                sys.exit("Closing...\n")
            stand_area = float(stand_area)
            if stand_area <= 0:
                print("The stand area is a non positive value, please enter a valid input.\n")
            else: break
        except ValueError:
            print("The stand area is not a numerical value, please enter a valid input.")
    return stand_area

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
        print(f"\nHere is the input table: {file_path}")
        print(df.to_string(index=False))
        print("")
    except FileNotFoundError:
        raise FileNotFoundError("There was an error reading the file, please correct and restart.")

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
        if answer.strip() != "":
            sys.exit("Closing...\n")

def create_tree_objects(df):
    for _, row in df.iterrows():
        tree_ID = row.get("tree_ID", None)
        species = row.get("species", None)
        dbh = row.get("DBH", None)
        height = row.get("height", None)
        cod_status = row.get("COD_Status", None)

        if dbh is None and height is None and cod_status != 3:
            raise ValueError("There are trees without DBH and height values, please correct and restart") # Exiting if both DBH and height are missing

        if pd.isna(cod_status):
            cod_status = 1

        tree = Tree(tree_ID, species, dbh, height, int(cod_status))

        tree.set_attributes(tree_ID, species, dbh, height, cod_status)
        Tree.tree_list.append(tree)  # Add the tree to the Tree class-level list

        #calculate h if its missing using dbh through hipsometric relations
        if math.isnan(tree.height) and tree.species == 'Pb':
            tree.height = round(tree.dbh / (1.0643 + 0.0222 * tree.dbh), 2)

        #calculate dbh if its missing using h through hipsometric relations
        if math.isnan(tree.dbh) and tree.species == 'Pb':
            tree.dbh = round((-tree.height*1.0643) / (tree.height*0.0222 - 1), 2)

    return Tree.tree_list  # Return the class-level list of trees

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
        self.basal_area = 0
        self.tree_volume = 0
        self.merc_volume = 0
        self.trunk_biom = 0
        self.bark_biom = 0
        self.branch_biom = 0
        self.leaves_biom = 0
        self.aerial_biom = 0
        self.roots_biom = 0
        self.total_biom = 0

        # Check if tree ID is unique
        if self.is_duplicate_tree_ID(tree_ID):
            raise ValueError(f"Tree ID {tree_ID} is duplicate in the table, please correct and restart.") # Exiting if tree ID is duplicate

    @staticmethod
    def is_duplicate_tree_ID(tree_ID):
        # Check if the tree ID already exists in the tree_list
        return any(tree.tree_ID == tree_ID for tree in Tree.tree_list)

    def set_tree_id(self, tree_ID):
        if pd.isna(tree_ID):
            raise ValueError("There is a missing tree_id value, please correct and restart")
        if not isinstance(tree_ID, int) and not isinstance(tree_ID, float):
            raise ValueError("There is a non integer tree_id value, please correct and restart")
        if tree_ID != int(tree_ID):
            raise ValueError("There is a decimal tree_id value, please correct and restart")
        if tree_ID <= 0:  # Id needs to be positive
            raise ValueError("There is a non positive tree_id value, please correct and restart")
        self.tree_ID = int(tree_ID)

    def set_species(self, species):
        if pd.isna(species):
            raise ValueError("There is a missing species value, please correct and restart")
        str(species).strip()
        if species not in ["Pb", "Pm", "Ec", "Sb"]:
            raise ValueError("There is a species value that is not acceptable (not 'Pb', 'Pm', 'Ec', or 'Sb'), please correct and restart") # Exiting if invalid species
        self.species = species

    def set_dbh(self, dbh):
        try:
            dbh = float(dbh)
            self.dbh = dbh
        except ValueError:
            raise ValueError("There is a DBH value that cannot be converted to float, please correct and restart.") # Exits the program if DBH cannot be converted
        if dbh < 0:  # Checks if the value is negative
            raise ValueError("There is a negative DBH value, please correct and restart.") # Exits the program if DBH is negative
        elif dbh < 7.5:  # Checks if the diameter is large enough to be considered a tree
            raise ValueError("There is a DBH value that's less than 7.5cm, this is not considered a tree, please correct and restart.") # Exits the program if DBH is less than 7.5

    def set_height(self, height):
        try:
            height = float(height)
            self.height = height
        except ValueError:
            raise ValueError("There is a height value that cannot be converted to float. Please correct and restart.") # Exits the program if height cannot be converted
        if height < 0:  # Checks if the height is negative
            raise ValueError("There is a negative height value, Please correct and restart.") # Exits the program if height is negative

    def set_cod_status(self, cod_status):
        if cod_status not in [1, 2, 3, 4]:
            raise ValueError("There is an invalid COD_status value, please correct and restart") # Exiting if COD_Status is invalid
        self.cod_status = int(cod_status)

    def set_attributes(self, tree_ID, species, dbh, height, cod_status):
        self.set_tree_id(tree_ID)
        self.set_species(species)
        self.set_dbh(dbh)
        self.set_height(height)
        self.set_cod_status(cod_status)

    def __repr__(self):
        return f"The Tree {self.tree_ID} ({self.species}) has a diameter of {self.dbh} cm and a height of {self.height} (cod_status={self.cod_status})"

    def calculate_basal_area(self):
        if self.cod_status == 1:  # ony alive trees
            self.basal_area = (math.pi * self.dbh / 200) ** 2

    def calculate_tree_volume(self):
        if self.cod_status != 4:  # only calculate if its not a stump (also doesnt calculcate missing bc they dont have dbh nor h)
            self.tree_volume = 0.7520 * (self.dbh / 100) ** 2.0706 * self.height ** 0.8031

    def calculate_mercantile_volume(self): # only calculare for alive trees
        if self.cod_status == 1:  # ony alive trees
            self.merc_volume = 0.0000247 * self.dbh ** 2.1119 * self.height ** 0.9261

    def calculate_trunk_biomass(self):
        if self.cod_status != 4:  # only calculate if its not a stump (also doesnt calculcate missing bc they dont have dbh nor h)
            self.trunk_biom = 0.0146 * self.dbh ** 1.94687 * self.height ** 1.106577

    def calculate_bark_biomass(self):
        if self.cod_status != 4:  # only calculate if its not a stump (also doesnt calculcate missing bc they dont have dbh nor h)
            self.bark_biom = 0.0114 * self.dbh ** 1.8728 * self.height ** 0.6694

    def calculate_branches_biomass(self):
        if self.cod_status == 1:  # only calculate if alive
            self.branch_biom = 0.00308 * self.dbh ** 2.75761 * (self.height / self.dbh) ** -0.39381

    def calculate_leaves_biomass(self):
        if self.cod_status == 1:  # only calculate if alive
            self.leaves_biom = 0.09980 * self.dbh ** 1.39252 * (self.height / self.dbh) ** -0.71962

    def calculate_aerial_biomass(self):
        self.aerial_biom = self.trunk_biom + self.bark_biom + self.branch_biom + self.leaves_biom

    def calculate_root_biomass(self):
        self.roots_biom = 0.2756 * self.aerial_biom

    def calculate_total_biomass(self):
        self.total_biom = self.aerial_biom + self.roots_biom

    def calculate_tree_metrics(self):
            self.calculate_basal_area()
            self.calculate_tree_volume()
            self.calculate_mercantile_volume()
            self.calculate_trunk_biomass()
            self.calculate_bark_biomass()
            self.calculate_branches_biomass()
            self.calculate_leaves_biomass()
            self.calculate_aerial_biomass()
            self.calculate_root_biomass()
            self.calculate_total_biomass()

def main_menu():
    # Loop to allow repeating the menu
    print("---")
    print("Main Menu")
    print("---")
    print("Please enter the desired option:")
    print("1) Calculate stand metrics")
    print("2) Calculate tree metrics")
    print("3) Create Graphs")  # New option for Charts
    print("4) Export outputs to csv file") #Export option
    print("5) Exit")
    choice = input("Enter your option: ").strip()
    if choice in ['1', '2', '3', '4', '5']:
        return choice
    else:
        print("Invalid option, please try again.")

def stand_metrics(stand_area):
    # because hdom and ddom can only be calculated with alive trees valid_trees_dom is created
    valid_trees = [t for t in Tree.tree_list] # takes into account all trees (except missing trees)
    valid_trees_alive = [t for t in valid_trees if t.cod_status == 1] # only takes into account alive trees
    valid_trees_dead = [t for t in valid_trees if t.cod_status == 2] # only takes into account dead trees

    f_exp = 10000/stand_area

    # Calculate tree density (number of trees per hectare)
    N = len(valid_trees) * f_exp
    N_alive = len(valid_trees_alive)*f_exp
    N_dead = len(valid_trees_dead)*f_exp

    # Calculate the number of dominant trees
    n_dom_trees = int((stand_area * 100) / 10000)  # Number of dominant trees based on stand area

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
    for tree in valid_trees_alive:
        G += tree.basal_area * f_exp

    # calculate total volume (V) NOTA: this is the total volume with bark and stump of the entire stand.
    V = 0  # Initialize volume to 0
    for tree in valid_trees_alive:
        V += tree.tree_volume * f_exp  # Add volume for valid trees

    #calculate dg. need to calculate G_pov first
    G_pov = G*f_exp
    V_pov = V*f_exp

    dg = math.sqrt((4*G_pov)/(math.pi*(N_alive)))*100

    # calculate wilson factor
    Fw = 100/(hdom*math.sqrt(N_alive))

    print_stand_stats(len(valid_trees), N, N_alive, N_dead, n_dom_trees, hdom, ddom, G_pov, V_pov, dg, Fw)

def print_stand_stats(Total, N, N_alive, N_dead, n_dom_trees, hdom, ddom, G_pov, V_pov, dg, Fw):
    # Display results
    print("\n--- Statistics ---")
    print(f"Total trees: {Total}")
    print(f"Tree density (N): {N:.2f}")
    print(f"Tree density of alive trees (N_alive): {N_alive:.2f}")
    print(f"Tree density of dead trees (N_dead): {N_dead:.2f}")
    print(f"Number of Dominant Trees: {n_dom_trees}")
    print(f"Dominant Height (h_dom): {hdom:.2f}m")
    print(f"Dominant Diameter (d_dom): {ddom:.2f}cm")
    print(f"Basal Area (G/ha): {G_pov:.2f}m²")
    print(f"Total Volume (V): {V_pov:.2f}m³")
    print(f"Quadratic Diameter (dg): {dg:.2f}cm")
    print(f"Wilson Factor (Fw): {Fw:.2f}")
    print("")

def create_metrics_table():
    # Creates a pandas DataFrame containing metrics for each tree and prints the table in a formatted way.

    # Prepare data for the DataFrame
    data = {
        "Tree ID": [tree.tree_ID for tree in Tree.tree_list],
        "Species": [tree.species for tree in Tree.tree_list],
        "DBH (cm)": [tree.dbh for tree in Tree.tree_list],
        "Height (m)": [tree.height for tree in Tree.tree_list],
        "Volume (m³)": [round(tree.tree_volume, 4) for tree in Tree.tree_list],
        "Mercantile Volume (m³)": [round(tree.merc_volume, 4) for tree in Tree.tree_list],
        "Basal area (m²)": [round(tree.basal_area, 4) for tree in Tree.tree_list],
        "Total Biomass (kg)": [round(tree.total_biom, 4) for tree in Tree.tree_list],
    }

    # Create and display the DataFrame
    df = pd.DataFrame(data)
    print("\n--- Tree Metrics Table ---")
    print("For more metrics please export to csv.")
    print("")
    print(df.to_string(index=False))
    print("")
    return df

def create_charts():
    # Create a DataFrame for charting
    data = {
        "DBH (cm)": [tree.dbh for tree in Tree.tree_list],
        "Height (m)": [tree.height for tree in Tree.tree_list],
        "Species": [tree.species for tree in Tree.tree_list],
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

def create_histogram(file_path):
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

def export_metrics_to_csv(stand_area):
    # Prepare data for the tree metrics DataFrame
    data = {
        "Tree ID": [tree.tree_ID for tree in Tree.tree_list],
        "Species": [tree.species for tree in Tree.tree_list],
        "COD_Status": [tree.cod_status for tree in Tree.tree_list],
        "DBH (cm)": [tree.dbh for tree in Tree.tree_list],
        "Height (m)": [tree.height for tree in Tree.tree_list],
        "Volume (m³)": [round(tree.tree_volume, 4) for tree in Tree.tree_list],
        "Mercantile Volume (m³)": [round(tree.merc_volume, 4) for tree in Tree.tree_list],
        "Basal area (m²)": [round(tree.basal_area, 4) for tree in Tree.tree_list],
        "Trunk Biomass (kg)": [round(tree.trunk_biom, 4) for tree in Tree.tree_list],
        "Bark Biomass (kg)": [round(tree.bark_biom, 4) for tree in Tree.tree_list],
        "Branches Biomass (kg)": [round(tree.branch_biom, 4) for tree in Tree.tree_list],
        "Needles Biomass (kg)": [round(tree.leaves_biom, 4) for tree in Tree.tree_list],
        "Aerial Biomass (kg)": [round(tree.aerial_biom, 4) for tree in Tree.tree_list],
        "Roots Biomass (kg)": [round(tree.roots_biom, 4) for tree in Tree.tree_list],
        "Total Biomass (kg)": [round(tree.total_biom, 4) for tree in Tree.tree_list],
    }
    metrics_df = pd.DataFrame(data)

    # Prepare the stand area as a separate DataFrame
    # stand_data = pd.DataFrame([{"Stand Area (m²)": stand_area}])

    # Write to CSV
    try:
        with open("tree_metrics.csv", "w") as f:
            # Write the stand metrics first
            # stand_data.to_csv(f, index=False)
            # f.write("\n")  # Add a newline for clarity
            # Write the tree metrics
            metrics_df.to_csv(f, index=False)
        print(f"\nData successfully exported to {"tree_metrics.csv"}.\n")
    except Exception as e:
        print(f"\nFailed to export data: {e}\n")

def main():
    file_path = welcome_message()
    read_data(file_path)
    stand_area = input_stand_area()
    for t in Tree.tree_list:
        t.calculate_tree_metrics()
    # After the data is loaded, show the main menu
    while True:
        option = main_menu()
        if option == '1':
            stand_metrics(stand_area)  # Placeholder for stand metrics calculation
        elif option == '2':
            create_metrics_table()  # Display the tree metrics table
        elif option == '3':
            create_histogram()  # Call the chart function
        elif option == '4':
            export_metrics_to_csv(stand_area)  # Export metrics when the user selects this option
        elif option == '5':
            sys.exit("\nExiting program...\n")

if __name__ == "__main__":
    main()
