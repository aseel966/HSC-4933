#########################################################
# Kaplan Meier Log rate and Cox PH tests                #
# ----------------------------------------------------- #
# Aseel S Ali # HSC4933.005 # 11/1/26                   #
# This script uses two heart failure dataset to perform #
# a Keplan Meier log rate test and a Cox proportional   #
# hazards regression. It compares hospital readmission  #
# between treatment groups and examines factors related #
#########################################################

import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test

# Part 1: Kaplan-meter log-rate test

# Load the log-rank dataset
km_data = pd.read_csv("../km_logrank_readmission.csv")

# Display the columns and data types
print("Log-Rank Dataset:")
print(km_data.head())
print(km_data.dtypes)

# Remove rows with missing required values
km_data = km_data.dropna(
    subset=["treatment_group", "time_days", "readmitted", "sex"]
)
# Clean treatment group names
km_data["treatment_group"] = km_data["treatment_group"].str.strip()

# Separate the two treatment groups
standard = km_data[
    km_data["treatment_group"].str.contains("Standard", case=False, na=False)
]
telehealth =km_data[
    km_data["treatment_group"].str.contains("TeleHealth", case=False, na=False)
]

# Check group sizes
print("\nStandard care patients:", len(standard))
print("\nTelehealth patients:", len(telehealth))

# Perform the log-rate test
logrank_results = logrank_test(
    standard["time_days"],
    telehealth["time_days"],
    event_observed_A=standard["readmitted"],
    event_observed_B=telehealth["readmitted"],
)
print("\nLog-Rank Test: Treatment Groups")
print(logrank_results.summary)

# Perform another log-rank tests comparing sex
male = km_data[km_data["sex"] =="Male"]
female = km_data[km_data["sex"] =="Female"]
sex_results = logrank_test(
    male["time_days"],
    female["time_days"],
    event_observed_A=male["readmitted"],
    event_observed_B=female["readmitted"],
)
print("\nLog-Rank Test: Male vs Female")
print(sex_results.summary)

# Create the Kaplan-Meier figure
kmf = KaplanMeierFitter()
plt.figure(figsize=(9,6))
kmf.fit(
    standard["time_days"],
    event_observed=standard["readmitted"],
    label="standard care",
)
kmf.plot_survival_function(ci_show=True)
kmf.fit(
    telehealth["time_days"],
    event_observed=telehealth["readmitted"],
    label="telehealth follow-up",
)
kmf.plot_survival_function(ci_show=True)

plt.title("Kaplan Meier: time to hospital readmission")
plt.xlabel("Time after discharge (days)")
plt.ylabel("Probability of no Readmission")
plt.xlim(0,180)
plt.ylim(0,1)
plt.grid(True)
plt.tight_layout()

# Save and display the figure
plt.savefig("kaplan_meier_logrank.png", dpi=300)
plt.show()

# Part 2: Cox Proportional Hazards Regression

# Load the cox proportional hazards dataset
cox_data = pd.read_csv("cox_ph_heart_failure_survival.csv")

# Display the columns and dataset
print("\nCox Proportional Hazard Dataset:")
print(cox_data.head())
print(cox_data.dtypes)

# Convert sex into a numeric variable
# Male = 1 and Female = 0
cox_data["sex"] = cox_data["sex"].map({
    "Male": 1,
    "Female": 0
})

# Select the required variables
cox_columns = [
    "time_months",
    "death",
    "age",
    "sex",
    "bmi",
    "systolic_bp",
    "ejection_fraction",
    "diabetes",
    "smoker",
    "chronic_kidney_disease",
    "nyha_class",
    "beta_blocker"
]

# Remove missing values
cox_data = cox_data[cox_columns].dropna()

# Create and fit the Cox model
cox_model = CoxPHFitter()

cox_model.fit(
    cox_data,
    duration_col="time_months",
    event_col="death",
)

# Display the Cox model results
print("\nCox Proportional Hazard Results:")
cox_model.print_summary()

# Create the Cox proportional hazards figure
plt.figure(figsize=(10,7))

cox_model.plot(hazard_ratios=True)

plt.title("Cox Proportional Hazard: Heart Failure Survival")
plt.xlabel("Hazard Ratio")
plt.grid(True)
plt.tight_layout()

# Save and display the figures
plt.savefig("cox_proportional_hazard.png", dpi=300)
plt.show()

print("\nAnalysis completed successfully")
print("Both figures have been saved")
