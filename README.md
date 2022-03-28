# Hiking Upward Recommender

**Status**: IN PROGRESS

**Purpose**: The purpose of this repo is to create and deploy an app that recommends similar Hiking Upward hikes based on a Hiking Upward Hike (using a URL as an identifier). 

## Skills used:
- Web scraping using requests and beautifulsoup 
- Content-based recommender systems using Apple's Turicreate
- Creating reproducible virtual environments using conda and poetry
- Dockerizing the virtual environment
- Deploying the recommender app using streamlit

## Lessons learned:
- The turicreate package doesn't run on windows (only mac, Linux, or Windox Linux subsystem)
- This required the use of docker container. 

## Useful resources:
### Turicreate:
- [Turicreate Recommender System User Guide](https://apple.github.io/turicreate/docs/userguide/recommender/)
- [Turicreate Item Recommender Docs](https://apple.github.io/turicreate/docs/api/generated/turicreate.recommender.item_content_recommender.ItemContentRecommender.html)

### Poetry:
- [Poetry Docs](https://python-poetry.org/docs/basic-usage/)
https://mungingdata.com/python/jupyter-workflow-poetry-pandas/ 
https://pythonspeed.com/articles/poetry-vs-docker-caching/

### Docker:
- [Deploy streamlit with Docker](https://towardsdatascience.com/create-an-awesome-streamlit-app-deploy-it-with-docker-a3d202a636e8#:~:text=Time%20to%20Dockerize%20the%20application)

### Streamlit:
