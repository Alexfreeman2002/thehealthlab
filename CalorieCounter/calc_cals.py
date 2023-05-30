def calculate_calories(protein, fat, carbs):
    #calculates the calorie equivalent for protein, fat and carbohydrates in grams
    p_cals = protein * 4
    f_cals = fat * 9
    carb_cals = carbs * 4

    #calculates the resulting calories
    total_cals = p_cals + f_cals + carb_cals

    return total_cals