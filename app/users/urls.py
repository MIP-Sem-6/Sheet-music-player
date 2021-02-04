from django.urls import path


from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('register/<int:id>/<int:tab>', views.register, name='register'),
    path('error', views.errorpage, name='errorpage')
]