# <a href = "https://simple-recommender.herokuapp.com/" >simple-recommender</a>
A simple content based recommendation application. NLP model is trained in another repository. This application makes recommendation given input using pre-trained model.

# Development
1. ### Install environment
   1. Create an virtual environment
   ```shell
   virtualenv --python=python3.8 .venv
   ```

   2. Activate environment
   ```shell
   source .venv/bin/activate
   ```

   3. Install required python packages
   ```shell
   pip3 install -r requirements.txt
   ```
2. ### Activate Github Large files to keep model files
   Install git lfs(Check up-to-date doc: https://git-lfs.github.com/)
   ```shell
   git lfs install
   git lfs pull
   ```
3. ### Database Configuration
   Make sure that you have installed `postgresql`.

      - docker-compose run localDb bash
      - export APP_SETTINGS="config.DevelopmentConfig"
      - export DATABASE_URL="postgresql://localhost:5432/rec_database"
      - python3 manage.py db init
      - python3 manage.py db migrate
      - python3 manage.py db upgrade
3. ### Run application
   ```shell
   flask run
   ```

4. ### Keep dependecies clear
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
        1. `heroku config:set APP_SETTINGS=config.ProductionConfig --remote heroku`
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
