import pandas as pd

def load_ingredients_database():
    # Load ingredients from the CSV file (ingredients_db.csv)
    try:
        df = pd.read_csv('ingredients_db.csv')  # Reading the updated CSV file name
        return df
    except FileNotFoundError:
        print("Error: ingredients_db.csv not found!")
        return pd.DataFrame(columns=["ingredient", "safety", "description"])  # Return an empty DataFrame if file is not found

def analyze_ingredients(user_input, db):
    # Split the user input by commas and clean the list
    input_ingredients = [i.strip().lower() for i in user_input.split(",")]
    results = []

    # Loop through the input ingredients and match them with the database
    for ingredient in input_ingredients:
        match = db[db["ingredient"].str.lower() == ingredient]  # Check if the ingredient exists in the CSV data
        if not match.empty:
            row = match.iloc[0]  # If found, get the first matching row
            results.append((ingredient, row["safety"], row["description"]))
        else:
            results.append((ingredient, "Unknown", "Not found in database"))
    return results

def compare_ingredients(input_ingredients, db):
    # Function to compare ingredients and return a DataFrame of results
    results_list = []

    # Loop through the input ingredients and match them with the database
    for ingredient in input_ingredients:
        match = db[db["ingredient"].str.lower() == ingredient]  # Check if the ingredient exists in the CSV data
        if not match.empty:
            row = match.iloc[0]  # If found, get the first matching row
            results_list.append({
                "ingredient": ingredient.title(),
                "safety": row["safety"].capitalize(),
                "description": row["description"],
                "rating": safety_rating(row["safety"])
            })
        else:
            results_list.append({
                "ingredient": ingredient.title(),
                "safety": "Unknown",
                "description": "Not found in database",
                "rating": 0
            })
    
    # Convert the results into a DataFrame for easy display and further analysis
    results_df = pd.DataFrame(results_list)
    return results_df

def safety_rating(safety):
    # Assign a numeric rating based on safety level
    safety = safety.lower()
    if safety == "safe":
        return 5
    elif safety == "moderate":
        return 3
    elif safety == "harmful":
        return 1
    else:
        return 0  # For "unknown" safety level

