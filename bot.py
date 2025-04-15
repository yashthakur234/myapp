import streamlit as st
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(layout="wide")

# Load data and models
df = pd.read_csv("objects/final_data.csv")
vectorizer = joblib.load("objects/tfidf_vectorizer.pkl")
tfidf_matrix = joblib.load("objects/tfidf_matrix.pkl")
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Load custom CSS
with open("styles/style.css", "r") as f:
    st.markdown(f"<style>{f.read()} </style>", unsafe_allow_html=True)

def get_score_color(score):
    colors = {
        0.9: "#FF6B6B",
        0.8: "#4ECDC4",
        0.7: "#45B7D1",
        0.6: "#96C93D",
        0.5: "#DAA520",
    }
    for threshold, color in colors.items():
        if score >= threshold:
            return color
    return "#DAA520"

def display_movie_grid(movies_df):
    if not movies_df.empty:
        cols = st.columns(4)
        for idx, (_, row) in enumerate(movies_df.iterrows()):
            col_idx = idx % 4
            score = row["similarity_score"]
            score_color = get_score_color(score)

            with cols[col_idx]:
                st.markdown(
                    f"""
                    <div class="movie-card">
                        <div class="movie-title">{row['Title']}</div>
                        <div class="movie-details">
                            <div><strong>Director:</strong> {row['Director']}</div>
                            <div><strong>Year:</strong> {int(row['Release Year'])}</div>
                            <div><strong>Genre:</strong> {row['Genre']}</div>
                            <div><strong>Rating:</strong> {row['Rating']}/10</div>
                            <div class="movie-summary"><strong>Summary:</strong> {row['Summary']}</div>
                        </div>
                        <div class="movie-score">
                            Similarity Score
                            <div class="score-bar">
                                <div class="score-fill" 
                                     style="width: {score * 100}%; background: {score_color};">
                                </div>
                            </div>
                            <div style="text-align: right; color: {score_color};">
                                {score:.0%}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

def get_recommendations(title):
    idx = df.index[df["Title"] == title].tolist()[0]
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:11]
    movie_indices = [i[0] for i in sim_scores]
    similarity_values = [i[1] for i in sim_scores]
    result_df = pd.DataFrame({
        "Title": df["Title"].iloc[movie_indices].values,
        "Director": df["Director"].iloc[movie_indices].values,
        "Release Year": df["Release Year"].iloc[movie_indices].values,
        "Genre": df["Main Genres"].iloc[movie_indices].values,
        "Rating": df["Rating (Out of 10)"].iloc[movie_indices].values,
        "Summary": df["Summary"].iloc[movie_indices].values,
        "similarity_score": similarity_values,
    })
    return result_df

def main():
    st.title("What to watch")
    st.caption("Your movie recommendation friend")

    all_movies = df["Title"].unique()
    selected_movie = st.selectbox("Select a movie you like", options=all_movies, placeholder="Choose a movie...")
    st.markdown("</div>", unsafe_allow_html=True)

    if selected_movie:
        recommendations_df = get_recommendations(selected_movie)
        st.markdown(
            f"""
            <div class="recommendation-header">
                Because you like "<span class="like">{selected_movie}</span>", we think you'll enjoy these movies:
            </div>
            """, 
            unsafe_allow_html=True
        )
        display_movie_grid(recommendations_df)

if __name__ == "__main__":
    main()