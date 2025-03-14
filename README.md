Instrcutions to run:

- Running in  docker : 
1- docker compose up --build

- Running locally:
1- uvicorn app.main:app --reload
2- python -m app.seed_database
optional - 3 : inside of app folder: pytest test_main.py -v


postman Document for APIs: https://documenter.getpostman.com/view/37281446/2sAYkAR3Bu

Directories:
app: 
main.py : " main fastAPI Application
cache.py: " Redis functions"
database.py: "database configuration
models.py : "database tables "
recommendations.py : "endpoint for recommendation"
seed_database.py: "generate a sample data " 
test_main.py :"pytest program " 
