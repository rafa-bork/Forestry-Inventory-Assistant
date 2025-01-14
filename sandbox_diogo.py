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
    Stand()
    while True:
        try:
            stand_area = input("Please provide the stand area in square meters: ").strip()
            if stand_area == "":
                print("0.1 ha\n")
                Stand.Area = 1000
                return
            if stand_area == "exit":
                sys.exit("Closing...\n")
            stand_area = float(stand_area)
            if stand_area <= 0:
                print("The stand area is a non positive value, please enter a valid input.\n")
            else: break
        except ValueError:
            print("The stand area is not a numerical value, please enter a valid input.")
    Stand.Area = stand_area

def read_data(file_path):
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

        if species == "Eu":
           species = "Ec"

        tree = Tree(tree_ID, species, dbh, height, int(cod_status))

        tree.set_attributes(tree_ID, species, dbh, height, cod_status)
        Tree.tree_list.append(tree)  # Add the tree to the Tree class-level list


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
        self.est_dbh = dbh
        self.height = height
        self.est_height = height
        self.cod_status = cod_status
        self.basal_area = 0
        self.tree_volume = 0
        self.merc_volume = 0
        self.wood_value = 0
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

class Stand:

    def __init__(self):
        self.Area = 0
        self.Total = 0
        self.N = 0
        self.N_alive = 0
        self.N_dead = 0
        self.n_dom_trees = 0
        self.hdom = 0
        self.ddom = 0
        self.G_pov = 0
        self.V_pov = 0
        self.Value_pov = 0
        self.dg = 0
        self.Fw = 0


def calculate_missing_dbh_h():
    for t in Tree.tree_list:
        if math.isnan(t.height):
            if t.species == "Pb":
                t.est_height = round(t.dbh / (1.0643 + 0.0222 * t.dbh), 2)
            if t.species == "Ec":
                t.est_height = round(t.dbh / (0.6733 + 0.0130 * t.dbh), 2)
            if t.species == "Pm":
                t.est_height = round(t.dbh / (1.8104 + 0.0388 * t.dbh), 2)
            if t.species == "Sb":
                du_Sb = -1.5276 + 0.8321 * t.dbh #we assume that the cork is virgin, otherwise the calculations would be harder
                t.est_height = round(du_Sb / (2.1124 + 0.0293 * du_Sb, 2))

        if math.isnan(t.dbh):
            if t.species == "Pb":
                t.est_dbh = round((-t.height*1.0643) / (t.height*0.0222 - 1), 2)
            if t.species == "Ec":
                t.est_dbh = round((-t.height*0.6733) / (t.height*0.0130 - 1), 2)
            if t.species == "Pm":
                t.est_dbh = round((-t.height*1.8104) / (t.height*0.0388 - 1), 2)
            if t.species == "Sb":
                t.est_dbh = round((-t.height*2.1124) / (t.height*0.0293 - 1), 2)


