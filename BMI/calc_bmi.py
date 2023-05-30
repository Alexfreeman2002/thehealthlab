import math as m

def height_m(Height, choice):
    #makes their input uppercase
    choice = choice.upper()
    if choice == "CM":
        #returns height in meters
        return Height/100
    elif choice == "FEET":
        #returns height in meters
        return Height/3.281


def weight_kg(Weight, choice):
    choice = choice.upper()
    if choice == "KG":
        # returns weight in kilograms
        return Weight
    elif choice == "LBS":
        # returns weight in kilograms
        return Weight/2.205


def bmi_calc(H, W, h_choice, w_choice):
    #gets the weight and height in kg and meters
    weight = weight_kg(W, w_choice)
    height = height_m(H, h_choice)
    #squares the height for the bmi calculation
    sq_height = m.pow(height,2)
    bmi = weight/sq_height
    #returns the bmi rounded to 2 decimal places
    return round(bmi,2)