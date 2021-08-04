from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("create_user", views.create_user),
    path("home", views.home),
    path('logout', views.logout),
    path('profile', views.profile),
    path('profile/<int:id>/edit', views.edit_user),
    path('profile/<int:id>/delete', views.delete_user),
    path('user/<int:id>', views.user),
    path('reviews', views.reviews),
    path('retailer/<int:id>', views.retailer),
    path('add_retailer', views.add_retailer),
    path('create_retailer', views.create_retailer),
    path('retailer/<int:id>/add_review', views.create_review1),
    path('retailer/all', views.retailers),
    path('review/<int:id>/like1', views.like1),
    path('review/<int:id>/like2', views.like2),
    path('review/<int:id>/like3', views.like3),
    path('review/<int:id>/like4', views.like4),
    path('add_review', views.add_review),
    path('create_review2', views.create_review2)
]
