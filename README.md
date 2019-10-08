# food-platform
### When you need to upload to the github ##
### settings.py  security key need to be remove or set the project into privacy ##

### When the project is going to online the settings.py DEBUG need to set to False ##

### Test the website
    cd softway_sys
    python manage.py runserver

### Create or upadate requirements
   pip freeze > requirements.txt

### Environment install requirements
   Python 3.7 or Higher
   Use venv as environment setting and connect to Anaconda's python or something else

   pip install -r requirements.txt

### When you change any thing in the database
    python manage.py makemigrations
    python manage.py migrate


### Unit test ###
   #### Write unit test to avoid the big change of the Project, ex: fetch from github or merge ####

### Remove migration
   python manage.py migrate --fake <your_app>
   find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
   find . -path "*/migrations/*.pyc"  -delete

### Reset migrations
   https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html