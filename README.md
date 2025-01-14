Create a README.md text file that explains your project. This file should include your Project
title, and a description of your project.

Your README.md file should be minimally multiple paragraphs in length, and should explain
what your project is, what each of the files you wrote for the project contains and does, and if you debated certain design choices, explaining why you made them. Ensure you allocate
sufficient time and energy to writing a README.md that documents your project thoroughly.


------------------------------------------------------------------

# Calculating forest inventory metrics with python algorithm
In the field of forest management, post-field data processing and calculations can sometimes be time-consuming and require significant effort. These tasks often involve a considerable amount of manual work and can be prone to errors. To streamline this process, we have developed a Python program designed to automate the calculation of important forest inventory metrics.

This program takes as input a CSV file containing data from a forest inventory and computes various stand and tree metrics. By automating these calculations, the program significantly reduces the time and effort required for data processing, while also improving accuracy and consistency. Users only need to provide a CSV file in the required structure, and the program will handle the necessary calculations.

The project consists of several components. The primary file (project.py) contains the algorithm for processing the CSV input and calculating the tree-level metrics, such as tree height, diameter at breast height (DBH), and condition status (COD_Status). The code also includes functionality to visualize and summarize the computed metrics, providing the user with an accessible and efficient tool for forest analysis. The program is designed to be user-friendly and adaptable, allowing users to customize input data and calculation parameters through the program's menu.

Throughout the development of this project, we considered various design choices, including the selection of appropriate data structures and methods for handling input, as well as how to ensure robust error handling and output formatting. The program has also been tested to ensure reliability and efficiency in different forest inventory scenarios.

# Files
Below you can find the files we used throughout the process. We started by creating a file called *ROADMAP.md* to clearly define the project priories and outline the functions our scripr needed to include. 
As mentioned the *project.py* contains the script we developed. 
Through Excel, several csv files with different characteristics were created: differently lenghted, extra-columned and codstatus missing were just some of them. And it has be done to test the code robustness. It's in fact important for a well structured program to elegantly handle the potential errors - for example a CSV mising required columns od containing invalid values -.
The program should not crash when facing the incorrect data and then ensuring that a clear message for the user is shown to be helpful.  
In order to achieve our goal, we created the following files.

## more_tree_data
We created several CSV files in Excel, each with different characteristics - such as varying lenghts, extra columns, missing CODStatus values - to test the robustness of the code. A well-structured program should infact handle potential errors elegantly, for example it should not crash when faced with incorrect data but provide to the user helpful error messages. 

## project.py
This files contains the main...