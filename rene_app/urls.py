from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('home', views.home),
    path('logout', views.logout),
    path('post_question', views.post),
    path('question/<int:q_id>', views.question),
    path('question_attempt/<int:q_id>', views.attempts),
    path('solution/<int:sol_id>', views.solutions),
]