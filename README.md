# <a href = "https://simple-recommender.herokuapp.com/" >simple-recommender</a>
A simple content based recommendation application. NLP model is trained in another repository. This application makes recommendation given input using pre-trained model.

# Running application
## Option 1: Docker
### Requirements
Docker allows you to run this application on every operating system. The only requirement is to have running Docker engine instance. If it is installed and running, `docker run hello-world` command returns "Hello from Docker!" text. Otherwise, please head over to https://docs.docker.com/get-started/#download-and-install-docker and go through the installation steps.

### Running
1. Download this repository to your local machine directly from <a href="https://github.com/TUM-IDP-WS-20/simple-recommender/archive/refs/heads/master.zip">here</a> or via Git:
    ```shell
   git clone https://github.com/TUM-IDP-WS-20/simple-recommender.git
    ```
2. In the root directory, run `docker-compose up`

That's all you need to do! Docker build and run 3 containers:
- lrs_app : The main literature recommender system
- nginx : An <a href="https://www.nginx.com/">Nginx</a> Webserver to welcome requests first and redirect them to the LRS app running behind the nginx
- lrs_db : A <a href="https://www.postgresql.org/">Postgresql</a> database to store user ratings

These all steps may take up to 5 minutes depending on your network connection. Once installation is done, you can reach the application on  http://localhost.

Note: If you want to make changes on the code, this option has one drawback that you need to delete the image created for 'lrs_app' and rerun `docker-compose up` to build and run 'lrs_app' service.

## Option 2: Setup Local Environment
1. ### Create a virtual environment
```shell
virtualenv --python=python3.8 .venv
```

2. ### Activate environment
```shell
source .venv/bin/activate
```

3. ### Install required python packages
```shell
pip3 install -r requirements.txt
```

4. ### Database Configuration
   1. Make sure that you have installed `postgresql` on your computer.
   2. Create a database with the following credentials:
      - Username: user
      - Password: password
      - Database Name: rec_database
      - Host: localhost
      - Port: 5432
      - Use docker/lrs_database_init.sql for initial tables

        OR simply run a prepared postgres container via:
        ```shell
        docker-compose run localDb bash
        ```
   3. Set environment variables
    ```shell
    export APP_SETTINGS="app.config.DevelopmentConfig"
    export DATABASE_URL="postgresql://user:password@localhost:5432/rec_database"
    ```

5. ### Running
    Run the command below to run the application:
   ```shell
   flask run
   ```
   You can reach the application on http://localhost:5000

# Development
1. ### Install environment

2. ### Activate Github Large files to keep model files
   Install git lfs(Check up-to-date doc: https://git-lfs.github.com/)
   ```shell
   git lfs install
   git lfs pull
   ```
3. ### Database Configuration
   Make sure that you have installed `postgresql`.

      - docker-compose run localDb bash
      - export APP_SETTINGS="app.config.DevelopmentConfig"
      - export DATABASE_URL="postgresql://localhost:5432/rec_database"
      - python3 manage.py db init
      - python3 manage.py db migrate
      - python3 manage.py db upgrade
3. ### Run application
   Run the command below to run the application:
   ```shell
   flask run
   ```
   You can reach the application on http://localhost:5000

4. ### Keep dependencies clear
   All dependencies will be saved in `requirements.txt`. If a new library is needed for a notebook, please update dependecies on `requirements.txt` accordingly. You can follow the steps below to update it quickly:

   - Be sure to activate the environment as shown in **1.ii.**
   - Install the packages that you need like `pip3 install <package name>`
   - Update the `requirements.txt`:
   ```shell
   pip3 freeze -r requirements.txt > requirements.txt
   ```


## Deployment
1. ### Heroku Setup
   1. Access
     Create a Heroku account and install heroku CLI. You can follow instruction here: https://devcenter.heroku.com/articles/getting-started-with-python
   2. Login
   ```shell
      heroku login
   ```
   3. Add `heroku` remote upstream url
   ```shell
   git remote add heroku https://git.heroku.com/simple-recommender.git
   ```
   4. Fetch heroku branch
   ```shell
      git fetch heroku master
   ```
   5. Database Config
        1. `heroku config:set APP_SETTINGS=app.config.ProductionConfig --remote heroku`
        2. `heroku addons:create heroku-postgresql:hobby-dev --app simple-recommender`
2. ### Deployment
   1. Commit changes
     Merge changes to `master` branch
   2. Deploy
   Then, push changes to heroku to trigger new deployment:
   ```shell
      git push heroku master
   ```

3. ### Configure database if you made any change on it
    1. `heroku config --app simple-recommender`
    2. `git push heroku master:master --no-verify`
    3. `heroku run python manage.py db upgrade --app simple-recommender`
