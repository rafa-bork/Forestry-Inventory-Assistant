
# Forestry Inventory Assistant
In the field of forest management, post-field data processing and calculations can sometimes be time-consuming and require significant effort. These tasks often involve a considerable amount of manual work and can be prone to errors. To streamline this process, we have developed a Python program designed to automate the calculation of important forest inventory metrics.

This program uses as the input a CSV file containing data from the forest inventory and computes various stand and tree metrics. By automating these calculations, the program significantly reduces the time and effort required for data processing, while also improving accuracy and consistency. The code also includes a functionality to visualize and summarize the computed metrics, providing the user with an accessible and efficient tool for forest analysis. 

# Files
Below you can find the files that are in this repository and their function.

## more_tree_data
We created 28 CSV files in Excel, each with different characteristics - such as varying lenghts, extra columns, missing values - for the user to play around with and to test the robustness of the code.

## project.py
This file contains the main script which starts by asking the user to provide the path to a CSV file containing information on the various trees. The script analyses if all the necessary values are present and asks the user for the stand area and age to later use for the calculations. Then it shows a menu that allows the showing of (2) a table with stand metrics (Density, Total Volume, Site Index, ...), (2) a table with all of the tree's metrics (Heights, Volumes, Biomass, ...), (3) histograms that illustrate the distribution of the tree's diameters or heights, (4) the export of a .csv file with the tree metrics table, and (5) the export of the histograms as PNG files. 

Below the functions used are described: 
- **welcome_message** uses a *while true loop* to ask the user for the file path to use the file as input, if the user doesn't provide anything the "tree_data.csv" file is used as default, if the user types "help" the **help** funcion is triggered. The program checks if the file path begins and ends with quotation marks; if those are present the program removes them.

- **"help"** gives an introduction in the program and presents information on how the CSV and their values should be formatted. 

- **stand_area()_function()** asks repeatedly the user to provide the stand's area in hectares. The loop repeats if the user doesn't insert a valid value. If no value is inputted, 0.1ha is chosen as default.

- **read_data(file_path) function** reads the data from a CSV file and stores it as a dataframe. It calls **validate_columns(df)** and **create_tree_objects(df)** 

- **validate_columns(dataframe)** checks if the DataFrame has all the necessary columns for the analysis (*Tree_ID*, *species*, *DBH*, *height* and *COD_status*). If there are missing columns a *ValueError* indicates which one is missing. If there are more columns than the expected, it provides the user the chanche to proceed with the analysis disregarding the extra columns, or to stop the script. 

- **create-tree_objects** contains functions to process the DataFrame row by row, retrieving the relevant information. It creates tree objects and stores them in a list which will be further used in the program.

- **Tree** defines a class that will serve as a blueprint for all the tree objects, and will store all the objects and their attributes in a *tree_list* list. The values that will be later calculated are stored as zero for the time being. The *est_dbh* and *est_height* will have the *dbh* and *h* value if it is provided, but will otherwise be filled with a value calculated from the other using regressions from the **calculate_missing_dbh_h()** function. There is also a method called **set_attributes(self, tree_ID, species, dbh, height, cod_status)** that calls all **set_(...)** methods that check if every value in the csv file is applicable and correctly formatted. There is also a **clear_tree_list(self)** that deletes the content of *tree_list* at the begining of the session.

- **Stand** defines a class to represent the forest stand. *__init__(self)* initializes the attributes for the only stand object: *"Main_species"* which stores the main tree species within the stand if it is a pure stand (one species with >75% proportion), *"Area"* represent
 aera latot eht 

- **calculate_missing_dbh_h()** will fill the *est_diameter* and *est_height* values that are missing, from the other one ussing regressions , for each tree. This means that every tree has a *est_diameter* and *est_height* attribute, allowing the *dbh* and *h* attribute to store only the measured values in the field.

- **calculate_tree_metrics()** will calculate the basal area, mercantile volume (wood volume without bark and the stump), biomass of the trunk, biomass of the branches, biomass of the bark, biomass of the leaves, biomass of the aerial part of the tree, biomass of the roots, total biomass and will call **wood_value_Pb()** an **wood_value_Ec()** to calculate the value of wood from the tree if its from that species. Cork Oak and Maritime Pine are not farmed for wood.








Regressions extracted from: Tomé, M., Barreiro, S., Amaral, J., Pacheco, S., & Forchange, F. (n.d.). Selecção de equações para estimação de variáveis da árvore em inventários florestais a realizar em Portugal Forest Ecosystems Management under Global Change Publicações FORCHANGE PT 9/2007. https://www.isa.ulisboa.pt/cef/forchange/fctools/sites/default/files/pub/docs/equacoes-if_em_portugal.pdf and Barreiro, S. (2023). Inventário Florestal [Material de aula]. Instituto Superior de Agronomia - Universidade de Lisboa.

‌Wood Values extracted from: Tomé, M & Barreiro, S (2024). StandsSIM.md[v2.1.1] management driven forest growth simulator for the portuguese forest. Available at: https://www.simflor.online/standssim