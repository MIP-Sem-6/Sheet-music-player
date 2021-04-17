from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('fav', views.fav, name='fav'),
    path('audio/<int:id>', views.audio, name='audio'),
    path('logout', views.logout_view, name='logout'),
    path('add_song', views.add_song, name='add_song'),
    path('my_songs', views.my_songs, name='my_songs'),
    path('tag/<str:name>', views.tag, name='tag'),
    path('download/<str:notes>', views.download, name='download'),
    path('update_song/<int:id>', views.update_song, name='update_song'),
    path('account', views.profile, name='account'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('view_profile/<int:id>', views.view_profile, name='view_profile'),
]