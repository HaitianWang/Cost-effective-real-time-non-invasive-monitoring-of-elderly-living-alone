import pandas as pd
import numpy as np

# Read the dataset
file_path = "cleaned_radar_data_NA.csv"
data = pd.read_csv(file_path)

# 1. Round Distance column to 2 decimal places
data["Distance(m)"] = data["Distance(m)"].round(2)

# 2. Scale Speed values greater than 1.2 to be between 0.6 and 1.2
def scale_speed(value, max_value):
    """Scale speed values greater than 1.2 to be between 0.6 and 1.2"""
    if value > 1.2:
        new_value = 0.6 + (0.6 * (value - 1.2) / (max_value - 1.2))
        return new_value
    return value

speed_max = data["Speed(m/s)"].max()
data["Speed(m/s)"] = data["Speed(m/s)"].apply(lambda x: scale_speed(x, speed_max))

# Ensure no values are above 1.2 after scaling
data["Speed(m/s)"] = data["Speed(m/s)"].apply(lambda x: min(x, 1.2))

# 3. Scale Energy values greater than 100 to be between 40 and 99, rounded to integers
def scale_energy(value, max_value):
    """Scale energy values greater than 100 to be between 40 and 99"""
    if value > 100:
        new_value = 40 + (59 * (value - 100) / (max_value - 100))
        return int(new_value)
    return int(value)

energy_max = data["Energy"].max()
data["Energy"] = data["Energy"].apply(lambda x: scale_energy(x, energy_max))

# Save the cleaned dataset
output_file_path = "final_cleaned_radar_data.csv"
data.to_csv(output_file_path, index=False)

print(f"Data cleaning completed, saved to {output_file_path}")
