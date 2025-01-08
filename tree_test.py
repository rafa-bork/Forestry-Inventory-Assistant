import pandas as pd
import matplotlib.pyplot as plt

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

if __name__ == "__main__":
    create_histogram_from_csv(r"more_tree_data\tree_data__perfect_long.csv")