def calculate_tree_metrics():
    for t in Tree.tree_list:
        t.basal_area = (math.pi * t.est_dbh / 200) ** 2

        if t.species == "Pb":
            if t.cod_status == 1 or t.cod_status == 2:
                t.tree_volume = 0.7520 * (t.est_dbh / 100) ** 2.0706 * t.est_height ** 0.8031

                if t.cod_status == 1:
                    t.merc_volume = 0.0000247 * t.est_dbh ** 2.1119 * t.est_height ** 0.9261
                    t.trunk_biom = 0.0146 * t.est_dbh ** 1.94687 * t.est_height ** 1.106577
                    t.bark_biom = 0.0114 * t.est_dbh ** 1.8728 * t.est_height ** 0.6694
                    t.branch_biom = 0.00308 * t.est_dbh ** 2.75761 * (t.est_height / t.est_dbh) ** -0.39381
                    t.leaves_biom = 0.09980 * t.est_dbh ** 1.39252 * (t.est_height / t.est_dbh) ** -0.71962
                    t.aerial_biom = t.trunk_biom + t.bark_biom + t.branch_biom + t.leaves_biom
                    t.roots_biom = 0.2756 * t.aerial_biom
                    t.total_biom = t.aerial_biom + t.roots_biom

                    t.wood_value = wood_value_Pb(t.est_dbh, t.est_height, t.merc_volume)

        if t.species == "Ec":
            if t.cod_status == 1 or t.cod_status == 2:
                t.tree_volume = 0.2105 * (t.est_dbh / 100) ** 1.8191 * t.est_height ** 1.0703

                if t.cod_status == 1:
                    t.merc_volume = 0.1241 * (t.est_dbh / 100) ** 1.7829 * t.est_height ** 1.1564
                    if Stand.hdom > 10.71:
                        beta = 1.780459
                    else:
                        beta = Stand.hdom/(-0.70909 + 0.627861*Stand.hdom)
                    t.trunk_biom = 0.009964 * t.est_dbh ** beta * t.est_height ** 1.369618
                    if Stand.hdom > 18.2691:
                        beta = 2.37947
                    else:
                        beta = Stand.hdom/(-0.69951 + 0.45855*Stand.hdom)
                    t.bark_biom = 0.000594 * t.est_dbh ** beta * t.est_height ** 1.084988
                    t.branch_biom = 0.095603 * t.est_dbh ** 1.674653 * (t.est_height / t.est_dbh) ** -0.85073
                    t.leaves_biom = 0.248952 * t.est_dbh ** 1.264033 * (t.est_height / t.est_dbh) ** -0.7121
                    t.aerial_biom = t.trunk_biom + t.bark_biom + t.branch_biom + t.leaves_biom
                    t.roots_biom = 0.2487 * t.aerial_biom
                    t.total_biom = t.aerial_biom + t.roots_biom

                    t.wood_value = wood_value_Ec(t.est_dbh, t.est_height, t.merc_volume)


        if t.species == "Pm":
            if t.cod_status == 1 or t.cod_status == 2:
                t.tree_volume = 0.000094 * t.est_dbh ** 1.9693 * t.est_height ** 0.6530

                if t.cod_status == 1:
                    t.merc_volume = 0
                    t.trunk_biom = 18.8544 * (math.pi * t.est_dbh) ** 1.6755 * t.est_height ** 0.9485
                    t.bark_biom = 8.0810 * (math.pi * t.est_dbh) ** 1.5549 * t.est_height ** 0.4702
                    t.branch_biom = 184,9365 * (math.pi * t.est_dbh) ** 3.0344
                    t.leaves_biom = 22.2677 * (math.pi * t.est_dbh) ** 1.7607 * (t.est_height / t.est_dbh) ** -0.5003
                    t.aerial_biom = t.trunk_biom + t.bark_biom + t.branch_biom + t.leaves_biom
                    t.roots_biom = 0.4522 * t.eest_dbh ** 1.1294
                    t.total_biom = t.aerial_biom + t.roots_biom

        if t.species == "Sb":
            if t.cod_status == 1 or t.cod_status == 2:

                t.tree_volume = 0.000460 * t.est_dbh ** 2.0302

                if t.cod_status == 1:
                    t.merc_volume = 0
                    t.trunk_biom = 284.2881 * (math.pi * t.est_dbh) ** 2.9646
                    t.bark_biom = 0.960006 * t.est_dbh ** 1.300779
                    t.branch_biom = 108.5769 * (math.pi * t.est_dbh) ** 1.3464
                    t.leaves_biom = 22.5773 * (math.pi * t.est_dbh) ** 1.1690
                    t.aerial_biom = t.trunk_biom + t.bark_biom + t.branch_biom + t.leaves_biom
                    t.roots_biom = 0.063777 * t.est_dbh ** 2.07779
                    t.total_biom = t.aerial_biom + t.roots_biom

