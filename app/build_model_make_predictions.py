from pandas import DataFrame, concat 
from numpy import nan
from requests import get
from bs4 import BeautifulSoup
import pandera as pa
from typing import List
from sklearn.preprocessing import StandardScaler
import turicreate as tc

parks_abbr = [
    "GWNF",
    "GSMNP",
    "JNF",
    "MNF",
    "NNF",
    "PNF",
    "SNP",
    "WMNF",
    "UNF",
    "OMH",
    "NCSP",
    "OPH",
    "OVH",
    "OWVH",
]

# states = ['MD', 'VA', 'WV', 'NC', 'PA', 'NH']

## define pandera schema
schema = pa.DataFrameSchema(
    {
        "hike_name": pa.column(str, nullable=False),
        "hike_url": pa.Column(
            str,
            pa.Check.str_startswith("https://www.hikingupward.com/"),
            nullable=False,
        ),
        "park_abbreviation": pa.column(str, pa.Check.isin(parks_abbr), vnullable=False),
        # "state": pa.column(str, pa.Check.isin(states), nullable = False),
        "hike_len_in_mi": pa.Column(int, nullable=False),
        "difficulty_rating": pa.Column(
            int,
            pa.Check.in_range(0, 6, include_min=True, include_max=True),
            nullable=False,
        ),
        "streams_rating": pa.Column(
            int,
            pa.Check.in_range(0, 6, include_min=True, include_max=True),
            nullable=False,
        ),
        "views_rating": pa.Column(
            int,
            pa.Check.in_range(0, 6, include_min=True, include_max=True),
            nullable=False,
        ),
        "solitude_rating": pa.Column(
            int,
            pa.Check.in_range(0, 6, include_min=True, include_max=True),
            nullable=False,
        ),
        "camping_rating": pa.Column(
            int,
            pa.Check.in_range(0, 6, include_min=True, include_max=True),
            nullable=False,
        ),
        "hiking_duration": pa.Column(str),  ##will change to int in the future
        "elevation_gain_ft": pa.Column(str),  ##will change to in in the future
    }
)


def get_rating(table):
    """Return an array of numeric ratings from an html table"""

    try:
        hike_len_in_mi = float(table[0].text.replace("mls", "").strip())
    except:
        hike_len_in_mi = nan

    try:
        difficulty_rating = int(
            table[1]
            .find("img")
            .get("src")
            .replace("../../images/stars/Star", "")
            .replace("/images/stars/Star", "")
            .replace("_clear.gif", "")
            .replace("_grey.gif", "")
            .replace("_red.gif", "")
        )
    except:
        difficulty_rating = nan

    try:
        streams_rating = int(
            table[2]
            .find("img")
            .get("src")
            .replace("../../images/stars/Star", "")
            .replace("/images/stars/Star", "")
            .replace("_clear.gif", "")
            .replace("_grey.gif", "")
            .replace("_red.gif", "")
        )
    except:
        streams_rating = nan

    try:
        views_rating = int(
            table[3]
            .find("img")
            .get("src")
            .replace("../../images/stars/Star", "")
            .replace("/images/stars/Star", "")
            .replace("_clear.gif", "")
            .replace("_grey.gif", "")
            .replace("_red.gif", "")
        )
    except:
        views_rating = nan

    try:
        solitude_rating = int(
            table[4]
            .find("img")
            .get("src")
            .replace("../../images/stars/Star", "")
            .replace("/images/stars/Star", "")
            .replace("_clear.gif", "")
            .replace("_grey.gif", "")
            .replace("_red.gif", "")
        )
    except:
        solitude_rating = nan

    try:
        camping_rating = int(
            table[5]
            .find("img")
            .get("src")
            .replace("../../images/stars/Star", "")
            .replace("/images/stars/Star", "")
            .replace("_clear.gif", "")
            .replace("_grey.gif", "")
            .replace("_red.gif", "")
        )
    except:
        camping_rating = nan

    return (
        hike_len_in_mi,
        difficulty_rating,
        streams_rating,
        views_rating,
        solitude_rating,
        camping_rating,
    )


def get_duration_and_elevation(table):
    """"Return an array of duration and elevation gain from an html table"""
    try:
        hiking_duration = str(table.contents[0].text.strip()) #av.note: want this to be numeric
    except:
        hiking_duration = ""

    try:
        elevation_gain_ft = str(
            table.contents[2]
            .text.strip()
            .replace("ft", "")
            .replace(",", "")
            .replace("with three different ascents", "")
            .replace("with multiple ascents", "")
            .replace("with two ascents", "")
            .replace("with two different ascents", "")
            .strip()
        ) #av.note: want this to be numeric
    except:
        elevation_gain_ft = ""

    return hiking_duration, elevation_gain_ft


