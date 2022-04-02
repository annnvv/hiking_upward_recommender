import streamlit as st
import pandas as pd
import numpy as np

st.title("Hiking Upward Recommender")

st.header("Input")
try:
    url = st.text_input("Hiking Upward Hike URL")
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

