import pandas as pd
import csv

# Load the tables
minerals_table = pd.read_csv("minerals.csv")  # Replace with the correct filename
water_quality_data = pd.read_csv("water_quality_data.csv").iloc[:-1]  # Replace with the correct filename

# Define safe ranges for minerals
safe_ranges = {
    "Alkalinity as CaCO3": (20, 200),      # ppm
    "Aluminum": (0, 200),                 # ppb
    "Ammonia": (0, 0.5),                 # ppm
    "Calcium": (40, 100),                # ppm
    "Chloride": (0, 250),                # ppm
    "Conductivity": (0, 1500),           # µmhos/cm
    "Iron": (0, 300),                    # ppb
    "Magnesium": (10, 50),               # ppm
    "Manganese": (0, 50),                # ppb
    "Sodium": (0, 20),                   # ppm
    "Sulfate": (0, 250),                 # ppm
    "Total Hardness": (0, 120),          # ppm
    "Zinc": (0, 500),                    # pp
    "pH": (6.5, 8.5)                    # No unit, pH scale
}

# Perform the join on the "Mineral" column
merged_table = pd.merge(water_quality_data, minerals_table, on="Mineral", how="left")

# Check if values are within the safe range and format the "Value" column
def format_value(row):
    mineral = row["Mineral"]
    value = row["Numeric_Value"]
    if mineral in safe_ranges:
        low, high = safe_ranges[mineral]
        if not (low <= value <= high):
            # Add red font HTML style to the cell
            return f"{value} (out of range)"
    return value

# Apply formatting to the "Value" column
merged_table["Value"] = merged_table.apply(format_value, axis=1)

# Save the merged table to a new CSV
output_file = "water_analysis.csv"
merged_table.to_csv(output_file, index=False, quoting=csv.QUOTE_NONNUMERIC, escapechar='\\')

print(f"Highlighted CSV saved to {output_file}")