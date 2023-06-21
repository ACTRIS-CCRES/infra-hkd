from django.urls import path
from users.api.views import UserList, UserMe

# API URLS
urlpatterns = [
    path("api/v1/users/", UserList.as_view()),
    path("api/v1/users/me", UserMe.as_view()),
]
