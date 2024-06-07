from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # CRUD operation urls
    path('create/', views.create, name='create'),
    path('delete/<int:tid>/', views.delete, name='delete'),
    path('update/<int:tid>/', views.update, name='update'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
