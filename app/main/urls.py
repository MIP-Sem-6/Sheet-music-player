from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('fav', views.fav, name='fav'),
    path('logout', views.logout_view, name='logout'),
    path('add_song', views.add_song, name='add_song'),
    path('my_songs', views.my_songs, name='my_songs'),
    path('update_song/<int:id>', views.update_song, name='update_song'),
]