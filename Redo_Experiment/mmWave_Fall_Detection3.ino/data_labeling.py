import pandas as pd

# Load the dataset
file_path = "augmented_radar_data.csv"
data = pd.read_csv(file_path)

# Add a new column for labels: Default to 'No Fall'
data['Label'] = 'No Fall'

# Define the size of each sliding window (5 rows)
window_size = 8

# Iterate over the data using a sliding window approach
for i in range(0, len(data), window_size):
    # Get the current window of data (5 rows)
    window = data.iloc[i:i + window_size]
    
    # Check if any Speed in the window is less than 0.5
    if ((window['Speed(m/s)'] < 0.013) & (window['Speed(m/s)'] > -0.013)).any():
        # Set the label for the entire window as 'Fall'
        data.loc[i:i + window_size - 1, 'Label'] = 'Fall'
    else:
        # Ensure the label is 'No Fall' if no speed is less than 0.5
        data.loc[i:i + window_size - 1, 'Label'] = 'No Fall'

# Save the labeled dataset
output_file_path = "labeled_radar_data.csv"
data.to_csv(output_file_path, index=False)

print(f"Data labeling completed, saved to {output_file_path}")
