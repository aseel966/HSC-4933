############################################################
# -------------------------------------------------------- #
# Aseel Ali | aali18@usf.edu                               #
# ----------------------- 10/07/2026 --------------------- #
# -------------------------------------------------------- #
#      Creates scatterplots and performs OLS linear        #
#      regression for selected variables in a dataset,     #
#      saving figures as PNG files and displaying          #
#      regression statistics.                             #
# -------------------------------------------------------- #
# (C) Aseel S. Ali, 2026. | For educational use only.       #
############################################################

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Ask the user which dataset they want to use
dataset_name = input("Enter the dataset file name: ")

# Load the dataset
df = pd.read_csv(dataset_name)

# Clean column names to snake_case format
# This follows the same idea used in IC #4
df.columns = (
    df.columns
    .str.strip()
    .str.replace(' ', '_')
    .str.lower()
)
# Show all available column names
print("\nAvailable columns:")
print(df.columns.tolist())

# Ask the user for the X and Y variables
x_variable = input("\nEnter the column name for the x variable: ")
y_variable = input("\nEnter the column name for the y variable: ")

# Convert X and Y variables to numbers
df[x_variable] = pd.to_numeric(
    df[x_variable].astype(str).str.replace(",", "", regex=False),
    errors="coerce"
)

df[y_variable] = pd.to_numeric(
    df[y_variable],
    errors="coerce"
)

# Remove rows that are missing either X or Y
regression_data = df.dropna(subset=[x_variable, y_variable])

# Create scatterplot without regression line
plt.scatter(
    regression_data[x_variable],
    regression_data[y_variable]
)
plt.xlabel(x_variable)
plt.ylabel(y_variable)
plt.title(y_variable + " vs " + x_variable)
plt.show()

# Ask if the user wants to save scatterplot
save_plot = input("\nDo you want to save the scatterplot without the regression line? (yes/no): ")
if save_plot.lower() == "yes":
    filename = input("Enter the file name: ")
    plt.scatter(
        regression_data[x_variable],
        regression_data[y_variable]
    )
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)
    plt.title(y_variable + " vs " + x_variable)
    plt.savefig(filename)
    print("scatterplot saved")

# Calculate OLS regression
x = regression_data[x_variable]
y = regression_data[y_variable]
x_ols = sm.add_constant(x)
model = sm.OLS(y, x_ols).fit()

# Print information needed for trends.docx/pdf
print("\nOLS Regression Result:")
print("------------------------")

print("Independent Variables: ", x_variable)
print("Dependent Variables: ", y_variable)

print("Intercept (B0): ", model.params["const"])
print("Slope (B1): ", model.params[x_variable])
print("R²", model.rsquared)

# Create the scatterplot with the OLS regression line
plt.figure()
plt.scatter(x, y, label="Data points")

predicted_y = model.predict(x_ols)

# Sort X values so regression line displays correctly
sorted_data = regression_data.copy()
sorted_data["predicted_y"] = predicted_y
sorted_data = sorted_data.sort_values(by=x_variable)

# Add the regression line
plt.plot(
    sorted_data[x_variable],
    sorted_data["predicted_y"],
    color="red",
    label="OLS Regression line"
)

plt.xlabel(x_variable)
plt.ylabel(y_variable)
plt.title(y_variable + " vs " + x_variable + " with OLS Regression Line")
plt.legend()

# Ask if the user wants to save a scatterplot with a regression line
save_regression = input(
    "\nDo you want to save the regression line? (yes/no): "
)

if save_regression.lower() == "yes":
    filename = input("Enter the file name: ")
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    print("Regression lines saved")

plt.show()
