import streamlit as st
import requests
import pickle
import pandas as pd
import random
import uuid
import logging

# --- Setup Logging ---
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# --- Set page config ---
st.set_page_config(page_title="🎬 Netflix-style Movie Recommender", layout="wide")

# --- Initialize Session State ---
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'show_watchlist' not in st.session_state:
    st.session_state.show_watchlist = False
if 'show_chatbot' not in st.session_state:
    st.session_state.show_chatbot = True
if 'profile_mode' not in st.session_state:
    st.session_state.profile_mode = "Adult"
if 'chatbot_option' not in st.session_state:
    st.session_state.chatbot_option = "None"

# --- Sidebar Theme Toggle ---
theme = st.sidebar.radio("🌓 Choose Theme", ("Default Theme", "Dark Mode", "Light Mode"))

# --- Apply CSS Based on Theme ---
if theme == "Default Theme":
    background_color = "#141414"  # Fallback
    text_color = "white"
    sidebar_bg_color = "#2a2a2a"
    sidebar_text_color = "white"
    chatbot_bg_color = "rgba(42, 42, 42, 0.7)"  # Semi-transparent
elif theme == "Dark Mode":
    background_color = "#141414"
    text_color = "white"
    sidebar_bg_color = "#1c1c1c"
    sidebar_text_color = "white"
    chatbot_bg_color = "rgba(28, 28, 28, 0.7)"  # Semi-transparent
else:  # Light Mode
    background_color = "#f5f5f5"
    text_color = "black"
    sidebar_bg_color = "#e0e0e0"
    sidebar_text_color = "black"
    chatbot_bg_color = "rgba(224, 224, 224, 0.7)"  # Semi-transparent

# --- Inject Custom CSS ---
background_style = (
    f"""
    background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
    url('https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/f562aaf4-5dbb-4603-a32b-6ef6c2230136/dh0w8qv-9d8ee6b2-b41a-4681-ab9b-8a227560dc75.jpg/v1/fill/w_1280,h_720,q_75,strp/the_netflix_login_background_canada2024__by_logofever_dh0w8qv-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NzIwIiwicGF0aCI6IlwvZlwvZjU2MmFhZjQtNWRiYi00NjAzLWEzMmItNmVmNmMyMjMwMTM2XC9kaDB3OHF2LTlkOGVlNmIyLWI0MWEtNDY4MS1hYjliLThhMjI3NTYwZGM3NS5qcGciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.LOYKSxIDqfPwWHR0SSJ-ugGQ6bECF0yO6Cmc0F26CQs');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    """
    if theme == "Default Theme"
    else f"background-color: {background_color};"
)