def get_duration_and_elevation2(table):
    """"Return an array of duration and elevation gain from an html table.
    This function is necessary because this data lives in a different part of the table"""

    try:
        hiking_duration = str(table.contents[2].text.strip())
    except:
        hiking_duration = ""

    try:
        elevation_gain_ft = str(
            table.contents[4]
            .text.strip()
            .replace("ft", "")
            .replace(",", "")
            .replace("with three different ascents", "")
            .replace("with multiple ascents", "")
            .replace("with two ascents", "")
            .replace("with two different ascents", "")
            .strip()
        )
    except:
        elevation_gain_ft = ""

    return hiking_duration, elevation_gain_ft


def get_one_hike_data(hiking_upward_url: str) -> DataFrame:
    """Return a dataframe with data for one hike"""

    hike_content = get(hiking_upward_url)
    if hike_content.status_code == 200:
        try:
            hike_soup = BeautifulSoup(hike_content.text, "html.parser")
            tables = hike_soup.find("table", {"class": "hike_pages"})

            if len(tables.find_all("tr")) < 7:
                rating_table = tables.find_all("tr")[1].find_all("td")
                (
                    hike_len_in_mi,
                    difficulty_rating,
                    streams_rating,
                    views_rating,
                    solitude_rating,
                    camping_rating,
                ) = get_rating(rating_table)

                time_elev = tables.find_all("tr")[2].find_all("td")[1]
                hiking_duration, elevation_gain_ft = get_duration_and_elevation(
                    time_elev
                )

                df = DataFrame(
                    {
                        "hike_name": str(hike_soup.title.text),
                        "park_abbreviation": hiking_upward_url.replace(
                            "https://www.hikingupward.com/", ""
                        ).split("/", 1)[0],
                        "hike_url": str(hiking_upward_url),
                        "hike_len_in_mi": hike_len_in_mi,
                        "difficulty_rating": difficulty_rating,
                        "streams_rating": streams_rating,
                        "views_rating": views_rating,
                        "solitude_rating": solitude_rating,
                        "camping_rating": camping_rating,
                        "hiking_duration_str": hiking_duration,
                        "elevation_gain_ft": elevation_gain_ft,
                    },
                    index=[0],
                )
                return df
            elif len(tables.find_all("tr")) == 8:
                rating_table = tables.find_all("tr")[1].find_all("td")
                (
                    hike_len_in_mi,
                    difficulty_rating,
                    streams_rating,
                    views_rating,
                    solitude_rating,
                    camping_rating,
                ) = get_rating(rating_table)

                time_elev = tables.find_all("tr")[2].find_all("td")[1]
                hiking_duration, elevation_gain_ft = get_duration_and_elevation(
                    time_elev
                )

                rating_table2 = tables.find_all("tr")[3].find_all("td")
                (
                    hike_len_in_mi2,
                    difficulty_rating2,
                    streams_rating2,
                    views_rating2,
                    solitude_rating2,
                    camping_rating2,
                ) = get_rating(rating_table2)

                time_elev2 = tables.find_all("tr")[4].find_all("td")[1]
                hiking_duration2, elevation_gain_ft2 = get_duration_and_elevation2(
                    time_elev2
                )

                df = DataFrame(
                    {
                        "hike_name": [
                            str(hike_soup.title.text),
                            str(hike_soup.title.text),
                        ],
                        "park_abbreviation": [
                            hiking_upward_url.replace(
                                "https://www.hikingupward.com/", ""
                            ).split("/", 1)[0],
                            hiking_upward_url.replace(
                                "https://www.hikingupward.com/", ""
                            ).split("/", 1)[0],
                        ],
                        "hike_url": [
                            str(hiking_upward_url + "1"),
                            str(hiking_upward_url + "2"),
                        ],
                        "hike_len_in_mi": [hike_len_in_mi, hike_len_in_mi2],
                        "difficulty_rating": [difficulty_rating, difficulty_rating2],
                        "streams_rating": [streams_rating, streams_rating2],
                        "views_rating": [views_rating, views_rating2],
                        "solitude_rating": [solitude_rating, solitude_rating2],
                        "camping_rating": [camping_rating, camping_rating2],
                        "hiking_duration_str": [hiking_duration, hiking_duration2],
                        "elevation_gain_ft": [elevation_gain_ft, elevation_gain_ft],
                    },
                    index=[0, 1],
                )
                return df
            elif len(tables.find_all("tr")) == 10:
                # if table length is 10 (tables 2/3, 5/6)
                rating_table = tables.find_all("tr")[2].find_all("td")
                (
                    hike_len_in_mi,
                    difficulty_rating,
                    streams_rating,
                    views_rating,
                    solitude_rating,
                    camping_rating,
                ) = get_rating(rating_table)

                time_elev = tables.find_all("tr")[3].find_all("td")[1]
                hiking_duration, elevation_gain_ft = get_duration_and_elevation(
                    time_elev
                )

                rating_table2 = tables.find_all("tr")[5].find_all("td")
                (
                    hike_len_in_mi2,
                    difficulty_rating2,
                    streams_rating2,
                    views_rating2,
                    solitude_rating2,
                    camping_rating2,
                ) = get_rating(rating_table2)

                time_elev2 = tables.find_all("tr")[6].find_all("td")[1]
                hiking_duration2, elevation_gain_ft2 = get_duration_and_elevation2(
                    time_elev2
                )

                df = DataFrame(
                    {
                        "hike_name": [
                            str(hike_soup.title.text),
                            str(hike_soup.title.text),
                        ],
                        "park_abbreviation": [
                            hiking_upward_url.replace(
                                "https://www.hikingupward.com/", ""
                            ).split("/", 1)[0],
                            hiking_upward_url.replace(
                                "https://www.hikingupward.com/", ""
                            ).split("/", 1)[0],
                        ],
                        "hike_url": [
                            str(hiking_upward_url + "1"),
                            str(hiking_upward_url + "2"),
                        ],
                        "hike_len_in_mi": [hike_len_in_mi, hike_len_in_mi2],
                        "difficulty_rating": [difficulty_rating, difficulty_rating2],
                        "streams_rating": [streams_rating, streams_rating2],
                        "views_rating": [views_rating, views_rating2],
                        "solitude_rating": [solitude_rating, solitude_rating2],
                        "camping_rating": [camping_rating, camping_rating2],
                        "hiking_duration_str": [hiking_duration, hiking_duration2],
                        "elevation_gain_ft": [elevation_gain_ft, elevation_gain_ft],
                    },
                    index=[0, 1],
                )
                return df
            else:
                pass
        except Exception:
            pass

