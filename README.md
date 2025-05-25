Streamlit-Based Movie Recommendation System
Overview
This project is a content-based movie recommendation system built using Python, Streamlit, and the TMDB 5000 Movie Dataset. It recommends movies similar to a user-selected title by analyzing metadata (genres, cast, keywords, etc.) using TF-IDF vectorization and cosine similarity. The Netflix-style web interface, deployed on Render, includes features like theme toggling, profile-based filtering (Kids/Adult), a watchlist, a random movie picker, trending movies, and a chatbot-like filtering system. The system fetches real-time movie details and posters via the TMDB API.
Developed by Tanish Sharma and Anshu Jain under the supervision of Dr. Rinky Ahuja at Sushant University, May 2025.
Features

Content-Based Recommendations: Suggests 10 movies similar to the user’s selection based on metadata.
Netflix-Style UI: Built with Streamlit, featuring:
Theme toggling (Default, Dark, Light).
Profile filtering: Kids (Animation only, ~312 movies) and Adult (all genres).
Sidebar filters: Genre dropdown and release year slider (1980–2024).
Watchlist: Add/remove movies, rate (0–10), add notes, and export as CSV.
Random Movie Picker: Suggests a movie respecting filters.
Trending Movies: Displays weekly trends from TMDB API in a 5-column grid.
Chatbot-Like Filtering: Filters by genre, cast, or release year in a 3-column grid.


TMDB API Integration: Fetches real-time posters, overviews, ratings, and trailers.
Optimized Performance: Uses sparse matrices to reduce memory usage (~70 MB vs. ~180 MB).
Deployment: Hosted on Render with code on GitHub.

Installation
To run the project locally, follow these steps:

Clone the Repository:
git clone https://github.com/TanishSharma2004/movie-recommendation-system.git
cd movie-recommendation-system


Install Dependencies: Ensure Python 3.9 is installed. Then, install required libraries:
pip install -r requirements.txt


Set Up TMDB API Key:

Obtain an API key from TMDB.
Add it as an environment variable:export TMDB_API_KEY='your-api-key'




Run the Streamlit App:

streamlit run app.py



Requirements:

Python 3.9
Libraries (listed in requirements.txt):
streamlit
pandas
scikit-learn
requests
pickle
scipy


Dataset: TMDB 5000 Movie Dataset (tmdb_5000_movies.csv, tmdb_5000_credits.csv)
Tools: Git, Visual Studio Code or PyCharm, Mermaid Live Editor

Usage

Open the app in your browser (default: http://localhost:8501).
Select a movie from the dropdown to get 10 similar movie recommendations.
Use the sidebar to:
Toggle themes (Default, Dark, Light).
Choose a profile (Kids or Adult).
Filter by genre or release year.


Add movies to the watchlist, rate them, and add notes. Export as CSV.
Use the random movie picker or chatbot popup to filter by genre, cast, or year.
View trending movies with posters and trailers fetched from the TMDB API.

Technical Details
Data Preprocessing

Dataset: TMDB 5000 Movie Dataset (4803 movies).
Steps:
Merged tmdb_5000_movies.csv and tmdb_5000_credits.csv on title.
Resolved 5 duplicates and 12 missing entries.
Extracted genres, top 3 cast, director, keywords, and overview into a tags column.
Saved as movie_data.pkl (~2.5 MB).



Model Building

TF-IDF Vectorization: Converted tags into a sparse matrix (~4803 × 20,000 features) using scikit-learn.
Cosine Similarity: Computed a 4803 × 4803 matrix using sklearn.metrics.pairwise.cosine_similarity.
Optimization: Used scipy.sparse.csr_matrix to reduce memory from ~180 MB to ~70 MB.
Recommendation Function: Returns top 10 similar movies, with Kids mode filtering Animation.

Streamlit App

UI Components:
Custom CSS for Netflix-style look (e.g., #e50914 buttons, hover effects).
TMDB API integration with caching (@st.cache_data).


Deployment:
Hosted on Render with GitHub integration.
Configured with requirements.txt and streamlit run app.py --server.port $PORT.



Implementation Challenges

API Rate Limits: TMDB’s 40 requests/10s limit handled with caching and retry logic.
Session State: Fixed Streamlit UI reruns using explicit st.session_state initialization.
CSS Conflicts: Overrode Streamlit’s default styles with targeted selectors and !important.
File Size: Reduced movie_data.pkl from 186.31 MB to ~70 MB to meet GitHub’s 100 MB limit.

Experimental Results

Recommendation Accuracy:
Tested with movies like Harry Potter (8/10 recommendations from the same franchise or fantasy genre) and The Dark Knight.
Kids mode correctly showed Animation films like Toy Story.


Performance:
Initial app load: ~3s.
Recommendation generation: ~1s.
Memory savings: 61% with sparse matrix.
Stable for ~50 concurrent users on Render.


UI Feedback: Rated 4.5/5 by three test users, suggesting faster API responses and larger posters.
Limitations: Accuracy depends on metadata quality; sparse overviews may reduce similarity scores.

Future Scope

Add collaborative filtering for hybrid recommendations.
Expand to books, songs, or TV shows.
Implement a conversational chatbot with NLP for natural language queries.
Add user authentication for personalized watchlists.
Enhance scalability with cloud-based vector storage.
Track user interactions for analytics.
Optimize UI for mobile devices.

Repository Structure
movie-recommendation-system/
├── app.py                    # Streamlit app
├── movie_data.pkl            # Preprocessed dataset and cosine similarity matrix
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── assets/                   # Flow charts, architecture diagrams, screenshots

Screenshots


Main Interface: Movie selection and recommendations.
Watchlist: Rated movies with notes.
Chatbot Popup: Filtering by genre (e.g., Action).

Contributing
Contributions are welcome for academic or research purposes. Please open a GitHub issue to report bugs or suggest improvements, or submit a pull request with detailed descriptions of changes.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Status
This repository is maintained for academic purposes and was completed as part of a B.Tech CSE (AI&ML) project in May 2025. For contributions or issues, please open a GitHub issue.
References

Ricci, F., et al., Recommender Systems Handbook, Springer, 2011.
Pazzani, M. J., Billsus, D., Content-Based Recommendation Systems, Springer, 2007.
Lops, P., et al., Content-based Recommender Systems, Springer, 2011.
Koren, Y., et al., Matrix Factorization Techniques, IEEE, 2009.
TMDB 5000 Movie Dataset
Streamlit Documentation
TMDB API
GitHub Documentation
Render Documentation

Acknowledgments
![Screenshot 2025-05-25 184853](https://github.com/user-attachments/assets/f2bf859f-755b-4236-b3c8-365657636fdb)
![Screenshot 2025-05-25 184359](https://github.com/user-attachments/assets/3d410b49-bc6f-427d-86d5-9a02b8a8ccac)
![Screenshot 2025-05-25 184105](https://github.com/user-attachments/assets/95008b24-b061-45d8-b803-07a148018fad)

Dr. Rinky Ahuja for guidance.
TMDB for providing the dataset and API.
Streamlit and Render for enabling easy development and deployment.
