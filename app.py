import streamlit as st
import pickle
import pandas as pd
import requests

# OMDB api key for fetching posters....
OMDB_API_KEY = '28a23645'

def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    data = requests.get(url).json()
    poster_url = data.get('Poster')
    return poster_url

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)  # Create 5 columns for the 5 recommended movies
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(f"<h6 style='text-align: center;'>{name}</h6>", unsafe_allow_html=True)
            if poster:
                st.image(poster, use_column_width=True)
            else:
                st.text("Poster not available")