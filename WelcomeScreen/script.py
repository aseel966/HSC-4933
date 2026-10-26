###########################################
# Lab 8 - Logistic and Poisson Regression #
# Aseel Ali - HSC 4933 - 10/25/2026       #
###########################################

import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import classification_report, confusion_matrix
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Ask the user for a dataset and load it
filename = input("Enter the dataset file name: ")
df = pd.read_csv(filename)

# Clean column names using IC#4 method
df.columns = df.columns.str.lower().str.replace(" ", "_")

# List all available columns
print("\nAvailable columns:")
print(df.columns.tolist())

# Ask for multiple predictors and one response variable
predictors = input("Enter predictors columns separated by commas: ")
predictors = predictors.replace(" ", "").lower().split(",")

response = input("Enter the response column: ")
response = response.strip().lower()

# Ask the user which regression to perform
print("\n1. Logistic Regression:")
print("2. Poisson Regression")
choice = input("Enter 1 or 2: ")

# Remove rows missing values when in selected columns
df = df.dropna(subset=predictors + [response])

# Select predictors and response
X = df[predictors]
x = X.apply(pd.to_numeric, errors="coerce")
y = df[response]
y = pd.to_numeric(y, errors="coerce")

valid_rows = X.notna().all(axis=1) & y.notna()
X = X.loc[valid_rows]
y = y.loc[valid_rows]
# Add a constant for regression
X = sm.add_constant(X)

# Logistic regression
if choice == "1":

    # Logistic regression requires values of 0 and 1
    if not y.isin([0, 1]).all():
        raise ValueError("Response must contain only 0 and 1.")

    model = sm.Logit(y, X).fit()

    # Predict values of 0 or 1
    prediction = model.predict(X)
    predictions = (prediction > 0.5).astype(int)

    # Calculate accuracy
    accuracy = (predictions == y).mean()

    # Create regression output
    output = str(model.summary())
    output += "\n\nAccuracy: " + str(accuracy)
    output += "\n\nClassification Report:\n"
    output += classification_report(y, predictions)
    output += "\nConfusion Matrix:\n"
    output += str(confusion_matrix(y, predictions))

# Poisson regression
elif choice == "2":

    # Poisson regression is intended for count variables
    if (y < 0).any():
        raise ValueError("Response must not contain negative values.")
    if (y % 1 != 0).any():
        print("Warning: The response contains decimals, not counts")

     # Calculate Poisson regression
    model = sm.GLM(y, X, family=sm.families.Poisson()).fit()

     # Calculate VIF for each predictor
    vif = pd.DataFrame()
    vif["Predictor"] = predictors
    vif["VIF"] = [
     variance_inflation_factor(X.values, i + 1)
     for i in range(len(predictors))
     ]

     # Calculate pseudo-R squared
    null_model = sm.GLM(
        y, X[["const"]], family=sm.families.Poisson()).fit()
    pseudo_r2 = 1 - model.llf / null_model.llf

    # Create regression output
    output = str(model.summary())
    output += "\n\nPseudo-R²: " + str(pseudo_r2)
    output += "\n\nVIF Results:\n"
    output += vif.to_string(index=False)

# Print the regression results
print("\n", output)

# Ask whether to save results
save = input("\nWould you like to save the result? (yes/no): ")

if save.lower() == "yes":
    output_name = input("Enter a filename ending in .txt: ")

    with open(output_name, "w") as file:
        file.write(output)

    print("Output saved as:", output_name)
