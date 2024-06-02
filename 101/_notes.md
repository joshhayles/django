5.12.24 - page 116 of 338

# Follow this general process for creating a new Django environment, project, and app:
  ## Create a new folder directory and navigate into it

  ## Create a new virtual environment named .venv (after navigating to proper directory)
  `python3 -m venv .venv`

  ## Activate virtual environment (keep activated for now)
  `source .venv/bin/activate`

  ## Install Django (version 4.2.0) inside the virtual environment 
  `python3 -m pip install django~=4.2.0`

  ## Creating / starting a new Django project (be sure to add a period at the end)
  `django-admin startproject <name_of_project> .`

  ## Create a requirements.txt file containing Python packages installed in our virtual environment (note: update this when a new Python package is installed)
  `python3 -m pip freeze > requirements.txt` 

  ## Create a new Django App for a specific purpose (optional)
  - Remember to add the app to the list of "Installed Apps" in django_project/settings.py file

  `python3 manage.py startapp <app_name>`

  ## Execute the migrate command to create an initial database from Django's default settings
  `python3 manage.py migrate`

  ## Launch Django server
  `python3 manage.py runserver`

# Django Databases
  ## Migrate the database (server needs to be stopped first). Django will create a SQLite database, and migrate its built-in apps
  `python3 manage.py migrate`

# Django Views
  ## There are two types of views in Django: function-based views and class-based views.

  ## Updating views and urls in Django
  When you update a view or url in your Django app, be sure to also update your django_project/urls.py file: that's the first place all URL requests come into, and you can include URLs from individual apps.

# General Notes about Django

  ## Django's Model, View, Template, URL (MVTU) design architecture
  - Model: Manages data and core business logic. Business logic would be rules and operations that handle the data and how it's processed, validated, and manipulated before being presented to the user or stored in the database.

  - View: Describes which data is sent to the user, but not its presentation. Forms, authentication, CRUD operations, etc. A view is a Python function that accepts a Web request and returns a Web response (such as the html contents of a web page, a redirect, 404, image, etc).
  
  When a webpage is requested, Django automatically creates an HttpRequest object that contains metadata about the request. Then Django loads the appropriate view, passing the HttpRequest object in as the first argument to the view function.

  The view is responsible for returning the HttpResponse object.

  - Template: Every web framework needs a convenient way to generate HTML files. Django's approach and solution for this is Templates. The template component presents the data as HTML with optional CSS and JavaScript. 

  Django links views to templates.

  By default, Django's template loader will look within each app for related templates. However, this can become a complicated approach, as Django would look for nested views like this:

  pages_app > templates > pages > home.html

  While this is a thorough, and safer approach by Django (it assures that the correct html files are associated with its corresponding app), there is an alternate method.

  Instead, you can create a single project-level 'templates' directory and place all templates within it. By altering our django_project/settings.py file, we can tell Django to look in that specific directory for templates.

  - URL configuration: This maps URLs to their corresponding views, allowing you to define the structure of your web application and how different URL patterns should be handled.

  In other popular design patters like Model, View, Controller (MVC), the "Controller" component can be thought of as being divided into a View and URL config in Django.

  ## What happens when you visit a URL when using Django?
  When you enter a URL when using Django, the first thing that happens within your Django project is that `runserver` starts up and helps Django look for a matching URL pattern, which is contained in the urls.py file.

  The URL pattern is linked to a single view contained in the views.py file, which combines the data from the model (stored in models.py), and the styling from a template (any file ending in .html). 

  Finally, the view returns a HTTP response to the user.

  ## What is a Django App?
  A Django App is a method of creating "mini applications" to help organize and structure your project. Each app should control an isolated piece of functionality.

  For example, an e-commerce site might have an Django app just for user authentication, another app for payments, etc.

  You can think of these as features, which have a single function.

  ## Updating Django URLs
  When you're updating URLs, there are two locations you need to update: the project-level urls.py and any app-level urls.py files.
  
  In the project-level/urls.py, you define the top-level URL patterns and include the URL patterns from individual apps. 

  Each Django app can have its own urls.py file and settings: myapp/urls.py. This file can define the URL patterns specific to that app.

  Example for urlpatterns:

  ```python
  urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("pages.urls")),
]

  The first path maps all URLs starting with admin/ to the built-in Django admin site URLs.

  The second path maps the root URL (which is the empty string "") to the URL patterns defined in the app: "pages.urls" module.

  The include() function is used to include a separate set of URL patterns from another Python module (in this case, pages.urls).

  For example, if pages.urls contains patterns like:
  path('about/', about_view, name='about') and 
  path('contact/', contact_view, name='contact')

  then URLs like '/about' and '/contact' would be handled by their respective views (about_view and contact_view).

  ## Django's Database
  When you run Django's migrate or runserver command(s), a db.sqlite3 file is created. However, the migrate command will sync the database with the current state of any database models contained in the project and listed in the INSTALLED_APPS section. To ensure the database is current, you'll need to run migrate, and also makemigrations, each time you update a model.

  When you create a new app and view the models.py file, you'll see that Django imports a module called 'models' to help us build new database models. These models are the characteristics of the data in our database.

  For each database model we want to create, the suggested approach is to subclass, or extend, the django.db.models.Model and then add our fields.

  When a new model has been created or modified, you need to activate it (make sure your server is not running):

  - First, create a new migrations file using the `python3 manage.py makemigrations <app_name>` command
  - Next, you build the database with the `python3 manage.py migrate` command, which executes the instructions in the migrations file 

  Note: it's not required to include the app_name after the makemigrations command. However, if you do not specify an app name, a migrations file will be created for all available changes throughout the Django project.

  ## Django's Admin
  To use Django's admin portal, you first create a superuser who can log in:
  `python3 manage.py createsuperuser`

  To display our database content on the homepage, we have to link our views, templates, and URLs.

# Django Commands
  ## static files: compile all of your project's static files into a new root-level directory called staticfiles
  `python3 manage.py collectstatic`

  ## install environs (for environment variables) along with the django extension
    - be sure to import: from environs import Env
  `python3 -m pip install "environs[django]"==9.5.0`