st.markdown(
    f"""
    <style>
    header[data-testid="stHeader"] {{
        display: none;
    }}
    .stApp {{
        {background_style}
        color: {text_color};
        min-height: 100vh;
        margin: 0;
        padding: 0;
        top: 0;
        left: 0;
    }}
    .stApp::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: {'rgba(0, 0, 0, 0.4)' if theme == "Default Theme" else 'none'};
        z-index: -1;
    }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg_color};
        color: {sidebar_text_color};
    }}
    [data-testid="stSidebar"] * {{
        color: {sidebar_text_color};
    }}
    h1 {{
        color: {text_color};
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        font-size: 50px !important;
        padding-bottom: 20px;
        background: none;
        margin-top: -40px !important;
        padding-top: 0px;
        text-align: center;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }}
    h2, h3, h4, h5, h6, .stMarkdown, .stText {{
        color: {text_color};
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
    }}
    div[data-testid="stSelectbox"] label {{
        color: #ffffff !important;
        font-size: 22px !important;
    }}
    [data-testid="stSelectbox"] .stSelectbox div[role="combobox"] {{
        color: black !important;
    }}
    [data-testid="stSelectbox"] option {{
        color: black !important;
    }}
    [data-testid="stSelectbox"] .stSelectbox div[data-baseweb="select"] > div {{
        color: black !important;
    }}
    [data-testid="stRadio"] > div:first-child > label {{
        font-size: 26px !important;
        color: {sidebar_text_color} !important;
    }}
    [data-testid="stRadio"] div[role="radiogroup"] label {{
        font-size: 16px !important;
        color: {sidebar_text_color} !important;
    }}
    .stRadio > div > label {{
        font-size: 26px !important;
        color: {sidebar_text_color} !important;
    }}
    img:hover {{
        filter: brightness(1.2) drop-shadow(0 0 10px #e50914);
        transition: 0.3s ease;
    }}
    .stButton>button {{
        background-color: #e50914;
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: #f40612;
        transform: scale(1.05);
        box-shadow: 0 0 15px {text_color};
    }}
    .chatbot-popup {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 350px;
        background: {chatbot_bg_color};
        border: 2px solid #e50914;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
        z-index: 1000;
        color: {text_color};
    }}
    .chatbot-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }}
    .chatbot-option {{
        background-color: #e50914;
        color: white;
        border-radius: 10px;
        padding: 8px;
        margin: 5px 0;
        text-align: center;
    }}
    .chatbot-option:hover {{
        background-color: #f40612;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Load dataset ---
try:
    logger.debug("Loading movie_data.pkl")
    with open('movie_data.pkl', 'rb') as file:
        movies, cosine_sim = pickle.load(file)
    required_columns = ['title', 'movie_id', 'genres', 'release_year']
    if not all(col in movies.columns for col in required_columns):
        st.error(f"Dataset missing required columns: {', '.join(set(required_columns) - set(movies.columns))}")
        logger.error(f"Missing columns: {set(required_columns) - set(movies.columns)}")
        st.stop()
    logger.debug(f"Dataset loaded successfully. Shape: {movies.shape}")
except FileNotFoundError:
    st.error("Error: movie_data.pkl not found. Please ensure the file is in the correct directory.")
    logger.error("movie_data.pkl not found")
    st.stop()
except Exception as e:
    st.error(f"Error loading dataset: {str(e)}")
    logger.error(f"Dataset loading failed: {str(e)}")
    st.stop()

# --- Functions ---
def get_recommendations(title, cosine_sim=cosine_sim):
    try:
        if st.session_state.profile_mode == "Kids":
            animation_movies = movies[movies['genres'].str.contains("Animation", case=False, na=False)]
            if animation_movies.empty:
                st.warning("No Animation movies found in the dataset.")
                logger.warning("No Animation movies in dataset")
                return pd.DataFrame()
            idx = movies[movies['title'] == title].index[0]
            sim_scores = list(enumerate(cosine_sim[idx]))
            animation_indices = animation_movies.index
            sim_scores = [score for score in sim_scores if score[0] in animation_indices]
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:10]
            movie_indices = [i[0] for i in sim_scores]
            recommendations = movies.iloc[movie_indices]
            if len(recommendations) < 10:
                st.warning(f"Only {len(recommendations)} Animation movies available for recommendation.")
            logger.debug(f"Kids recommendations for {title}: {len(recommendations)} movies")
            return recommendations
        else:
            idx = movies[movies['title'] == title].index[0]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
            movie_indices = [i[0] for i in sim_scores]
            recommendations = movies.iloc[movie_indices]
            logger.debug(f"Adult recommendations for {title}: {len(recommendations)} movies")
            return recommendations
    except (IndexError, KeyError) as e:
        logger.error(f"Recommendation error for {title}: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def fetch_movie_details(movie_id):
    try:
        api_key = '5c35b598fd61fbe662ae2f088ac68559'
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch details for movie_id {movie_id}: {str(e)}")
        return None

def fetch_trending_movies():
    try:
        api_key = '5c35b598fd61fbe662ae2f088ac68559'
        url = f'https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()['results']
    except requests.RequestException as e:
        logger.error(f"Failed to fetch trending movies: {str(e)}")
        return []

@st.cache_data
def fetch_movie_credits(movie_id):
    try:
        api_key = '5c35b598fd61fbe662ae2f088ac68559'
        url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json().get('cast', [])[:3]
    except requests.RequestException as e:
        logger.error(f"Failed to fetch credits for movie_id {movie_id}: {str(e)}")
        return []

@st.cache_data
def fetch_movie_trailer(movie_id):
    try:
        api_key = '5c35b598fd61fbe662ae2f088ac68559'
        url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        videos = response.json().get('results', [])
        for video in videos:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                return f"https://www.youtube.com/watch?v={video['key']}"
        return None
    except requests.RequestException as e:
        logger.error(f"Failed to fetch trailer for movie_id {movie_id}: {str(e)}")
        return None

# --- App Layout ---
logger.debug("Rendering app layout")
st.title('🎬 Your Next Binge!')

# 2. Trending Now Section
st.subheader('🔥 Trending Now')
trending = fetch_trending_movies()
if trending:
    trend_cols = st.columns(5)
    for idx, movie in enumerate(trending[:5]):
        with trend_cols[idx]:
            poster_path = movie.get('poster_path')
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
            title = movie.get('title', 'Unknown Title')
            overview = movie.get('overview', 'No overview available.')
            imdb_id = movie.get('imdb_id')
            imdb_url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "https://www.imdb.com/"
            st.image(poster_url, use_container_width=True)
            st.markdown(f"<p><strong>{title}</strong></p>", unsafe_allow_html=True)
            with st.expander(f"More about {title}"):
                st.write(f"Overview: {overview}")
                st.markdown(f"[👉 Visit IMDb Page]({imdb_url})", unsafe_allow_html=True)
                trailer_url = fetch_movie_trailer(movie.get('id'))
                if trailer_url:
                    st.markdown(f"[🎥 Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                else:
                    st.write("No trailer available.")
else:
    st.warning("Unable to fetch trending movies.")

st.markdown("---")

# 3. Random Movie Button
if st.button("🎲 Pick a Random Movie", key="random_movie"):
    filtered_movies = movies.copy()
    if st.session_state.profile_mode == "Kids":
        filtered_movies = filtered_movies[filtered_movies['genres'].str.contains("Animation", case=False, na=False)]
    if not filtered_movies.empty:
        random_movie = filtered_movies.sample(1).iloc[0]
        st.subheader(f"🎬 Random Pick: {random_movie['title']}")
        details = fetch_movie_details(random_movie['movie_id'])
        poster_url = (f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}"
                      if details and details.get('poster_path')
                      else "https://via.placeholder.com/500x750?text=No+Image")
        st.image(poster_url, use_container_width=True)
        st.markdown(f"<p><strong>{random_movie['title']}</strong></p>", unsafe_allow_html=True)
        with st.expander(f"More about {random_movie['title']}"):
            overview = details.get('overview', 'No overview available.') if details else 'No overview available.'
            release_date = details.get('release_date', 'Unknown') if details else 'Unknown'
            rating = details.get('vote_average', 'N/A') if details else 'N/A'
            runtime = details.get('runtime', 'N/A') if details else 'N/A'
            genres = ', '.join([g['name'] for g in details.get('genres', [])]) if details else 'N/A'
            imdb_id = details.get('imdb_id') if details else None
            imdb_url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "#"
            st.write(f"Overview: {overview}")
            st.write(f"Release Date: {release_date}")
            st.write(f"Rating: ⭐ {rating}")
            st.write(f"Runtime: {runtime} min")
            st.write(f"Genres: {genres}")
            st.markdown(f"[👉 IMDb Page]({imdb_url})", unsafe_allow_html=True)
            trailer_url = fetch_movie_trailer(random_movie['movie_id'])
            if trailer_url:
                st.markdown(f"[🎥 Watch Trailer]({trailer_url})", unsafe_allow_html=True)
            else:
                st.write("No trailer available.")
        if st.button(f"➕ Add to Watchlist", key=f"add_random_{random_movie['movie_id']}"):
            st.session_state.watchlist.append({
                'title': random_movie['title'],
                'poster_url': poster_url
            })
            st.success(f"✅ {random_movie['title']} added to your Watchlist!")
    else:
        st.warning("No movies available for random selection.")

st.markdown("---")

# 4. Sidebar Filters
st.sidebar.header('👤 Profile')
profile_mode = st.sidebar.radio("Select Profile:", ["Kids", "Adult"], index=0 if st.session_state.profile_mode == "Kids" else 1)
st.session_state.profile_mode = profile_mode

st.sidebar.header('🎯 Filters')
genres_available = ['All'] + sorted(list(set(genre for sublist in movies['genres'].str.split() for genre in sublist)))
selected_genre = st.sidebar.selectbox('Select Genre', genres_available)
selected_year = st.sidebar.slider('Select Release Year', 1980, 2024, (2000, 2024))

# Watchlist Toggle Button
if st.sidebar.button("🎯 Your Perfect Watchlist", key="watchlist_toggle"):
    st.session_state.show_watchlist = not st.session_state.show_watchlist

# 5. Movie Selection and Recommendations
filtered_movies = movies.copy()
if st.session_state.profile_mode == "Kids":
    filtered_movies = filtered_movies[filtered_movies['genres'].str.contains("Animation", case=False, na=False)]
if selected_genre != 'All':
    filtered_movies = filtered_movies[filtered_movies['genres'].str.contains(selected_genre, case=False, na=False)]
filtered_movies = filtered_movies[
    (filtered_movies['release_year'] >= selected_year[0]) &
    (filtered_movies['release_year'] <= selected_year[1])
]

# Default recommendations for Kids profile
if st.session_state.profile_mode == "Kids":
    st.subheader("🎬 Recommended Kids Movies")
    kids_movies = filtered_movies.sort_values(by='release_year', ascending=False).head(6)
    if not kids_movies.empty:
        cols = st.columns(3)
        for idx, movie in enumerate(kids_movies.iterrows()):
            movie_title = movie[1]['title']
            movie_id = movie[1]['movie_id']
            details = fetch_movie_details(movie_id)
            with cols[idx % 3]:
                poster_url = (f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}"
                              if details and details.get('poster_path')
                              else "https://via.placeholder.com/500x750?text=No+Image")
                st.image(poster_url, use_container_width=True)
                st.markdown(f"<p><strong>{movie_title}</strong></p>", unsafe_allow_html=True)
                st.markdown(f"<p>Genres: {movie[1]['genres']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p>Release Year: {movie[1]['release_year']}</p>", unsafe_allow_html=True)
                with st.expander(f"More about {movie_title}"):
                    overview = details.get('overview', 'No overview available.') if details else 'No overview available.'
                    release_date = details.get('release_date', 'Unknown') if details else 'Unknown'
                    rating = details.get('vote_average', 'N/A') if details else 'N/A'
                    runtime = details.get('runtime', 'N/A') if details else 'N/A'
                    genres = ', '.join([g['name'] for g in details.get('genres', [])]) if details else movie[1]['genres']
                    imdb_id = details.get('imdb_id') if details else None
                    imdb_url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "#"
                    st.write(f"Overview: {overview}")
                    st.write(f"Release Date: {release_date}")
                    st.write(f"Rating: ⭐ {rating}")
                    st.write(f"Runtime: {runtime} min")
                    st.write(f"Genres: {genres}")
                    st.markdown(f"[👉 IMDb Page]({imdb_url})", unsafe_allow_html=True)
                    trailer_url = fetch_movie_trailer(movie_id)
                    if trailer_url:
                        st.markdown(f"[🎥 Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                    else:
                        st.write("No trailer available.")
                if st.button(f"➕ Add to Watchlist", key=f"add_kids_{movie_id}_{idx}"):
                    st.session_state.watchlist.append({
                        'title': movie_title,
                        'poster_url': poster_url
                    })
                    st.success(f"✅ {movie_title} added to your Watchlist!")
    else:
        st.warning("No Animation movies available for recommendation.")

# Default recommendations for Adult profile
if st.session_state.profile_mode == "Adult":
    st.subheader("🎬 Recommended Adult Movies")
    adult_movies = filtered_movies.sort_values(by='release_year', ascending=False).head(6)
    if not adult_movies.empty:
        cols = st.columns(3)
        for idx, movie in enumerate(adult_movies.iterrows()):
            movie_title = movie[1]['title']
            movie_id = movie[1]['movie_id']
            details = fetch_movie_details(movie_id)
            with cols[idx % 3]:
                poster_url = (f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}"
                              if details and details.get('poster_path')
                              else "https://via.placeholder.com/500x750?text=No+Image")
                st.image(poster_url, use_container_width=True)
                st.markdown(f"<p><strong>{movie_title}</strong></p>", unsafe_allow_html=True)
                st.markdown(f"<p>Genres: {movie[1]['genres']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p>Release Year: {movie[1]['release_year']}</p>", unsafe_allow_html=True)
                with st.expander(f"More about {movie_title}"):
                    overview = details.get('overview', 'No overview available.') if details else 'No overview available.'
                    release_date = details.get('release_date', 'Unknown') if details else 'Unknown'
                    rating = details.get('vote_average', 'N/A') if details else 'N/A'
                    runtime = details.get('runtime', 'N/A') if details else 'N/A'
                    genres = ', '.join([g['name'] for g in details.get('genres', [])]) if details else movie[1]['genres']
                    imdb_id = details.get('imdb_id') if details else None
                    imdb_url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "#"
                    st.write(f"Overview: {overview}")
                    st.write(f"Release Date: {release_date}")
                    st.write(f"Rating: ⭐ {rating}")
                    st.write(f"Runtime: {runtime} min")
                    st.write(f"Genres: {genres}")
                    st.markdown(f"[👉 IMDb Page]({imdb_url})", unsafe_allow_html=True)
                    trailer_url = fetch_movie_trailer(movie_id)
                    if trailer_url:
                        st.markdown(f"[🎥 Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                    else:
                        st.write("No trailer available.")
                if st.button(f"➕ Add to Watchlist", key=f"add_adult_{movie_id}_{idx}"):
                    st.session_state.watchlist.append({
                        'title': movie_title,
                        'poster_url': poster_url
                    })
                    st.success(f"✅ {movie_title} added to your Watchlist!")
    else:
        st.warning("No movies available for recommendation.")

# Movie selection for manual recommendations
selected_movie = st.selectbox('🎥 Select a Movie:', filtered_movies['title'].values if not filtered_movies.empty else ["No movies available"])

if st.button('Recommend Similar Movies', key="recommend_button"):
    with st.spinner('🍿 Finding the best movies for you...'):
        if selected_movie != "No movies available":
            recommendations = get_recommendations(selected_movie)
            if not recommendations.empty:
                st.subheader("🎬 Recommended Movies")
                cols = st.columns(3)
                for idx, movie in enumerate(recommendations.iterrows()):
                    movie_title = movie[1]['title']
                    movie_id = movie[1]['movie_id']
                    details = fetch_movie_details(movie_id)
                    if details:
                        poster_path = details.get('poster_path')
                        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
                        overview = details.get('overview', 'No overview available.')
                        release_date = details.get('release_date', 'Unknown')
                        rating = details.get('vote_average', 'N/A')
                        runtime = details.get('runtime', 'N/A')
                        genres = ', '.join([g['name'] for g in details.get('genres', [])]) if details else movie[1]['genres']
                        imdb_id = details.get('imdb_id')
                        imdb_url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "#"
                        with cols[idx % 3]:
                            st.image(poster_url, use_container_width=True)
                            st.markdown(f"<p><strong>{movie_title}</strong></p>", unsafe_allow_html=True)
                            st.markdown(f"<p>Genres: {genres}</p>", unsafe_allow_html=True)
                            st.markdown(f"<p>Runtime: {runtime} min</p>", unsafe_allow_html=True)
                            with st.expander(f"More about {movie_title}"):
                                st.write(f"Overview: {overview}")
                                st.write(f"Release Date: {release_date}")
                                st.write(f"Rating: ⭐ {rating}")
                                st.write(f"Genres: {genres}")
                                st.markdown(f"[👉 IMDb Page]({imdb_url})", unsafe_allow_html=True)
                                trailer_url = fetch_movie_trailer(movie_id)
                                if trailer_url:
                                    st.markdown(f"[🎥 Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                                else:
                                    st.write("No trailer available.")
                            if st.button(f"➕ Add to Watchlist", key=f"add_recommend_{movie_id}{idx}{uuid.uuid4()}"):
                                st.session_state.watchlist.append({
                                    'title': movie_title,
                                    'poster_url': poster_url
                                })
                                st.success(f"✅ {movie_title} added to your Watchlist!")
            else:
                st.warning("No recommendations found for the selected movie.")
        else:
            st.warning("Please select a valid movie.")

st.markdown("---")

# 6. Display Watchlist if Toggled
if st.session_state.show_watchlist:
    st.subheader('👀 Your Perfect Watchlist:')
    if st.session_state.watchlist:
        if st.button("🗑 Clear Watchlist", key="clear_watchlist"):
            st.session_state.watchlist = []
            st.rerun()
        watch_cols = st.columns(4)
        for idx, item in enumerate(st.session_state.watchlist):
            with watch_cols[idx % 4]:
                st.image(item['poster_url'], use_container_width=True)
                st.markdown(f"<p><strong>{item['title']}</strong></p>", unsafe_allow_html=True)
                st.slider(f"Rate {item['title']}", 0, 10, key=f"rate_{idx}")
                st.text_input(f"Note for {item['title']}", key=f"note_{idx}")
                if st.button("🗑 Remove", key=f"remove_watchlist_{idx}"):
                    st.session_state.watchlist.pop(idx)
                    st.rerun()
        if st.button("📥 Download Watchlist as CSV", key="download_watchlist"):
            df_watchlist = pd.DataFrame(st.session_state.watchlist)
            st.download_button("Download CSV", data=df_watchlist.to_csv(index=False), file_name="watchlist.csv", key="download_csv")
    else:
        st.info("Your watchlist is currently empty. Add some favorites to get started! 🎬")

st.markdown("---")

# 7. Chatbot Popup with Heading
st.subheader("🎬 Watch by Your Preference")
if st.session_state.show_chatbot:
    with st.container():
        st.markdown(
            f"""
            <div class='chatbot-popup'>
                <div class='chatbot-header'>
                    <h3>Let me help you out :)</h3>
                </div>
                <p>🎥 Scroll down to get the perfect movie for you ✨</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🎭 Genres", key="chatbot_genres"):
                st.session_state.chatbot_option = "Genres"
        with col2:
            if st.button("🎬 Cast", key="chatbot_cast_btn"):
                st.session_state.chatbot_option = "Cast"
        with col3:
            if st.button("📅 Year", key="chatbot_year"):
                st.session_state.chatbot_option = "Year"
        with col4:
            if st.button("🔄 Reset", key="chatbot_reset"):
                st.session_state.chatbot_option = "None"

        if st.session_state.chatbot_option == "Genres":
            genres_available = sorted(list(set(genre for sublist in movies['genres'].str.split() for genre in sublist)))
            selected_chatbot_genre = st.selectbox("Select a genre:", ["Choose a genre"] + genres_available, key="chatbot_genre")
            if selected_chatbot_genre != "Choose a genre":
                matched_movies = movies[movies['genres'].str.contains(selected_chatbot_genre, case=False, na=False)]
                if not matched_movies.empty:
                    st.subheader(f"🎬 Movies in {selected_chatbot_genre}")
                    cols = st.columns(3)
                    for idx, movie in matched_movies.head(6).iterrows():
                        movie_title = movie['title']
                        movie_id = movie['movie_id']
                        details = fetch_movie_details(movie_id)
                        with cols[idx % 3]:
                            poster_url = (f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}"
                                         if details and details.get('poster_path')
                                         else "https://via.placeholder.com/500x750?text=No+Image")
                            st.image(poster_url, use_container_width=True)
                            st.markdown(f"<p><strong>{movie_title}</strong></p>", unsafe_allow_html=True)
                            st.markdown(f"<p>Genres: {movie['genres']}</p>", unsafe_allow_html=True)
                            st.markdown(f"<p>Release Year: {movie['release_year']}</p>", unsafe_allow_html=True)
                            with st.expander(f"More about {movie_title}"):
                                overview = details.get('overview', 'No overview available.') if details else 'No overview available.'
                                release_date = details.get('release_date', 'Unknown') if details else 'Unknown'
                                rating = details.get('vote_average', 'N/A') if details else 'N/A'
                                runtime = details.get('runtime', 'N/A') if details else 'N/A'
                                genres = ', '.join([g['name'] for g in details.get('genres', [])]) if details else movie['genres']
                                imdb_id = details.get('imdb_id') if details else None
                                imdb_url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "#"
                                st.write(f"Overview: {overview}")
                                st.write(f"Release Date: {release_date}")
                                st.write(f"Rating: ⭐ {rating}")
                                st.write(f"Runtime: {runtime} min")
                                st.write(f"Genres: {genres}")
                                st.markdown(f"[👉 IMDb Page]({imdb_url})", unsafe_allow_html=True)
                                trailer_url = fetch_movie_trailer(movie_id)
                                if trailer_url:
                                    st.markdown(f"[🎥 Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                                else:
                                    st.write("No trailer available.")
                            if st.button(f"➕ Add to Watchlist", key=f"add_chatbot_genre_{movie_id}_{idx}"):
                                st.session_state.watchlist.append({
                                    'title': movie_title,
                                    'poster_url': poster_url
                                })
                                st.success(f"✅ {movie_title} added to your Watchlist!")
                else:
                    st.warning(f"No movies found for genre: {selected_chatbot_genre}")
        elif st.session_state.chatbot_option == "Cast":
            selected_cast = st.text_input("Enter an actor/actress name:", placeholder="e.g., Tom Hanks", key="chatbot_cast")
            if selected_cast:
                with st.spinner("Searching for movies..."):
                    matched_movies = pd.DataFrame()
                    for _, movie in movies.iterrows():
                        credits = fetch_movie_credits(movie['movie_id'])
                        cast_names = [cast['name'] for cast in credits]
                        if any(selected_cast.lower() in name.lower() for name in cast_names):
                            matched_movies = pd.concat([matched_movies, movie.to_frame().T], ignore_index=True)
                    if not matched_movies.empty:
                        st.subheader(f"🎬 Movies with {selected_cast}")
                        cols = st.columns(3)
                        for idx, movie in matched_movies.head(6).iterrows():
                            movie_title = movie['title']
                            movie_id = movie['movie_id']
                            details = fetch_movie_details(movie_id)
                            with cols[idx % 3]:
                                poster_url = (f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}"
                                             if details and details.get('poster_path')
                                             else "https://via.placeholder.com/500x750?text=No+Image")
                                st.image(poster_url, use_container_width=True)
                                st.markdown(f"<p><strong>{movie_title}</strong></p>", unsafe_allow_html=True)
                                st.markdown(f"<p>Genres: {movie['genres']}</p>", unsafe_allow_html=True)
                                st.markdown(f"<p>Release Year: {movie['release_year']}</p>", unsafe_allow_html=True)
                                with st.expander(f"More about {movie_title}"):
                                    overview = details.get('overview', 'No overview available.') if details else 'No overview available.'
                                    release_date = details.get('release_date', 'Unknown') if details else 'Unknown'
                                    rating = details.get('vote_average', 'N/A') if details else 'N/A'
                                    runtime = details.get('runtime', 'N/A') if details else 'N/A'
                                    genres = ', '.join([g['name'] for g in details.get('genres', [])]) if details else movie['genres']
                                    imdb_id = details.get('imdb_id') if details else None
                                    imdb_url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "#"
                                    st.write(f"Overview: {overview}")
                                    st.write(f"Release Date: {release_date}")
                                    st.write(f"Rating: ⭐ {rating}")
                                    st.write(f"Runtime: {runtime} min")
                                    st.write(f"Genres: {genres}")
                                    st.markdown(f"[👉 IMDb Page]({imdb_url})", unsafe_allow_html=True)
                                    trailer_url = fetch_movie_trailer(movie_id)
                                    if trailer_url:
                                        st.markdown(f"[🎥 Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                                    else:
                                        st.write("No trailer available.")
                                if st.button(f"➕ Add to Watchlist", key=f"add_chatbot_cast_{movie_id}_{idx}"):
                                    st.session_state.watchlist.append({
                                        'title': movie_title,
                                        'poster_url': poster_url
                                    })
                                    st.success(f"✅ {movie_title} added to your Watchlist!")
                    else:
                        st.warning(f"No movies found with cast: {selected_cast}")
        elif st.session_state.chatbot_option == "Year":
            year_range = sorted(movies['release_year'].dropna().astype(int).unique())
            selected_year = st.selectbox("Select a release year:", ["Choose a year"] + list(map(str, year_range)), key="chatbot_year_select")
            if selected_year != "Choose a year":
                matched_movies = movies[movies['release_year'] == int(selected_year)]
                if not matched_movies.empty:
                    st.subheader(f"🎬 Movies from {selected_year}")
                    cols = st.columns(3)
                    for idx, movie in matched_movies.head(6).iterrows():
                        movie_title = movie['title']
                        movie_id = movie['movie_id']
                        details = fetch_movie_details(movie_id)
                        with cols[idx % 3]:
                            poster_url = (f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}"
                                         if details and details.get('poster_path')
                                         else "https://via.placeholder.com/500x750?text=No+Image")
                            st.image(poster_url, use_container_width=True)
                            st.markdown(f"<p><strong>{movie_title}</strong></p>", unsafe_allow_html=True)
                            st.markdown(f"<p>Genres: {movie['genres']}</p>", unsafe_allow_html=True)
                            st.markdown(f"<p>Release Year: {movie['release_year']}</p>", unsafe_allow_html=True)
                            with st.expander(f"More about {movie_title}"):
                                overview = details.get('overview', 'No overview available.') if details else 'No overview available.'
                                release_date = details.get('release_date', 'Unknown') if details else 'Unknown'
                                rating = details.get('vote_average', 'N/A') if details else 'N/A'
                                runtime = details.get('runtime', 'N/A') if details else 'N/A'
                                genres = ', '.join([g['name'] for g in details.get('genres', [])]) if details else movie['genres']
                                imdb_id = details.get('imdb_id') if details else None
                                imdb_url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "#"
                                st.write(f"Overview: {overview}")
                                st.write(f"Release Date: {release_date}")
                                st.write(f"Rating: ⭐ {rating}")
                                st.write(f"Runtime: {runtime} min")
                                st.write(f"Genres: {genres}")
                                st.markdown(f"[👉 IMDb Page]({imdb_url})", unsafe_allow_html=True)
                                trailer_url = fetch_movie_trailer(movie_id)
                                if trailer_url:
                                    st.markdown(f"[🎥 Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                                else:
                                    st.write("No trailer available.")
                            if st.button(f"➕ Add to Watchlist", key=f"add_chatbot_year_{movie_id}_{idx}"):
                                st.session_state.watchlist.append({
                                    'title': movie_title,
                                    'poster_url': poster_url
                                })
                                st.success(f"✅ {movie_title} added to your Watchlist!")
                else:
                    st.warning(f"No movies found for year: {selected_year}")
