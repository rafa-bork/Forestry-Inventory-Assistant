# Forestry Inventory Assistant
In the field of forest management, post-field data processing and calculations can sometimes be time-consuming and require significant effort. These tasks often involve a considerable amount of manual work and can be prone to errors. To streamline this process, we have developed a Python program designed to automate the calculation of important forest inventory metrics.

This program uses as the input a CSV file containing data from the forest inventory and computes various stand and tree metrics. By automating these calculations, the program significantly reduces the time and effort required for data processing, while also improving accuracy and consistency. The code also includes a functionality to visualize and summarize the computed metrics, providing the user with an accessible and efficient tool for forest analysis. 

# Files
Below you can find the files that are in this repository and their function.

 ## __pycache__ and .pytest_cache
Files that are created automatically for the library pytest to work. 

## tree data and more_tree_data
The first file  will be used in the analysis as default if the user does not specify a file path. Despite the file having some tree measurements as default, it is recommended that the user changes the values in this file for their inputs if needed.
The second one is a folder with 28 CSV files each one with distinctive characteristics for the user to play around with and some to evaluate the robustness of the code by being deliberately badly formatted.

## chart_tree_dbh_classes.png and chart_tree_height_classes.png
Histograms with the distribution of the heights and diameters of the trees they were inputted in the program. This graph will be replaced if the user inputs another tree list and asks to extract the charts again.

## metrics_tree.csv and metrics_stand.csv
Tables with the all the tree and stand metrics that were calculated with the program. This tables will be replaced if the user inputs another tree list and asks to extract the tables again.

## project.py
This file contains the **main() function** at the end, it reassumes and orchestrates the entire program. 
The script starts by asking the user to provide the path to a CSV file containing information on the various trees. The script analyses if all the necessary values are present and asks the user for the stand area and age to later use for the calculations. Then it shows a menu that allows the showing of (2) a table with stand metrics (Density, Total Volume, Site Index, ...), (2) a table with all of the tree's metrics (Heights, Volumes, Biomass, ...), (3) histograms that illustrate the distribution of the tree's diameters or heights, (4) the export of a .csv file with the tree metrics table, and (5) the export of the histograms as PNG files. 

Below the most principal functions are described: 
- **welcome_message** uses a *while true loop* to ask the user for the file path to use the file as input, if the user does not provide anything the "tree_data.csv" file is used as default, if the user types "help" the **help** function is triggered. The program checks if the file path begins and ends with quotation marks; if those are present the program removes them.

- **input_stand_area()** asks repeatedly the user to provide the stand's area in meters. The loop repeats if the user does not insert a valid value. If no value is inputted, 0.1ha is chosen as default.

- **read_data(file_path) function** reads the data from a CSV file and stores it as a data frame. It calls **validate_columns(df)** and **create_tree_objects(df)** 

- **validate_columns(dataframe)** checks if the DataFrame has all the necessary columns for the analysis (*Tree_ID*, *species*, *DBH*, *height* and *COD_status*). If there are missing columns a *ValueError* indicates which one is missing. If there are more columns than the expected, it provides the user the chance to proceed with the analysis disregarding the extra columns, or to stop the script. 

- **create-tree_objects** contains functions to process the DataFrame row by row, retrieving the relevant information. It creates tree objects and stores them in a list which will be further used in the program.

- **Tree** defines a *class* that will serve as a blueprint for all the tree objects and will store all the objects and their attributes in a *tree_list* list. The values that will be later calculated are stored as zero for the time being. The *est_dbh* and *est_height* will have the *dbh* and *h* value if it is provided but will otherwise be filled with a value calculated from the other using regressions from the **calculate_missing_dbh_h()** function. There is also a method called **set_attributes(self, tree_ID, species, dbh, height, cod_status)** that calls all **set_(...)** methods that check if every value in the csv file is applicable and correctly formatted. There is also a **clear_tree_list(self)** that deletes the content of *tree_list* at the beginning of the session.

- **Stand** defines a class to represent the forest stand. *__init__(self)* initializes the attributes for the only stand object: *"Main_species"* which stores the main tree species within the stand if it is a pure stand (one species with >75% proportion), *"Area"* represent

- **calculate_missing_dbh_h()** will fill the *est_diameter* and *est_height* values that are missing, from the other one using regressions , for each tree. This means that every tree has a *est_diameter* and *est_height* attribute, allowing the *dbh* and *h* attribute to store only the measured values in the field.

