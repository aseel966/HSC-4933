#############################################
# function_practice_1.py # aseelali18@usf.edu
#############################################
# (c) Aseel,Ali 2026 #HSC4933 #Week 2, Wed #
# A practice script missing a function to  #
# calculate BMI from input                 #
############################################

# First, lets make a variable called height_m that is a floating-point number
# and let it be assigned a value according to a user input:

height_m = float(input("Please enter your height in metres: "))

# Now, lets define another floating-point variables called weight_kg that is
# a;so assigned a value according to user input:

weight_kg = float(input("Please enter your weight in kg: "))

# Now, in the space below this line bt before line 25, lets make a function to
# calculate bmi according to the formula BMI = weight_kg / (height in m)^2 and
# return the result as a floating number:

def calculate_bmi (height_m ,  weight_kg):
    """
    Calculates the BMI based on the height and weight in metres

    :param height_m: Height in metres
    :param weight_kg: Weight in kg
    :return: BMI
    """
    BMI=(weight_kg/height_m **2)
    return BMI

def categorize_bmi(bmi):
    """
    Calculates the BMI based on the height and weight in metres

    :param bmi:
    :return:
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi <25:
        return "Normal"
    elif bmi <30:
        return "Overweight"
    elif bmi <=30:
        return "Obese"
    else:
        return "ERROR"

# With our function written, now we can call it and set the BMI value equal to the output:

BMI=calculate_bmi(height_m,weight_kg)
category = categorize_bmi(BMI)

# Now that we have a variable called BMI, lets print out the BMI calculation statement
# with the value rounded to 2 decimal places:
print(f"Your BMI is {BMI:.2f}")
print(f"Your category is {category}")






































