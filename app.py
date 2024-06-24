from flask import Flask, render_template, request
import pandas as pd
from main import get_drink_recommendations, sbdrinks_data

app = Flask(__name__)

drinks_aslist = sbdrinks_data['Drink_name'].tolist()

@app.route('/')
def index():
    return render_template('index.html', drinks=drinks_aslist)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_drinks_names = request.form.getlist('selected_drinks')
    include_all = 'include_all' in request.form
    include_coffee = 'include_coffee' in request.form
    include_tea = 'include_tea' in request.form
    include_neither = 'include_neither' in request.form
    include_hot = 'include_hot' in request.form
    include_cold = 'include_cold' in request.form
    include_frozen = 'include_frozen' in request.form
    n_recommendations = int(request.form.get('n_recommendations', 5))

    # Call your recommendation function
    recommendations = get_drink_recommendations(
        selected_drinks_names,
        sbdrinks_data,
        include_all=include_all,
        include_coffee=include_coffee,
        include_tea=include_tea,
        include_neither=include_neither,
        include_hot=include_hot,
        include_cold=include_cold,
        include_frozen=include_frozen,
        n_recommendations=n_recommendations
    )

    # Format recommendations as HTML
    html_output = '<h2>Recommendations:</h2><ul>'
    for index, row in recommendations.iterrows():
        html_output += f'<li>{row["Drink_name"]} (Distance: {row["distance"]:.2f})</li>'
    html_output += '</ul>'
    return html_output

if __name__ == '__main__':
    app.run(debug=True)
