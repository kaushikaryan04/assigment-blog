from django.urls import path
from . import views

urlpatterns = [
    path("" , views.home ,name = "home"),
    path("post/<str:slug>" , views.postdetail , name = "post_detail"),
    path('post/new/', views.post_create_view, name='post_create'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('search/', views.search, name='search'),

]
