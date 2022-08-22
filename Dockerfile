FROM python:3.8-slim

WORKDIR /app
COPY . .

COPY poetry.lock pyproject.toml ./

RUN pip3 install poetry
RUN poetry config virtualenvs.create true
RUN poetry install --no-dev

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["streamlit_app.py"]
