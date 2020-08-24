from django.urls import path
from . import views
app_name = 'blogapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('author/<name>', views.ProfileView.as_view(), name='profile'),
    path('single/<int:id>', views.SingleView.as_view(), name='single'),
    path('category/<name>', views.CategoryView.as_view(), name='category'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('create_new_post/', views.create_new_post_view, name='create_new_post'),
    path('article_auhtor_profile/', views.article_auhtor_profile_view, name='article_auhtor_profile'),
    path('update_post/<int:id>', views.update_post_view, name='update_post'),
    path('delete_post/<int:id>', views.delete_post_view, name='delete_post'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('topics/', views.TopicView.as_view(), name='topics'),
    path('create_new_topic/', views.create_new_topic_view, name='create_new_topic')

]
