5.12.24 - page 75 of 338

# A new Django environment and project:
  ## Create a new virtual environment named .venv (after navigating to proper directory)
  `python3 -m venv .venv`

  ## Activate virtual environment
  `source .venv/bin/activate`

  ## Install Django (version 4.2.0) inside the virtual environment 
  `python3 -m pip install django~=4.2.0`

  ## Creating / starting a new Django project (be sure to add a period at the end)
  `django-admin startproject <name_of_project> .`

  ## Create a new Django App for a specific purpose (optional)
  - Remember to add the app to the list of "Installed Apps" in Django's settings.py file"

  `python3 manage.py startapp <app_name>`

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