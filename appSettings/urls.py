from django.urls import path
from .views import SettingsView, homepage

urlpatterns = [
    path('test', SettingsView.as_view()),
    path('create-new-settings/', SettingsView.as_view()),
    path('home', homepage)
]