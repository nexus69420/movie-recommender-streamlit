import pickle
import streamlit as st
import pandas as pd
import requests


OMDB_API_KEY = "56d47059"


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

svd = pickle.load(open('svd_model.pkl', 'rb'))


def fetch_poster(movie_title):
    try:
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['Response'] == 'True':
            return data.get('Poster', "https://via.placeholder.com/300x450?text=No+Poster")
        else:
            return "https://via.placeholder.com/300x450?text=Not+Found"
    except Exception as e:
        print(f"Error fetching poster for '{movie_title}': {e}")
        return "https://via.placeholder.com/300x450?text=Error"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters

def hybrid_recommend(user_id, movie_title, top_n=5):
    try:
        movie_index = movies[movies['title'] == movie_title].index[0]
    except IndexError:
        return [], []

    content_scores = list(enumerate(similarity[movie_index]))
    content_scores = sorted(content_scores, key=lambda x: x[1], reverse=True)[1:21]

    recommended_movies = []
    recommended_posters = []

    for i in content_scores:
        tmdb_id = movies.iloc[i[0]]['id']
        try:
            rating_pred = svd.predict(user_id, tmdb_id).est
        except:
            rating_pred = 0
        title = movies.iloc[i[0]]['title']
        recommended_movies.append((title, rating_pred))

    recommended_movies = sorted(recommended_movies, key=lambda x: x[1], reverse=True)[:top_n]

    for movie in recommended_movies:
        title = movie[0]
        recommended_posters.append(fetch_poster(title))

    return [m[0] for m in recommended_movies], recommended_posters


st.title('Movie Recommendation System')
selected_movie_name = st.selectbox('Select a movie to get similar recommendations:', movies['title'].values)
user_id = st.number_input('Enter your user ID (e.g. 1–600)', min_value=1, max_value=100000, value=1)






if st.button('Show Recommendation'):
    names, posters = hybrid_recommend(user_id, selected_movie_name)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])

