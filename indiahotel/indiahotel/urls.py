"""indiahotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from api.views import MenuItems,SpecificItems
from rest_framework_simplejwt.views import TokenVerifyView

from hotel.views import *
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("dishes",DishViewViewset,basename="dishes"),
router.register("mdishes",DishModelViewViewset,basename="mdishes")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotel/Menu',MenuItems.as_view()),
    path('hotel/Menu/<int:mid>',SpecificItems.as_view()),
    path('h/',include('hotel.urls')),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    


]+router.urls
