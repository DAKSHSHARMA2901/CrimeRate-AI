from flask import Flask, request, render_template, jsonify
import pickle
import math
import os
import pandas as pd

app = Flask(__name__)

# -------------------------------
# Load the dataset
# -------------------------------
def load_crime_data():
    try:
        df = pd.read_excel('Dataset/new_dataset.xlsx', sheet_name='Sheet1')
        print("Dataset loaded successfully. First 5 records:")
        print(df.head())
        return df
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        return None

crime_df = load_crime_data()

# -------------------------------
# Generate mappings from dataset
# -------------------------------
def create_mappings():
    cities = sorted(crime_df['City'].unique())
    crimes = sorted(crime_df['Type'].unique())

    city_names = {str(i): city for i, city in enumerate(cities)}
    crimes_names = {str(i): crime for i, crime in enumerate(crimes)}

    latest_year = crime_df['Year'].max()
    pop_data = crime_df[crime_df['Year'] == latest_year][['City', 'Population (in Lakhs) (2011)+']]
    population = pop_data.set_index('City')['Population (in Lakhs) (2011)+'].to_dict()
    population_codes = {str(i): population[city] for i, city in enumerate(cities)}

    return city_names, crimes_names, population_codes

if crime_df is not None:
    city_names, crimes_names, population = create_mappings()
else:
    raise RuntimeError("Failed to load dataset. Please check file path/content.")

# -------------------------------
# Load ML model
# -------------------------------
model_path = 'Model/model.pkl'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found at {model_path}")

with open(model_path, 'rb') as file:
    model = pickle.load(file)

# -------------------------------
# Home route
# -------------------------------
@app.route('/')
def index():
    return render_template("index.html", cities=city_names, crimes=crimes_names)

# -------------------------------
# Predict crime rate
# -------------------------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        city_code = data['city']
        crime_code = data['crime']
        year = int(data['year'])

        if city_code not in city_names or crime_code not in crimes_names:
            return jsonify({"error": "Invalid city or crime type", "success": False}), 400

        city_name = city_names[city_code]
        crime_type = crimes_names[crime_code]
        pop = float(population[city_code])

        # Check if data is available for the given year
        year_data = crime_df[(crime_df['City'] == city_name) & 
                             (crime_df['Year'] == year) & 
                             (crime_df['Type'] == crime_type)]

        if not year_data.empty:
            pop = year_data['Population (in Lakhs) (2011)+'].values[0]
            crime_rate = year_data['Crime Rate'].values[0]
        else:
            base_year = crime_df['Year'].min()
            pop *= (1.01 ** (year - base_year))
            crime_rate = model.predict([[year, int(city_code), pop, int(crime_code)]])[0]

        # Classify crime status
        if crime_rate <= 1:
            crime_status = "Very Low Crime Area"
        elif crime_rate <= 5:
            crime_status = "Low Crime Area"
        elif crime_rate <= 15:
            crime_status = "High Crime Area"
        else:
            crime_status = "Very High Crime Area"

        cases = math.ceil(crime_rate * pop)

        return jsonify({
            'city_name': city_name,
            'crime_type': crime_type,
            'year': year,
            'crime_status': crime_status,
            'crime_rate': round(crime_rate, 2),
            'cases': cases,
            'population': round(pop, 2),
            'success': True
        })

    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

# -------------------------------
# Compare two cities
# -------------------------------
@app.route('/compare', methods=['POST'])
def compare():
    try:
        data = request.get_json()
        city1 = data['city1']
        city2 = data['city2']
        crime_code = data['crime']
        year = int(data['year'])

        if city1 not in city_names or city2 not in city_names or crime_code not in crimes_names:
            return jsonify({"error": "Invalid input", "success": False}), 400

        def get_prediction(city_code):
            city_name = city_names[city_code]
            pop = float(population[city_code])
            crime_type = crimes_names[crime_code]

            year_data = crime_df[(crime_df['City'] == city_name) & 
                                 (crime_df['Year'] == year) & 
                                 (crime_df['Type'] == crime_type)]

            if not year_data.empty:
                pop = year_data['Population (in Lakhs) (2011)+'].values[0]
                crime_rate = year_data['Crime Rate'].values[0]
            else:
                base_year = crime_df['Year'].min()
                pop *= (1.01 ** (year - base_year))
                crime_rate = model.predict([[year, int(city_code), pop, int(crime_code)]])[0]

            return {
                "name": city_name,
                "crime_rate": round(crime_rate, 2),
                "safety_index": round(100 - crime_rate, 2),
                "population": round(pop, 2)
            }

        city1_data = get_prediction(city1)
        city2_data = get_prediction(city2)

        return jsonify({
            "city1": city1_data,
            "city2": city2_data,
            "crime_type": crimes_names[crime_code],
            "year": year,
            "success": True
        })

    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

# -------------------------------
# About Page
# -------------------------------
@app.route('/about')
def about():
    return render_template("about.html")

# -------------------------------
# Dataset Page
# -------------------------------
@app.route('/dataset')
def show_dataset():
    if crime_df is None:
        return jsonify({"error": "Dataset not loaded", "success": False}), 500

    return render_template("dataset.html", 
                           tables=[crime_df.head(50).to_html(classes='data')], 
                           titles=crime_df.columns.values)

# -------------------------------
# Main runner
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