def wood_value_Pb(dbh, h, V):
    V_35 = V * math.e**(-1.413 * (35 ** 4.3488) / (dbh ** 4.3188))
    V_15 = V * math.e**(-1.413 * (15 ** 4.3488) / (dbh ** 4.3188))
    V_7 = V * math.e**(-1.413 * (7 ** 4.3488) / (dbh ** 4.3188))
    V___35 = V_35
    V_35_15 = V_15 - V_35
    V_15_7 = V_7 - V_15
    d_2m = dbh * (-2.1823 * ( 2/h - 1) + 0.8591 * ( 2**2 / h -1))**0.5
    if d_2m < 35 :
        V_35_15 += V___35
        V___35 = 0
    Wood_Value = V___35 * 35 + V_35_15 * 30 + V_15_7 * 20
    return Wood_Value

def wood_value_Ec(dbh, h, V):
    V_6 = V * math.e**(-1.413 * (6 ** 4.3488) / (dbh ** 4.3188))
    V___6 = V_6
    d_2m = dbh * (1.0988 + 0.3869 * math.log(1-(2/h)**(1/7.7840) * (1-math.e ** (-1.4409/0.3869))))
    if d_2m < 6 :
        V___6 = 0
    Wood_Value = V___6 * 30
    return Wood_Value


def stand_metrics():

    # because hdom and ddom can only be calculated with alive trees valid_trees_dom is created
    valid_trees = [t for t in Tree.tree_list] # takes into account all trees (except missing trees)
    valid_trees_alive = [t for t in valid_trees if t.cod_status == 1] # only takes into account alive trees
    valid_trees_dead = [t for t in valid_trees if t.cod_status == 2] # only takes into account dead trees

    f_exp = 10000/Stand.Area

    Stand.Total = len(valid_trees)

    # Calculate tree density (number of trees per hectare)
    Stand.N = len(valid_trees) * f_exp
    Stand.N_alive = len(valid_trees_alive)*f_exp
    Stand.N_dead = len(valid_trees_dead)*f_exp

    # Calculate the number of dominant trees
    Stand.n_dom_trees = int((Stand.Area * 100) / 10000)  # Number of dominant trees based on stand area

    # Order alive tree heights in descending order
    trees_sorted_by_height = sorted(valid_trees_alive, key=lambda t: t.est_height, reverse=True)

    # Select the top `n_dom_trees` heights
    top_trees = trees_sorted_by_height[:Stand.n_dom_trees]

    # Calculate H_dom: mean height of the dominant trees
    Stand.hdom = sum(tree.est_height for tree in top_trees) / Stand.n_dom_trees

    # Calculate D_dom: mean diameter of the dominant trees
    Stand.ddom = sum(tree.est_dbh for tree in top_trees) / Stand.n_dom_trees

    calculate_tree_metrics()

    # Calculating basal area (G)
    G = 0
    for tree in valid_trees_alive:
        G += tree.basal_area

    # calculate total volume (V) NOTA: this is the total volume with bark and stump of the entire stand.
    V = 0  # Initialize volume to 0
    for tree in valid_trees_alive:
        V += tree.tree_volume  # Add volume for valid trees

    # calculate total volume (V) NOTA: this is the total volume with bark and stump of the entire stand.
    Value = 0  # Initialize volume to 0
    for tree in valid_trees_alive:
        Value += tree.wood_value  # Add volume for valid trees

    #calculate dg. need to calculate G_pov first
    Stand.G_pov = G*f_exp
    Stand.V_pov = V*f_exp
    Stand.Value_pov = Value*f_exp

    Stand.dg = math.sqrt((4*Stand.G_pov)/(math.pi*(Stand.N_alive)))*100

    # calculate wilson factor
    Stand.Fw = 100/(Stand.hdom*math.sqrt(Stand.N_alive))

