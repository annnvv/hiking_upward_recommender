import streamlit as st
import pandas as pd

st.set_page_config(title="Hiking Upward Recommender", layout="wide")

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

    hike_df = pd.read_csv("app/data/hiking_upward_data.csv")

    recommend_df = pd.read_csv("app/data/nearest_25_recommendations_for_each_hike.csv")

    one_hike = hike_df[hike_df.hike_url == url]
    st.text("Input Hike Information")
    st.write(one_hike)

    recommend_df_subset = recommend_df[recommend_df.hike_url == url].head(num_recommend)

    recommend_df_subset.drop("hike_url", axis=1, inplace=True)

    merged = pd.merge(
        recommend_df_subset, hike_df, left_on="similar", right_on="hike_url", how="left"
    )

    merged.drop(["similar", "score"], axis=1, inplace=True)

    st.text("Recommended Hike Information")
    st.dataframe(merged)

