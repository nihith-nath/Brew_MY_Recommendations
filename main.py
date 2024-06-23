print("heelo world!!");


#---------------My creation of starbucks drink recommendation system----------------------#


#---------------Importing all necessary libraries ----------------------#


from typing import List
from scipy.spatial import distance
import pandas as pd 
#from pyscript import Element
from scipy.spatial.distance import euclidean



#---------------Initial setup and loading of data ----------------------#

file_path = '/Users/HP/Desktop/Starbucks_rs/starbucks_drinks.csv'
sbdrinks_data = pd.read_csv(file_path)

## i renamed the column coz its doesnt name sense for a cloumn name to be "490"

sbdrinks_data.rename(columns={'490': 'Drink_name'}, inplace=True)

## creating a new column Drink_id  and adding it as first column 

sbdrinks_data['Drink_id'] = range(1, len(sbdrinks_data) + 1)
columns = ['Drink_id'] + sbdrinks_data.columns[:-1].tolist()
sbdrinks_data = sbdrinks_data[columns]
print(sbdrinks_data.dtypes)


#---------------Turning data into float data types ----------------------#

columns_to_convert = sbdrinks_data.columns.difference(['Drink_id', 'Drink_name'])
sbdrinks_data[columns_to_convert] = sbdrinks_data[columns_to_convert].astype(float)

# Print the data types after conversion
print("\nData types after conversion:")
print(sbdrinks_data.dtypes)

# Verify the DataFrame structure
# print("\nDataFrame:")
# print(sbdrinks_data.head())






#---------------Main Logic ----------------------#


def mean_selected_drink(s_drinks):
    mean_vector = s_drinks.drop(columns=['Drink_id', 'Drink_name']).mean().values
    return mean_vector

# Function to find closest drinks based on mean vector
def find_closest_drinks(mean_vector, all_drinks_data, n_recommendations=5):
    # Calculate Euclidean distances
    all_drinks_data['distance'] = all_drinks_data.apply(lambda row: euclidean(mean_vector, row.drop(['Drink_id', 'Drink_name'])), axis=1)
    # Sort drinks by distance and get top recommendations
    closest_drinks = all_drinks_data.sort_values(by='distance').head(n_recommendations)
    return closest_drinks[['Drink_id', 'Drink_name', 'distance']]

# Function to get recommendations based on selected drink names
def get_drink_recommendations(selected_drinks_names, all_drinks_data, include_all=True, include_coffee=True, include_tea=True, include_neither=False, include_hot=True, include_cold=True, include_frozen=True, n_recommendations=5):
    selected_drinks = all_drinks_data[all_drinks_data['Drink_name'].isin(selected_drinks_names)]
    
    if selected_drinks.empty:
        print("No drinks selected")
        return pd.DataFrame(columns=['Drink_id', 'Drink_name', 'distance'])
    
    # Calculating mean vector of selected drinks
    mean_vector = mean_selected_drink(selected_drinks)

    
    #applying Filters on all_drinks_data based on user's preference
    filtered_drinks = pd.DataFrame(columns=all_drinks_data.columns)
    
    for index, row in all_drinks_data.iterrows():
        if include_all:
            filtered_drinks = pd.concat([filtered_drinks, pd.DataFrame([row])], ignore_index=True, sort=False)
        else:
            if include_coffee and row['is_coffee'] == 1:
                filtered_drinks = pd.concat([filtered_drinks, pd.DataFrame([row])], ignore_index=True, sort=False)
            if include_tea and row['is_tea'] == 1:
                filtered_drinks = pd.concat([filtered_drinks, pd.DataFrame([row])], ignore_index=True, sort=False)
            if include_neither and row['is_not_coffee_or_tea'] == 1:
                filtered_drinks = pd.concat([filtered_drinks, pd.DataFrame([row])], ignore_index=True, sort=False)
            if include_hot and row['is_hot'] == 1:
                filtered_drinks = pd.concat([filtered_drinks, pd.DataFrame([row])], ignore_index=True, sort=False)
            if include_cold and row['is_cold'] == 1:
                filtered_drinks = pd.concat([filtered_drinks, pd.DataFrame([row])], ignore_index=True, sort=False)
            if include_frozen and row['is_frozen'] == 1:
                filtered_drinks = pd.concat([filtered_drinks, pd.DataFrame([row])], ignore_index=True, sort=False)
                
    if filtered_drinks.empty:
        print("No drinks matched the filters.")
        return pd.DataFrame(columns=['Drink_id', 'Drink_name', 'distance'])

    recommendations = find_closest_drinks(mean_vector,filtered_drinks, n_recommendations)
    
    return recommendations

# Example usage
selected_drinks_names = ["Americano", "Blended Strawberry Lemonade", "Pink Drink"]
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
print(recommendations)


#--------------- Functions for clearing active_drinks and toggling drinks ----------------------#

 




