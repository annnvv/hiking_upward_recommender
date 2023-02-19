# Hiking Upward Recommender

**Status**: In Progress

**Purpose**: The purpose of this repo is to create and deploy an app that recommends similar Hiking Upward hikes based on a Hiking Upward Hike (using a URL as an identifier). 

I decided to do this project because I wasn't satisfied by the simple filtering page that Hiking Upward has [here](https://www.hikingupward.com/maps/). I wanted to find similar hikes to the ones that I enjoyed and I wanted to learn about recommender systems, which is why I chose to take on this project. 

App version 0 (complete) : Data scraping and recommendation done in notebooks, results exported in a csv. Streamlit app uses the csvs to display recommendations. 

App version 1 (in progress): Convert notebooks to functions (maybe later classes), streamlit app runs the functions and caches the results and displays recommendations. 

To see the app, please visit [this link](https://share.streamlit.io/annnvv/hiking_upward_recommender/main/app/streamlit_app.py).

**Data Source**: webscraping [Hiking Upward](https://www.hikingupward.com)

## Skills used:
- Web scraping using `requests` and `beautifulsoup` 
- Validating a dataframe using `pandera`
- Content-based recommender systems using ~~Apple's `Turicreate`~~
- Creating reproducible virtual environments using `poetry`
- `Docker`izing the virtual environment
- Deploying the recommender app using `streamlit`

## Lessons learned:
- The turicreate package doesn't run on windows (only mac, Linux, or Windox Linux subsystem)
  - This required the use of docker container. 
- Eventually, I decided against using turicreate. Some of the reasons: 
  - Turicreate uses its own data types (such as SFrame and SArray)
  - Tucireate only supports up to python 3.8
  - There were issues with dependency resolution related to turicreate (mainly coremltools version 3.3 and tensorflow version) 
  - It was difficult to figure out how to get a recommendation from the model using new data (maybe because of the data types) 

## Useful resources:

### Poetry:
- [Poetry Docs](https://python-poetry.org/docs/basic-usage/)
- https://realpython.com/dependency-management-python-poetry/
- https://mungingdata.com/python/jupyter-workflow-poetry-pandas/ 
- https://pythonspeed.com/articles/poetry-vs-docker-caching/

Useful command line command for poetry 
```
poetry cache clear --all pypi ##(seem to speed up dependency resolution)

poetry env remove python ## delete poetry virtual env
```

### Docker:
- [Deploy streamlit with Docker](https://towardsdatascience.com/create-an-awesome-streamlit-app-deploy-it-with-docker-a3d202a636e8#:~:text=Time%20to%20Dockerize%20the%20application)
- [Docker Ignore](https://codefresh.io/docker-tutorial/not-ignore-dockerignore-2/)

### Streamlit:
- [Streamlit Cheatsheet](https://docs.streamlit.io/library/cheatsheet)
- https://www.rockyourcode.com/run-streamlit-with-docker-and-docker-compose/

### Pandera:
- [Pandera Docs](https://pandera.readthedocs.io/en/stable/index.html)
- [Validating Pandas DataFrame](https://towardsdatascience.com/validate-your-pandas-dataframe-with-pandera-2995910e564)

### Turicreate:
- [Turicreate Recommender System User Guide](https://apple.github.io/turicreate/docs/userguide/recommender/)
- [Turicreate Item Recommender Docs](https://apple.github.io/turicreate/docs/api/generated/turicreate.recommender.item_content_recommender.ItemContentRecommender.html)
