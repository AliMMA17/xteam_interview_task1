# xteam задание 1

## Instructions to run:

### Running in Docker:
1. `docker compose up --build`

### Running locally:
#### Backend:
1.change the .env db and redis address to localhost
2. `uvicorn app.main:app --reload`
3. `python -m app.seed_database`
   
**Optional:**
3. Inside the `app` folder: `pytest test_main.py -v`

Frontend:
1. change the .env address to localhost
2. `cd frontend`
3. `npm start`
### Postman Document for APIs:
[Postman Documentation](https://documenter.getpostman.com/view/37281446/2sAYkAR3Bu)

## Directories:
- **app:**
  - `main.py`: Main FastAPI application
  - `cache.py`: Redis functions
  - `database.py`: Database configuration
  - `models.py`: Database tables
  - `recommendations.py`: Endpoint for recommendations
  - `seed_database.py`: Generate sample data
  - `test_main.py`: Pytest program