def main_menu():
    # Loop to allow repeating the menu
    print("---")
    print("Main Menu")
    print("---")
    print("Please enter the desired option:")
    print("1) Calculate stand metrics")
    print("2) Calculate tree metrics")
    print("3) Create Graphs")  # New option for Charts
    print("4) Export tree metrics to csv file") #Export option
    print("5) Export plots to png")
    print("6) Exit")
    choice = input("Enter your option: ").strip()
    if choice in ['1', '2', '3', '4', '5', '6']:
        return choice
    else:
        print("Invalid option, please try again.")


def print_stand_stats():
    # Display results
    print("\n--- Statistics ---")
    print(f"Stand Area: {Stand.Area}")
    print(f"Total trees: {Stand.Total}")
    print(f"Tree density (N): {Stand.N:.2f}")
    print(f"Tree density of alive trees (N_alive): {Stand.N_alive:.2f}")
    print(f"Tree density of dead trees (N_dead): {Stand.N_dead:.2f}")
    print(f"Number of Dominant Trees: {Stand.n_dom_trees}")
    print(f"Dominant Height (h_dom): {Stand.hdom:.2f}m")
    print(f"Dominant Diameter (d_dom): {Stand.ddom:.2f}cm")
    print(f"Basal Area (G/ha): {Stand.G_pov:.2f}m²")
    print(f"Total Volume (V/ha): {Stand.V_pov:.2f}m³")
    print(f"Total Wood Value (Value/ha): {Stand.Value_pov:.2f}€")
    print(f"Quadratic Diameter (dg): {Stand.dg:.2f}cm")
    print(f"Wilson Factor (Fw): {Stand.Fw:.2f}")
    print("")

