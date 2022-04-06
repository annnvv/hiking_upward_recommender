from numpy import float16
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hiking Upward Recommender", layout="wide")

st.title("Hiking Upward Recommender")

st.header("Input")
st.write(
    "Please visit [Hiking Upward](https://www.hikingupward.com/maps/) to choose a hike and enter the URL below to see similar hikes."
)

try:
    url = st.text_input("Hiking Upward Hike URL", max_chars=75)  # max len of URL is 72
except ValueError:
    print("URL must start with https://www.hikingupward.com/")

num_recommend = st.radio("Choose the number of recommendations", (5, 10, 15))

st.header("Output")
if url:

    hike_df = pd.read_csv(
        "app/data/hiking_upward_data.csv",
        dtype={
            "hike_url": str,
            "hike_name": str,
            "park_abbreviation": str,
            "hike_len_in_mi": float16,
            "difficulty_rating": int,
            "streams_rating	views_rating": int,
            "solitude_rating": int,
            "camping_rating": int,
            "hiking_duration_str": str,
            "elevation_gain_ft": float16,
        },
    )

    recommend_df = pd.read_csv("app/data/nearest_15_recommendations_for_each_hike.csv")

    one_hike = hike_df[hike_df.hike_url == url].reset_index(drop=True)
    st.text("Input Hike Information")
    st.write(one_hike)

    recommend_df_subset = recommend_df[recommend_df.hike_url == url].head(num_recommend)

    recommend_df_subset.drop("hike_url", axis=1, inplace=True)

    merged = pd.merge(
        recommend_df_subset, hike_df, left_on="similar", right_on="hike_url", how="left"
    )

    merged.drop(["similar", "score"], axis=1, inplace=True)

    st.text("Recommended Hike Information")

    # CSS to inject contained in a string
    hide_dataframe_row_index = """
                <style>
                .row_heading.level0 {display:none}
                .blank {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

    st.dataframe(merged)

with st.expander("Methodology Note"):
    st.markdown(
        "The recommender system calculates the cosine similarity between the hike and all other hikes. \
        In calculating the cosine similarity, it takes into account hike length (in miles), difficulty, streams, views, solitude, and camping ratings \
        (a rating has a scale from zero to six, higher values indicate more difficulty, better views, more streams, etc.). \
        A future iteration will take into account hike duration and elevation gain. \
        Then, the top 5, 10, or 15 most similar hikes are returned."
    )
