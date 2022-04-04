import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


def get_rating(table):
    try:
        hike_len_in_mi = float(table[0].text.replace("mls", "").strip())
    except:
        hike_len_in_mi = np.nan

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
        difficulty_rating = np.nan

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
        streams_rating = np.nan

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
        views_rating = np.nan

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
        solitude_rating = np.nan

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
        camping_rating = np.nan

    return (
        hike_len_in_mi,
        difficulty_rating,
        streams_rating,
        views_rating,
        solitude_rating,
        camping_rating,
    )


def get_duration_and_elevation(table):
    try:
        hiking_duration = str(table.contents[0].text.strip())
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
        )
    except:
        elevation_gain_ft = ""

    return hiking_duration, elevation_gain_ft


def get_duration_and_elevation2(table):
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


def get_hike_data(hiking_upward_url: str) -> pd.DataFrame:

    hike_content = requests.get(hiking_upward_url)
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

                df = pd.DataFrame(
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

                df = pd.DataFrame(
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

                df = pd.DataFrame(
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


####
try:
    url = "https://www.hikingupward.com/"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    url_links = [
        url + url_link.attrs.get("href")
        for nav in soup.find_all("div", {"class": "navigation"})
        for url_link in nav.find_all("a", href=True)
    ]

    hike = []
    for url_link in url_links:
        one_hike_df = get_hike_data(url_link)
        hike.append(one_hike_df)
    hike_df = pd.concat(hike, ignore_index=True)

    hike_df.streams_rating.fillna(0, inplace=True)
    hike_df.camping_rating.fillna(0, inplace=True)
    hike_df.views_rating.fillna(0, inplace=True)

    print(hike_df.head())
    hike_df.to_csv("/data/hiking_upward_data.csv", index=False)

except Exception as e:
    print(e)

