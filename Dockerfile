FROM python:3.11-slim
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi
COPY ./src /app/src
RUN mkdir -p /app/src/model/models
RUN poetry run pip install --upgrade uvicorn
RUN poetry run pip list | grep uvicorn  # Debugging step
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "--app-dir", "/app", "src.inference:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
