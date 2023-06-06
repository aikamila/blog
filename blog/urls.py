from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/create/', views.PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/comment/', views.CommentCreate.as_view(), name='comment_create'),
    path('search/', views.PostSearch.as_view(), name='post_search'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('registration-success/', views.registration_success, name='registration_success'),
]