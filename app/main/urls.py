from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('fav', views.fav, name='fav'),
    path('logout', views.logout_view, name='logout'),
]