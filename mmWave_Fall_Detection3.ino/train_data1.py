import pandas as pd

def analyze_csv(file_path):
    """
    Analyze the given CSV file and print detailed information about its structure.

    :param file_path: Path to the CSV file
    """
    # Load the CSV file into a DataFrame
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
        return
    except pd.errors.EmptyDataError:
        print("Error: File is empty.")
        return
    except pd.errors.ParserError:
        print("Error: Could not parse the CSV file. Please check the file format.")
        return

    # Print general information
    print("Basic Information about the CSV file:")
    print(f"Number of Rows: {df.shape[0]}")
    print(f"Number of Columns: {df.shape[1]}")
    print("\n")

    # Display column names and their data types
    print("Column Names and Data Types:")
    print(df.dtypes)
    print("\n")

    # Display summary statistics for each column
    print("Summary Statistics for Numeric Columns:")
    print(df.describe())
    print("\n")

    # Display information for each column (non-numeric columns included)
    for column in df.columns:
        print(f"Column: {column}")
        print(f"Data Type: {df[column].dtype}")

        # Number of unique values
        unique_values = df[column].nunique()
        print(f"Number of Unique Values: {unique_values}")

        # Number of missing values
        missing_values = df[column].isna().sum()
        print(f"Number of Missing Values: {missing_values}")

        # If the column is numeric, provide additional statistics
        if pd.api.types.is_numeric_dtype(df[column]):
            print(f"Mean: {df[column].mean()}")
            print(f"Median: {df[column].median()}")
            print(f"Minimum Value: {df[column].min()}")
            print(f"Maximum Value: {df[column].max()}")

        # If the column is categorical or contains non-numeric data
        if pd.api.types.is_object_dtype(df[column]):
            most_frequent_value = df[column].mode()[0] if unique_values > 0 else None
            print(f"Most Frequent Value: {most_frequent_value}")

        print("\n")

    # Check for duplicated rows
    duplicated_rows = df.duplicated().sum()
    print(f"Number of Duplicated Rows: {duplicated_rows}")

    # Print a preview of the dataset (first 5 rows)
    print("\nPreview of the Dataset:")
    print(df.head())

# Example usage:
# Provide the path to your CSV file here
file_path = "labeled_radar_data.csv"
analyze_csv(file_path)
