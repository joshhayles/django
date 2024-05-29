from django.urls import path 

from .views import homePageView

urlpatterns = [
    path("", homePageView, name="home"),
]

"""
The url pattern has three parts:
    - the empty string "" represents the root URL
    - a reference to the view "homePageView"
    - an optional named URL pattern "home"

If the user requests the home page represented by the empty string "", Django should use the view called homePageView
"""