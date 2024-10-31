# Eksiseyler API

Eksiseyler API is a FastAPI-based application for fetching and managing article data from a database. It provides endpoints to retrieve all articles, a random article, and a health check endpoint.

## Features

- Retrieve all articles from the database.
- Get a random article.
- Simple health check endpoint.

## Requirements

- Python 3.7+
- Docker (if using containerization)
- PostgreSQL database

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/frknltrk/eksiseyler_api
   cd eksiseyler_api
   ```

2. **Set Up Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Ensure that the following environment variable is set:

- `DATABASE_URL`: The connection URL for your PostgreSQL database.

## Running the Application

You can run the application locally using:

```bash
fastapi dev app/main.py
```

By default, it will run on `http://127.0.0.1:8000`.

## API Endpoints

- **GET /articles/all**: Retrieve all articles.
- **GET /articles/random**: Retrieve a random article.
- **GET /health**: Health check endpoint.

## Deployment

### Platforms

- fly.io (used & recommended)
- render.com
- railway.app
- Heroku

### Docker

```bash
docker build -t eksiseyler-img .
docker run -d --name eksiseyler -p 8000:8000 eksiseyler-img -e DATABASE_URL=your_database_url
```

For more details, refer to the FastAPI documentation [here](https://fastapi.tiangolo.com/deployment/docker/#build-the-docker-image).

### Fly.io

To deploy using Fly.io, ensure your `fly.toml` is configured correctly. Key settings include:

- `app`: Name of your app.
- `primary_region`: Example set to `'ams'` for Amsterdam.

Refer to the [Crontab with Supercronic](https://fly.io/docs/blueprints/supercronic/) and [App configuration (fly.toml)](https://fly.io/docs/reference/configuration/) for more details.

## License

[MIT License](LICENSE)
