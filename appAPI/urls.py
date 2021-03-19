from django.urls import path
from appAPI import views

urlpatterns = [
    path('articles/', views.articles_list, name='articles_list'),
    path('articles/<int:pk>/', views.articles_detail, name='articles_detail'),
    path('shelfs/', views.shelves_list, name='shelfs_list'),
    path('shelfs/<int:row>/', views.shelves_by_row, name='shelfs_by_row'),
    path('shelfs/<int:row>/<int:bay>/', views.shelves_detail, name='shelfs_by_row_bay'),
    path('warehouse/', views.warehouse_list, name='warehouse_list_articles'),


]