def get_many_hikes() -> DataFrame:
    """Return a dataframe with data for all hikes on hikingupward.com and do some minor cleaning on the dataframe """

    try:
        url = "https://www.hikingupward.com/"
        data = get(url)
        soup = BeautifulSoup(data.text, "html.parser")

        url_links = [
            url + url_link.attrs.get("href")
            for nav in soup.find_all("div", {"class": "navigation"})
            for url_link in nav.find_all("a", href=True)
        ]

        hike = []
        for url_link in url_links:
            one_hike_df = get_one_hike_data(url_link)
            hike.append(one_hike_df)
        hike_df = concat(hike, ignore_index=True)

        hike_df.streams_rating.fillna(0, inplace=True)
        hike_df.camping_rating.fillna(0, inplace=True)
        hike_df.views_rating.fillna(0, inplace=True)

        hike_df.dropna(
            subset=[
                "hike_url",
                "hike_len_in_mi",
                "difficulty_rating",
                "streams_rating",
                "views_rating",
                "solitude_rating",
                "camping_rating",
            ],
            inplace=True,
        )

        print(hike_df.head())
        schema.validate(hike_df, lazy=True)

        hike_df.to_csv("data/hiking_upward_data_TEST.csv", index=False) #av.note: will eventually want to get rid of this

    except Exception as e:
        print(e)

    return hike_df

def scale_df(df: DataFrame, 
    list_vars: List = [
            "hike_len_in_mi",
            "difficulty_rating",
            "streams_rating",
            "views_rating",
            "solitude_rating",
            "camping_rating",
        ] #av.note: this is a subset eventually want this to be all numeric vars in hike_df
        ) -> DataFrame:
    """Using StandardScaler to scale numeric variables in dataframe and returned scaled dataframe with hike_url as unique identifier"""

    std_scaler = StandardScaler()
    scaled = df[list_vars]
    df_scaled = std_scaler.fit_transform(scaled.to_numpy())
    df_scaled = DataFrame(df_scaled, columns=scaled.columns)
    df_scaled["hike_url"] = df["hike_url"]

    return df_scaled  ##av.note: might need to return the standard scaler so that it can be used in the recommendation


def get_recommendations():
    """This function is a work in progress, will change from current iteration """

    hike_df = get_many_hikes()
    df_scaled = scale_df(hike_df)
    tcdf = tc.SFrame(data=df_scaled)

    ## fit the model
    recommender_model = tc.recommender.item_content_recommender.create(
        tcdf, item_id="hike_url", verbose=False
    )

    ## return the fifteen most similar items for every item in the training data
    nn = recommender_model.get_similar_items(k=15)

    nn.export_csv("data/nearest_15_recommendations_for_each_hike_TEST.csv") #av.note: will eventually want to get rid of this
    print("recommender finished")

    return nn


get_recommendations()