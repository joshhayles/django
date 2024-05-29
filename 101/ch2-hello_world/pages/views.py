from django.shortcuts import render
# render() is a Django shortcut function that can be used to create views, however, some say a simpler approach is to use the built-in HttpResponse method

from django.http import HttpResponse

def homePageView(request):
    return HttpResponse("Hello, World!")
