from django.urls import path
from .views import recommend_songs, index

urlpatterns = [
    path('recommend_songs', recommend_songs, name='recommend-songs'),
    path('', index, name='index')
    # Add more paths as needed
]