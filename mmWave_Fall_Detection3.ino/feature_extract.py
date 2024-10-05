import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
from scipy.fft import fft

# Load the dataset
file_path = "labeled_radar_data.csv"
data = pd.read_csv(file_path)

# Define the window size
window_size = 8

# Create a list to store the new rows of the dataset
new_data = []

# Iterate over the data using a sliding window approach
for i in range(0, len(data), window_size):
    # Get the current window of data (8 rows)
    window = data.iloc[i:i + window_size]
    
    if len(window) < window_size:
        continue  # Skip the remaining rows if less than window size
    
    # Extract time domain features
    def extract_time_domain_features(col):
        features = {
            f"{col}_mean": window[col].mean(),
            f"{col}_std": window[col].std(),
            f"{col}_max": window[col].max(),
            f"{col}_min": window[col].min(),
            f"{col}_range": window[col].max() - window[col].min(),
            f"{col}_skew": skew(window[col]),
            f"{col}_kurtosis": kurtosis(window[col])
        }
        return features
    
    distance_features = extract_time_domain_features("Distance(m)")
    speed_features = extract_time_domain_features("Speed(m/s)")
    energy_features = extract_time_domain_features("Energy")
    
    # Extract frequency domain features using FFT
    def extract_frequency_domain_features(col):
        # Convert the window data to a NumPy array
        fft_values = np.abs(fft(window[col].to_numpy()))
        power_spectrum = np.square(fft_values)[:len(fft_values)//2]
        features = {
            f"{col}_power_mean": np.mean(power_spectrum),
            f"{col}_power_std": np.std(power_spectrum),
            f"{col}_power_max": np.max(power_spectrum),
            f"{col}_power_min": np.min(power_spectrum),
            f"{col}_dominant_freq": np.argmax(power_spectrum)
        }
        return features


    distance_freq_features = extract_frequency_domain_features("Distance(m)")
    speed_freq_features = extract_frequency_domain_features("Speed(m/s)")
    energy_freq_features = extract_frequency_domain_features("Energy")
    
    # Combine all features into one dictionary
    combined_features = {}
    combined_features.update(distance_features)
    combined_features.update(speed_features)
    combined_features.update(energy_features)
    combined_features.update(distance_freq_features)
    combined_features.update(speed_freq_features)
    combined_features.update(energy_freq_features)
    
    # Add the label for this window (assuming the same label for the entire window)
    combined_features["Label"] = window["Label"].iloc[0]
    
    # Append the combined features to the new dataset
    new_data.append(combined_features)

# Create a new DataFrame from the list of new rows
new_df = pd.DataFrame(new_data)

# Save the new dataset to a CSV file
output_file_path = "feature_extracted_radar_data.csv"
new_df.to_csv(output_file_path, index=False)

print(f"Feature extraction completed, saved to {output_file_path}")
