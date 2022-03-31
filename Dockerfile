FROM python:3.7-slim

COPY poetry.lock pyproject.toml ./

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["python"]

# WORKDIR /app
# COPY . /src

# EXPOSE 8501

# ENTRYPOINT ["streamlit", "run"]

# CMD ["src/streamlit_app.py"]