import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from utils import load_ingredients_database, analyze_ingredients

# Set up the Streamlit page configuration
st.set_page_config(page_title="Ingredients Scanner", layout="wide")

# Custom CSS for a better design
st.markdown("""
    <style>
        /* Add custom background with leaves */
        .main {
            background-image: url('C:\\Users\\dell\\Downloads\\cdfc82c1-dbc1-46d5-8cab-fc302dfc82af.jpg');  /* Add your background leaf image URL */
            background-size: cover;
            background-repeat: no-repeat;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        /* Title and styling */
        .title {
            color: #2C3E50;
            font-family: 'Pacifico', cursive;
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            text-decoration: underline;
            text-decoration-color: #8BC34A;
            position: relative;
            z-index: 2;
        }

        /* Button styling */
        .button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 12px 20px;
            border-radius: 10px;
            cursor: pointer;
        }

        .button:hover {
            background-color: #45a049;
        }

        /* Section header styling */
        .section-header {
            font-family: 'Arial', sans-serif;
            color: #34495e;
            font-size: 26px;
            font-weight: bold;
        }

        /* Footer styling */
        .footer {
            font-size: 14px;
            text-align: center;
            color: #95a5a6;
        }

        /* Ingredient details styling */
        .ingredient-details {
            font-size: 16px;
            font-family: 'Arial', sans-serif;
            color: #2C3E50;
            line-height: 1.5;
            margin-bottom: 20px;
        }

        .ingredient-header {
            font-weight: bold;
            font-size: 18px;
            color: #2C3E50;
        }

        /* Safety level color coding */
        .safety-safe {
            color: green;
            font-weight: bold;
        }

        .safety-moderate {
            color: orange;
            font-weight: bold;
        }

        .safety-harmful {
            color: red;
            font-weight: bold;
        }

        /* Input box styling */
        .input-box {
            font-size: 18px;
            font-family: 'Arial', sans-serif;
        }

        /* Progress bar styling */
        .progress-bar {
            width: 100%;
            background-color: #f3f3f3;
        }

        .progress-bar-filled {
            width: 0;
            height: 20px;
            background-color: #4CAF50;
            text-align: center;
            color: white;
            line-height: 20px;
            border-radius: 10px;
        }

        /* Reminder message styling */
        .reminder {
            color: #E67E22;
            font-weight: bold;
            font-size: 18px;
            margin-top: 30px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Header image (optional)
st.image("logo.png", width=150)

# Title
st.markdown('<div class="title">🧴 INGREDIENTS SCANNER </div>', unsafe_allow_html=True)

# Description
st.write("""
    Welcome to the **INGRESCAN**! ✨  
    This tool helps you analyze the safety of ingredients in cosmetic products.  
    Just enter the ingredients (separated by commas) and get detailed safety analysis.
""", unsafe_allow_html=True)

# Input field for ingredients
user_input = st.text_area("Enter ingredients (comma separated)", 
                          "e.g., glycerin, fragrance, parabens", 
                          height=150, 
                          key="ingredients_input", 
                          placeholder="Type the ingredients here...")

# Add a button to trigger analysis
if st.button("Analyze Ingredients", key="analyze", use_container_width=True):
    # Display progress bar while processing
    st.markdown('<div class="progress-bar"><div class="progress-bar-filled">Analyzing...</div></div>', unsafe_allow_html=True)
    
    # Load the ingredient database
    db = load_ingredients_database()

    # Analyze the ingredients entered by the user
    results = analyze_ingredients(user_input, db)

    # Hide the progress bar and display results
    st.markdown('<div class="progress-bar"><div class="progress-bar-filled" style="width: 100%;">Done!</div></div>', unsafe_allow_html=True)

    # Display the results
    st.subheader("🔍 Analysis Result")
    
    safe_count = 0
    moderate_count = 0
    harmful_count = 0
    unknown_count = 0
    results_list = []

    for ingredient, safety, description in results:
        if safety.lower() == "safe":
            safe_count += 1
            rating = 5
        elif safety.lower() == "moderate":
            moderate_count += 1
            rating = 3
        elif safety.lower() == "harmful":
            harmful_count += 1
            rating = 1
        else:
            unknown_count += 1
            rating = 0  # For unknown safety level

        # Safety color coding
        safety_class = "safety-safe" if safety.lower() == "safe" else "safety-moderate" if safety.lower() == "moderate" else "safety-harmful"

        st.markdown(f"""
        <div class="ingredient-details">
        <div class="ingredient-header">{ingredient.title()}</div>
        <div class="{safety_class}">Safety: {safety.capitalize()}</div>
        <div><strong>Details:</strong> {description}</div>
        <div><strong>Rating:</strong> {rating}/5</div>
        </div>
        """, unsafe_allow_html=True)

        results_list.append({
            "ingredient": ingredient.title(),
            "safety": safety.capitalize(),
            "description": description,
            "rating": rating
        })

    # Bar chart of safety levels based on rating
    st.subheader("📊 Ingredient Ratings Based on Safety")

    # Extract ratings and ingredient names for plotting
    ingredients = [result["ingredient"] for result in results_list]
    ratings = [result["rating"] for result in results_list]

    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(ingredients, ratings, color=['#8BC34A' if r == 5 else '#FFC107' if r == 3 else '#F44336' for r in ratings], edgecolor="black")
    
    ax.set_title("Ingredient Ratings (Higher is better)", fontsize=16, fontweight='bold')
    ax.set_xlabel("Rating (out of 5)", fontsize=12)
    ax.set_ylabel("Ingredients", fontsize=12)
    
    # Invert y-axis to display the highest ratings at the top
    ax.invert_yaxis()

    # Display the chart
    st.pyplot(fig)

    # Add a download button for the analysis results (CSV)
    df = pd.DataFrame(results_list)
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Analysis Results (CSV)",
        data=csv,
        file_name="ingredients_analysis.csv",
        mime="text/csv"
    )

    # Conclusion message with dark orange color for reminder
    st.markdown('<div class="reminder">**Reminder**: Always check the ingredients before using a cosmetic product, especially if you have sensitive skin or allergies. Stay safe and informed!</div>', unsafe_allow_html=True)

# Footer with links to social media (optional)
st.markdown("""
    <div class="footer">
    Made with ❤️ by [Your Name](https://www.linkedin.com/in/yourprofile) | Powered by [Streamlit](https://streamlit.io)
    </div>
""", unsafe_allow_html=True)
