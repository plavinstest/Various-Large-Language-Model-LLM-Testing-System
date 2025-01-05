from django.urls import path
from . import views

# URL patterns for the LLM Chatting Application
urlpatterns = [
    # Home page where users interact with the app
    path("", views.index, name="index"),
    # Result page for viewing chat history
    path("result/", views.result, name="result"),
    # Endpoint for deleting a specific message/record from database
    path("delete_message/", views.delete_message, name="delete_message"),
]
