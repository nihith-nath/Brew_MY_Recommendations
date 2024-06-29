from flask import Flask, render_template, request
import pandas as pd
from main import get_drink_recommendations, sbdrinks_data

app = Flask(__name__)

# Assuming sbdrinks_data is loaded or imported correctly
drinks_aslist = sbdrinks_data['Drink_name'].tolist()

@app.route('/')
def index():
    return render_template('index.html', drinks=drinks_aslist)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_drinks_names = request.form.getlist('selected_drinks')

    include_all = request.form.get('include_all') == '1'
    include_coffee = request.form.get('include_coffee') == '1'
    include_tea = request.form.get('include_tea') == '1'
    include_neither = request.form.get('include_neither') == '1'
    include_hot = request.form.get('include_hot') == '1'
    include_cold = request.form.get('include_cold') == '1'
    include_frozen = request.form.get('include_frozen') == '1'
    n_recommendations = int(request.form.get('n_recommendations', 5))

    print("Selected Drinks:", selected_drinks_names)
    print("Include All:", include_all)
    print("Include Coffee:", include_coffee)
    print("Include Tea:", include_tea)
    print("Include Neither:", include_neither)
    print("Include Hot:", include_hot)
    print("Include Cold:", include_cold)
    print("Include Frozen:", include_frozen)
    print("Number of Recommendations:", n_recommendations)

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
    html_output = '<div id="recommendations">'
    html_output += '<h3>Your Top Recommendations:</h3>'
    html_output += '<ul>'
    for index, row in recommendations.iterrows():
        html_output += f'<li>{row["Drink_name"]} (Distance: {row["distance"]:.2f})</li>'
    html_output += '</ul>'
    html_output += '</div>'

    return html_output

if __name__ == '__main__':
    app.run(debug=True)