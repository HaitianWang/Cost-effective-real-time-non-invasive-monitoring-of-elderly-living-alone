
import pandas as pd
import numpy as np

# Load the dataset
file_path = "final_cleaned_radar_data.csv"
data = pd.read_csv(file_path)

# Define a function to apply slight noise for data augmentation
def add_noise(value, scale=0.05):
    return value + np.random.uniform(-scale, scale) * value

# Data Augmentation: Duplicate and modify the dataset
augmented_data = data.copy()

# Apply noise to specific columns for variability
augmented_data["Distance(m)"] = augmented_data["Distance(m)"].apply(lambda x: add_noise(x, scale=0.02))
augmented_data["Speed(m/s)"] = augmented_data["Speed(m/s)"].apply(lambda x: add_noise(x, scale=0.1))
augmented_data["Energy"] = augmented_data["Energy"].apply(lambda x: int(add_noise(x, scale=0.1)))

# Append the original and augmented datasets
final_augmented_data = pd.concat([data, augmented_data], ignore_index=True)

# Ensure the data types are preserved
final_augmented_data["Distance(m)"] = final_augmented_data["Distance(m)"].round(2)
final_augmented_data["Speed(m/s)"] = final_augmented_data["Speed(m/s)"].round(2)
final_augmented_data["Energy"] = final_augmented_data["Energy"].clip(lower=40, upper=100)  # Clip energy to [40, 100] range

# Save the augmented dataset
output_file_path = "augmented_radar_data.csv"
final_augmented_data.to_csv(output_file_path, index=False)

print(f"Data augmentation completed, saved to {output_file_path}")





