from django.urls import path
from .views import *


app_name = 'landing'

urlpatterns = [
    path('contact_us/', contact_us, name='contact_us'),
    path('', HomeView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('access_denied/', AccessDenied.as_view(), name='access_denied'),

]
