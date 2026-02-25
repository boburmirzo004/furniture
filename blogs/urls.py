from django.urls import path

from blogs.views import blog_detail_page_view, blog_list_page_view

app_name='blogs'

urlpatterns =[
    path('<int:pk>/', blog_detail_page_view, name='detail'),
    path('', blog_list_page_view, name='list'),
]