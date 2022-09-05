from django.urls import path
from . import views

urlpatterns=[

    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    path('stock/<str:pk>/', views.stock, name='stock'),
    path('config/', views.config, name='config'),
    path('monitored/', views.monitored, name='monitored'),
    path('monitored/<str:pk>/', views.monitored_stock, name='monitored_stock'),
]