#  Movie Recommendation System (Hybrid: Content + Collaborative)

## Demo

[Click here to watch the demo video](https://drive.google.com/file/d/1BfIsC60jOq1tUTi3FPx01rw1rq-kRD6l/view?usp=sharing)

This project is a movie recommender system that suggests movies based on both:
- **What the movie is about** (using text-based content)
- **What users with similar preferences liked** (using user ratings)

It uses TMDB and MovieLens data to deliver more accurate and personalized movie recommendations. The system is built with Python and has a web interface using Streamlit.

---

##  Features

- Content-based filtering using movie overview, genres, cast, keywords, and director
- Collaborative filtering using user ratings (SVD model from Surprise)
- Hybrid recommendation that combines both approaches
- Poster fetching from OMDb API
- Clean and simple web interface using Streamlit
- Takes user input (movie + user ID) and returns 5 recommended movies

---