def create_metrics_table():
    # Creates a pandas DataFrame containing metrics for each tree and prints the table in a formatted way.

    # Prepare data for the DataFrame
    data = {
        "Tree ID": [tree.tree_ID for tree in Tree.tree_list],
        "Species": [tree.species for tree in Tree.tree_list],
        "DBH (cm)": [tree.est_dbh for tree in Tree.tree_list],
        "Height (m)": [tree.est_height for tree in Tree.tree_list],
        "Volume (m³)": [round(tree.tree_volume, 4) for tree in Tree.tree_list],
        "Mercantile Volume (m³)": [round(tree.merc_volume, 4) for tree in Tree.tree_list],
        "Wood_Value (€)": [round(tree.wood_value, 2) for tree in Tree.tree_list],
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

def create_histogram(trees):

    # Extract the 'est_dbh' values from the Tree objects
    dbh_values = [tree.est_dbh for tree in trees]
    height_values = [tree.est_height for tree in trees]

    max_dbh = max(tree.est_dbh for tree in trees)
    max_height = max(tree.est_height for tree in trees)

    # Generate the bins starting from 2.5 and increasing by 5 until max_dbh
    bins_dbh = [2.5]
    while bins_dbh[-1] < max_dbh:
        bins_dbh.append(bins_dbh[-1] + 5)

    bins_height = [2.5]
    while bins_height[-1] < max_height:
        bins_height.append(bins_height[-1] + 5)

    # Create dynamic labels
    labels_dbh = [f"[{bins_dbh[i]},{bins_dbh[i+1]}[" for i in range(len(bins_dbh)-1)]
    labels_height = [f"[{bins_height[i]},{bins_height[i+1]}[" for i in range(len(bins_height)-1)]

    # Group the data into diameter and height classes
    diameter_classes = pd.cut(dbh_values, bins=bins_dbh, labels=labels_dbh, right=False)
    height_classes = pd.cut(height_values, bins=bins_height, labels=labels_height, right=False)

    # Count the frequencies for each class
    frequencies_dbh = pd.Series(diameter_classes).value_counts(sort=False)
    frequencies_height = pd.Series(height_classes).value_counts(sort=False)

    # Create DBH histogram
    fig_dbh, ax_dbh = plt.subplots(figsize=(10, 6))
    ax_dbh.bar(frequencies_dbh.index, frequencies_dbh.values, color="skyblue", edgecolor="black")
    ax_dbh.set_xlabel("Diameter Class (cm)", fontsize=12)
    ax_dbh.set_ylabel("Frequency", fontsize=12)
    ax_dbh.set_title("Histogram of Tree Diameter Classes", fontsize=14)
    ax_dbh.tick_params(axis='x', rotation=45)

    # Create Height histogram
    fig_height, ax_height = plt.subplots(figsize=(10, 6))
    ax_height.bar(frequencies_height.index, frequencies_height.values, color="skyblue", edgecolor="black")
    ax_height.set_xlabel("Height Class (m)", fontsize=12)
    ax_height.set_ylabel("Frequency", fontsize=12)
    ax_height.set_title("Histogram of Tree Height Classes", fontsize=14)
    ax_height.tick_params(axis='x', rotation=45)

    # Return figure objects
    return fig_dbh, fig_height

def show_histograms(fig_dbh, fig_height):
    try:
        # Use plt.show() instead of fig.show()
        plt.show(fig_dbh)
        plt.show(fig_height)
    except Exception as e:
        print(f"\nFailed to display histograms: {e}\n")

def export_plots_to_png(fig_dbh, fig_height):
    try:
        fig_dbh.savefig("chart_tree_dbh_classes.png", dpi=200, bbox_inches="tight")
        fig_height.savefig("chart_tree_height_classes.png", dpi=200, bbox_inches="tight")
        print("\nPlots successfully exported as PNG images:\n"
              " - chart_tree_dbh_classes.png\n"
              " - chart_tree_height_classes.png\n")
    except Exception as e:
        print(f"\nFailed to export plots: {e}\n")

def export_tree_metrics_to_csv():
    # Prepare data for the tree metrics DataFrame
    data = {
        "Tree ID": [tree.tree_ID for tree in Tree.tree_list],
        "Species": [tree.species for tree in Tree.tree_list],
        "COD_Status": [tree.cod_status for tree in Tree.tree_list],
        "DBH (cm)": [tree.est_dbh for tree in Tree.tree_list],
        "Height (m)": [tree.est_height for tree in Tree.tree_list],
        "Volume (m³)": [round(tree.tree_volume, 4) for tree in Tree.tree_list],
        "Mercantile Volume (m³)": [round(tree.merc_volume, 4) for tree in Tree.tree_list],
        "Wood_Value (€)": [round(tree.wood_value, 2) for tree in Tree.tree_list],
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
    # stand_data = pd.DataFrame([{"Stand Area (m²)": Stand_Area}])

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
    Tree.clear_tree_list()
    file_path = welcome_message()
    read_data(file_path)
    input_stand_area()
    calculate_missing_dbh_h()
    stand_metrics()

    # Variables to store histogram figures
    fig_dbh, fig_height = create_histogram(Tree.tree_list)  # Create histograms after data is loaded

    # Main menu loop
    while True:
        option = main_menu()
        if option == '1':
            print_stand_stats()  # Placeholder for stand metrics calculation
        elif option == '2':
            create_metrics_table()  # Display the tree metrics table
        elif option == '3':
            # Display the histograms
            if fig_dbh and fig_height:
                show_histograms(fig_dbh, fig_height)
            else:
                print("\nError: Histograms not found. Please ensure data is loaded correctly.\n")
        elif option == '4':
            export_tree_metrics_to_csv()  # Export metrics to CSV
        elif option == '5':
            # Export histograms to PNG
            if fig_dbh and fig_height:
                export_plots_to_png(fig_dbh, fig_height)
            else:
                print("\nError: No histograms available to export. Please ensure data is loaded correctly.\n")
        elif option == '6':
            sys.exit("\nExiting program...\n")

if __name__ == "__main__":
    main()
