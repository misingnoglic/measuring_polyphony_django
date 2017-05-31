# Measuring Polyphony: Django Project
## About
This website is created to display the research of Karen Desmond at Brandeis University. It is built using Django with Python 3.6.

## How to Install

0. Run the initial setup guide: https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04
1. Install Python 3.6 on your machine
    1. To install on ubuntu: https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get
2. Create a virtual environment for verovio.
    1. `python3.6 -m pip install virtualenv`
    2. `mkvirtualenv polyphony`
    3. `source polyphony/bin/activate`
    4. Note: You should always do that `source` command when using python on the server
3. Install SWIG
    1. For ubuntu: `sudo apt-get install swig`
4. Install the developer tools for Python
    1. `sudo apt-get install python3-dev`
5. Install Verovio: https://github.com/rism-ch/verovio/wiki/Building-instructions#building-the-python-toolkit
6. Git pull this repository, and CD into the folder it was downloaded to
7. (In the virtual environment you sourced in step 2) - `pip install -r requirements.txt`
9. Create the  secrets.py folder, and populate it with these four variables:
    1. SECRET_KEY -> A string which is your secret key
    2. DATABASE_PASSWORD -> The password for the 'polyphony' user in the database (you'll add this later)
    3. font_path => "{path verovio was installed}/data"
    4. debug -> True or False (depending on if the website is live or not)

10. Go through this tutorial to set up the actual web server: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
    1. Note that this is the guide to making a new app - there isn't one on hosting an already made app. Keep this in mind
    2. In postgres: Create a database called polyphony, and a user called polyphony, and grant that user all privileges on the database

11. To import data from the CSV file, you can do `python importer.py`


## How to modify files on the website

1. Push the files to git.
2. Pull them onto the server
3. Activate the virtual environment. On the current box you would do `source ~/envs/polyphonyenv/bin/activate`
4. If you changed any of the static files: `python manage.py collectstatic` (Say yes if it asks for permission)
5. If you changed any of the files in models.py
    1. `python manage.py makemigrations`
    2. `python manage.py migrate`
6. Run `sudo systemctl restart gunicorn`

## Important files

* importer.py -> The program I wrote to transfer the files from the CSV to the database
* requirements.txt -> List of all the python libraries needed for this app to run
* secrets.py -> All of the "secret" variables that should not be checked into the git repository.
* measuring_polyphony/settings.py -> Where the settings for the project are.
* media/... -> All the files uploaded to the database
* mei_files/... -> All the initial mei files given for the project. They dont serve any purpose in the app, but they're good to keep in that format.
* static/... -> All of the collected static files. Don't edit these ones, always edit the ones in viewer/static/... and then run `python manage.py collectstatic`
* templates/... -> All of the templates that are rendered - edit these to edit the HTML files for the website. They are rendered using the Django templating language (like HTML but with some logic for loops and stuff). The way the templates are rendered is you have these template files, which refer to variables and such, and those are provided by the functions/classes in viewer/views.py
* viewer/... -> All of the files for the main app. 
    * static/... -> All of the CSS, javascript, etc for the website template we're using: https://templated.co/introspect
    * admin.py -> The code that controls the admin interface
    * logic.py -> All of the functions relating to verovio
    * models.py -> All of the database models. If you want to change the SQL, this is where you do it (and then run the makemigrations/migrate commands)
    * urls.py -> All of the URLS for the project. They're determined using regex. When a user types a URL, django uses this file to decide which view to run.
    * views.py -> The files that render web pages. 
    
## If you want to edit:
* HTML: files in templates/...
* CSS: files in viewer/static/introspect/assets/css
* Add a new page: Write the template, put it in the templates folder, add a function in viewer/views.py that renders the template with a context, and then write the URL in viewer/urls.py


This tutorial might be helpful: https://docs.djangoproject.com/en/1.11/intro/tutorial01/