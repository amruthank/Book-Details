from django.urls import path, re_path

from . import views

urlpatterns = [
        path('external-books/', views.external_books, name='external_books'),
        path('v1/books/', views.create_read_method, name='create_read_method'),
        re_path(r'v1/books/(?P<book_id>\d+)/$', views.update, name='update'), #(?P<book_id>\d+)$
        re_path(r'v1/books/(?P<book_id>\d+)/delete', views.delete, name='delete'),

    ]
