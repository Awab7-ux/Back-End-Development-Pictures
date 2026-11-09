# Back-End-Development-Pictures

A small Flask REST API for browsing and managing event pictures. Picture records are loaded from `backend/data/pictures.json` when the application starts.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Check API health |
| GET | `/count` | Return the number of pictures |
| GET | `/picture` | Return all pictures |
| GET | `/picture/<id>` | Return one picture by ID |
| POST | `/picture` | Add a picture (duplicate IDs return 302) |
| PUT | `/picture/<id>` | Replace a picture by ID |
| DELETE | `/picture/<id>` | Delete a picture by ID |

## Run locally

Install the dependencies and start Flask:

```bash
pip install -r requirements.txt
flask --app backend run
```

## Run tests

```bash
pytest -v
```

## Build the Docker image

```bash
docker build -t pictures-api .
```

Run the image on port 8080 with `docker run --rm -p 8080:8080 pictures-api`.