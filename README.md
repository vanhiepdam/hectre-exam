# hectre-exam

## Notes & Assumptions
1. The timezone is used in this project is UTC+0.

2. All apis are public.

3. Because I don't have AWS account. So for this exam, all services will be deployed by docker.

# Deployment

## Deploy backend
1. Change working dir
    ```
    cd harvest_be
    ```
2. Set env variables
    ```
    cp .env.template .env
    ```
    .env value
    ```
    DJANGO_SETTINGS_MODULE=harvest_be.settings.local
    ALLOWED_HOSTS=127.0.0.1
    
    POSTGRES_DB=harvest
    POSTGRES_USER=pguser
    POSTGRES_PASSWORD=pguser
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    ```
3. Deploy
    ```
    docker-compose build
    docker-compose up -d
    ```
4. Run unit test
    ```
    docker exec -w /code/source harvest_be_web_1 pytest
    ```
5. Run
    
    For now, api server is running on http://localhost:8000/

6. Run script to populate data to db
    
    For the first time launching api server, run this script to populate data to db
    ```
    docker exec -w /code/source harvest_be_web_1 python scripts/setup_data/populate_data_to_db.py
    ```
    
    Expected: Done creating 80 harvesting records 

7. Api Doc
    ```http://localhost:8000/api-doc/```
