import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from geopy.distance import geodesic
from fuzzywuzzy import process

# Load data
data = pd.read_csv('data/data.csv')

# Preprocessing
data['Coordinate'] = data['Coordinate'].apply(eval)
data['Lat'] = data['Coordinate'].apply(lambda x: x['lat'])
data['Long'] = data['Coordinate'].apply(lambda x: x['lng'])

# Helper function to compute cosine similarity between descriptions
def compute_cosine_similarity(descriptions):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

# Helper function to find the closest matching place name
def find_closest_place_name(place_name, place_names):
    place_name = place_name.lower()
    match = process.extractOne(place_name, place_names)
    return match[0] if match[1] >= 80 else None

# Function to recommend based on place name
def recommend_by_place_name(place_name, data=data, start=0, end=5):
    place_names = data['Place_Name'].str.lower().tolist()
    closest_place_name = find_closest_place_name(place_name, place_names)

    if closest_place_name is None:
        return []

    place_data = data[data['Place_Name'].str.lower() == closest_place_name].iloc[0]
    place_index = data.index[data['Place_Name'].str.lower() == closest_place_name][0]
    descriptions = data['Description'].tolist()
    cosine_sim = compute_cosine_similarity(descriptions)

    data['Distance'] = data.apply(lambda row: geodesic((place_data['Lat'], place_data['Long']), (row['Lat'], row['Long'])).kilometers, axis=1)
    data['Similarity'] = cosine_sim[place_index]
    data['Category_Similarity'] = data['Category'].apply(lambda x: 1 if x == place_data['Category'] else 0)
    
    recommendations = data[(data['Place_Name'].str.lower() != closest_place_name) & (data['Category_Similarity'] == 1)]
    recommendations = recommendations.sort_values(by=['Similarity', 'Rating', 'Distance'], ascending=[False, False, True])
    
    paginated_recommendations = recommendations[start:end].to_dict('records')
    
    return paginated_recommendations

if __name__ == '__main__':
    place_name = 'kota tua'
    start = 0
    end = 5

    for place in recommend_by_place_name(place_name, start=start, end=end):
        print(place)
        print()