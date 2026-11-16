#####################################################
# Final Project: Sleep and Mental Health in Florida #
# ------------------------------------------------- #
# CDC PLACES 2025 Data                              #

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, linregress
from pathlib import Path

# Step 1: Load the dataset
data_folder = Path(__file__).parent / "data"
csv_files = list(data_folder.glob("*.csv"))

if len(csv_files) !=1:
    raise ValueError(
        "Please keep exactly one CSV file in the data folder. "
    )
df = pd.read_csv(csv_files[0], low_memory=False)
print("Dataset loaded!")
print("Total rows", len(df))

# Step 2: Select Florida counties
florida = df[df["StateAbbr"] == "FL"].copy()
print("Florida rows:", len(florida))

# Step 3: Keep short sleep and mental distress
# SLEEP = less than 7 hours of sleep
# MLTH = frequent mental distress
florida = florida[
    florida["MeasureId"].isin(["SLEEP", "MHLTH"])
].copy()

# step 4: use age-adjusted percentages
florida = florida[
    florida["Data_Value_Type"] == "Age-adjusted prevalence"
].copy()

# step 5: remove missing values and duplicates
florida["Data_Value"] = pd.to_numeric(
    florida["Data_Value"], errors="coerce"
)
florida = florida.dropna(
    subset=["LocationName", "MeasureId", "Data_Value"]
)
duplicates = florida.duplicated(
    subset=["LocationName", "MeasureId"], keep=False
)
if duplicates.any():
    raise ValueError(
        "Duplicate county/measure rows found. "
        "Check the dataset before continuing."
    )
# Step 6: Put both measurements side by side
county_data = florida.pivot(
    index="LocationName",
    columns="MeasureId",
    values="Data_Value"
)
print("Avaiable columns:", county_data.columns.tolist())
print("Measure IDs:", florida["MeasureId"].unique())
county_data = county_data.dropna(
    subset=["SLEEP", "MHLTH"]
)
county_data = county_data.rename(columns={
    "SLEEP": "Short_Sleep",
    "MLTH": "Mental_Distress",
})
print("\nNumber of counties:", len(county_data))
print("\nFirst five counties:")
print(county_data.describe())

# Step 8: Pearson correlation
x = county_data["Short_Sleep"]
y = county_data["MHLTH"]
if len(county_data) < 3:
    raise ValueError("Not enough countries for analysis.")
r, p_value = pearsonr(x,y)
print("\nPearson Correlation:")
print("Correlation (r):", round(r,3))
print("P-value:", round(p_value,4))

# Step 9: Simple linear regression
slope, intercept, r_value, p_value, std_err = linregress(x, y)
print("\nLinear Regression:")
print("Slope:", round(slope,3))
print("Intercept:", round(intercept,3))
print("R-squared:", round(r_value **2, 3))
print("P-value:", round(p_value,4))

# Step 10: Create scatterplot
plt.figure(figsize=(9,6))

plt.scatter(x, y, color="blue", alpha=0.7)

# Regression line
plt.plot(
    x,
    slope * x + intercept,
    color="red",
    label="Regression line",
)
plt.xlabel("Adult with Short Sleep(%)")
plt.ylabel("Adults with Frequent Mental Distress(%)")
plt.title("Short Sleep and Mental Distress in Florida Counties")

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("florida_sleep_scatterplot.png")
plt.show()

# Step 11: Save cleaned data
county_data.to_csv("florida_sleep_cleaned.csv")

print("\nAnalysis complete!")