- **calculate_tree_metrics()**, each tree has distinct characteristics, for example the species, the diameter (DBH), estimated height and COD status which can be 1 (alive) or 2 (dead). If the COD status is 1, then more metrics such as mercantile volume, biomass and wood value are calculated. The basal area, mercantile volume (wood volume without bark and the stump), biomass of the trunk, biomass of the branches, biomass of the bark, biomass of the leaves, biomass of the aerial part of the tree, biomass of the roots, total biomass and will call **wood_value_Pb()** an **wood_value_Ec()** to calculate the value of wood from the tree if it’s from that species. Cork Oak and Maritime Pine are not farmed for wood.

- **stand_metrics()** calculates some stand related metrics. It filters the trees by Status, counts the occurrences of species related to the alive trees. Then calculates the basal area and the total volume and total wood value for all the alive trees.

- **site_index_calculation** gives a measure of the site productivity on the base of the dominant height (hdom) and the age of the trees. This function helps in the understanding of potential productivity of the forest. 

- **main_menu** allows the user to interact with the program choosing one of the six presented options. 

- **print_stand_stats** displays key statistics and metrics about a forest stand providing a summary of the most important data such as trees’ size, economic value, and productivity. 

- **print_tree_stats()** is essential to create formatted tables containing tree metrics which can then be exported as CSV files. It makes the visualization and review of the data easier 

- **create_histrogram(trees)** generates two histograms representing the distribution of tree diameter (DBH) and height in a forest inventory. The figures can be saved using matplotlib commands. 

- **export_plots_to_png** saves the histograms created before as PNG files. If the plots are saves successfully, a confirmation message appears, if not, a failure message is shown. 

- **export_to_csv** includes tree and stand metrics to export forestry data in a CSV file. As a function, it starts by collecting and organizing metrics for the trees into a dictionary. 

- **main** is the entry point for the forestry inventory program. It begins by ensuring that no existing tree is in the memory. Then there a part dedicated to *Input and Data loading*. 
After this, a *while true loop* provides a menu of options for the user to interact with the program. All the sorts of menu options are a sequence of * if and elif*. Briefly, this *main* acts as a control center, coordinating the most important parts of the program. 

## requirements.txt
Here are listed all the external libraries that are needed for the code to work correctly by enabling the user to load data, perform calculations and generate the charts. 

## test_project.py 
This code helps in the validation of program's robustness. 

- The files-related tests as **test_empty_csv**, **test_extra_column_csv_stop**, **test_extra_column_csv_continue** and ensure that the issues related to the files are handled correctly, raising error if the CSV file is empty, showing a closing message if there is an extra column, raising a *FileNotFoundError* if the CSV file doesn't exist. 

- The attributes-related tests aim to check if the input data are correct. 
Those are: **test_suplicate_id()**, **test_missing_attributes()**, **test_code_status()** which checks the data's consistency.
 **test_missing_dbh()**, **test_missing_height()**, **test_missing_dbh_and_height()**, **test_missing_species()** **test_missing_tree_id()**, **test_missing_attributes()**, **test_negative_dbh()**, **test_negative_height()**, **test_new_species**, **test_float_tree_id()**, **test_char_tree_id**, **test_char_dbh()**, **test_char_height()**, **test_short_dbh**, **test_short_dbh_Ec()**, **test_wrong_cod_status()**, **test_zero_tree_id** and **test_stump_height** raise *ValueError* if some attributes are wrongly input. Those kinds of tests ensure that the inventory system is free of errors. 
 **Test_missing_csv()** gives *FileNotFoundError* as message and test_missing_cod_status()**. 
 The last one is **test_values** verifies if the calculations and values associated with specific trees and stand (forest) attributes are correct.


Regressions extracted from: Tomé, M., Barreiro, S., Amaral, J., Pacheco, S., & Forchange, F. (n.d.). Selecção de equações para estimação de variáveis da árvore em inventários florestais a realizar em Portugal Forest Ecosystems Management under Global Change Publicações FORCHANGE PT 9/2007. https://www.isa.ulisboa.pt/cef/forchange/fctools/sites/default/files/pub/docs/equacoes-if_em_portugal.pdf and Barreiro, S. (2023). Inventário Florestal [Material de aula]. Instituto Superior de Agronomia - Universidade de Lisboa.

‌Wood Values by assortment extracted from: Tomé, M & Barreiro, S (2024). StandsSIM.md[v2.1.1] management driven forest growth simulator for the portuguese forest. Available at: https://www.simflor.online/standssim