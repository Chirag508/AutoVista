from django.urls import path
from . import views
urlpatterns = [
    path('',views.show_welcome_page,name='welcome'),
    path('home',views.show_home_page,name='home'),
    path('base',views.show_base_page,name='base'),
    path('about',views.show_about_page,name='about'),
    path('contact',views.show_contact_page,name='contact'),
    path('wallpaper/', views.wallpaper_list, name='wallpaper_list'),
    path('wallpaper/<int:id>/', views.wallpaper_detail, name='wallpaper_detail'),
    path('increment-download/<int:id>/', views.increment_download, name='increment_download'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('blog/', views.blog_list, name='blog_list'),
    path('<slug:slug>/', views.blog_detail_page, name='blog_detail'),
]