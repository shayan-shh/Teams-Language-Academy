
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('about/',views.about, name="about"),
    path('my_course/', views.my_course, name="my_course"),
    path('course/<int:ck>', views.course, name="course"),
    path('courses/', views.courses, name="courses"),
    path('category/<str:cat>', views.category, name="category"),
    path('category_summary/', views.category_summary, name="category_summary"),
    path('search/', views.search, name="search"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('signup/', views.signup_user, name="signup"),
    path('update_user/', views.update_user, name="update_user"),
    path('update_info/', views.update_info, name="update_info"),
    path('update_password/', views.update_password, name="update_password"),
    path('add_course/', views.add_course, name="add_course"),
    path('edit_course/<int:pk>', views.edit_course, name="edit_course"),
    path('delete_course/<int:pk>', views.delete_course, name="delete_course"),
    path('add_category/', views.add_category, name="add_category"),
    path('edit-category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    
]
