# hectre-exam

## Notes & Assumptions
1. The timezone is used in this project is UTC+0.

2. All apis are public, no authentication at all.

3. Because I don't have AWS account. So for this exam, all services will be deployed by docker.

4. No unit tests for FE

5. backend APIs are using Django framework

6. No https

7. The legend of piechart is not correct with design but I have solution that the color for each variety and orchard can be configured in model at backend to response for user. I dont have enough time to do that.

### git & CI & CD workflow 
1. "main" is the protected branch
2. devs fork new branch to develop their feature
3. devs create PR in order to be merged to "main"
4. Setup 2 github action: CI, Deploy
5. Every push on the branches of open pull requests, Action "CI" will run unit tests and response the result
6. Every merge on branch "main", action "Deploy" will run to deploy new source code

Note: In this example, my action "Deploy" will ssh to the server contains source code and run script to deploy

Now it always be failed because it has no credentials to ssh to server 

# Deployment

## Setup backend
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
    DJANGO_SETTINGS_MODULE=harvest_be.settings.dev
    ALLOWED_HOSTS=127.0.0.1,localhost,nginx
    
    POSTGRES_DB=harvest
    POSTGRES_USER=pguser
    POSTGRES_PASSWORD=pguser
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    ```
  
## Deploy
1. Deploy
    ```
    cd deployments
    docker-compose build
    docker-compose up -d
    ```
2. Run BE unit tests
    ```
    docker exec -w /code/source deployments_backend_1 pytest
    ```

3. Run script to populate data to db
    
    For the first time launching api server, run this script to populate data to db
    ```
    docker exec -w /code/source deployments_backend_1 python scripts/setup_data/populate_data_to_db.py
    ```
    
    Expected: Done creating 80 harvesting records 

4. Live
    
    For now, dashboard is now live at http://localhost/

5. Api Doc
    ```http://localhost/api-doc/```

