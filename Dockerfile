FROM python:3.11-slim
RUN pip install poetry
WORKDIR /app/src
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction --no-ansi
COPY ./src /app/src
RUN mkdir -p /app/src/model/models
ENV PYTHONPATH=/app/src
EXPOSE 8000
CMD ["poetry", "run", "python", "-m", "uvicorn", "src.inference:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
