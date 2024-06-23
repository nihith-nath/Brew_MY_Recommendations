from flask import Flask, render_template, request, jsonify
import pandas as pd
from main import get_drink_recommendations, sbdrinks_data

app = Flask(__name__)

# Load Starbucks drinks data
file_path = '/Users/HP/Desktop/Starbucks_rs/starbucks_drinks.csv'
sbdrinks_data = pd.read_csv(file_path)

# Rename and add Drink_id column as needed
sbdrinks_data.rename(columns={'490': 'Drink_name'}, inplace=True)
sbdrinks_data['Drink_id'] = range(1, len(sbdrinks_data) + 1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_drinks_names = request.form.getlist('selected_drinks')
    # Call your recommendation function
    recommendations = get_drink_recommendations(
        selected_drinks_names,
        sbdrinks_data,
        include_all=False,
        include_coffee=True,
        include_tea=False,
        include_neither=False,
        include_hot=False,
        include_cold=True,
        include_frozen=True,
        n_recommendations=5
    )
    # Format recommendations as HTML
    html_output = '<h2>Recommendations:</h2><ul>'
    for index, row in recommendations.iterrows():
        html_output += f'<li>{row["Drink_name"]} (Distance: {row["distance"]:.2f})</li>'
    html_output += '</ul>'
    return html_output

if __name__ == '__main__':
    app.run(debug=True)
