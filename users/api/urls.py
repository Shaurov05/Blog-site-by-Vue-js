from django.urls import path
from users.api.views import *


urlpatterns = [
    path("user/", CurrentUserAPIView.as_view(), name='current-user'),

]


#
