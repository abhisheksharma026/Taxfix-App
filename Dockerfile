FROM python:3.11-slim
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]