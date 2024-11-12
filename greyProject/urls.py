
from django.contrib import admin
from django.urls import path, include
# from oauth2_provider import urls as oauth2_urls 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("o/", include('oauth2_provider.urls', namespace='oauth2_provider')),
    path("", include("api.urls")),

]
