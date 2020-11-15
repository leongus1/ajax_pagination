from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), 
    path('success', views.success),
    path('register', views. register),
    path('login', views.check_login),
    path('logout', views.logout),
    path('users/<int:user_id>/', views.user_details),
    path('user/<int:user_id>/edit/', views.user_edit),
    path('user/<int:user_id>/update/', views.update),
    path('user/search', views.search),
    path('user/page/<int:page_no>/', views.page),
]