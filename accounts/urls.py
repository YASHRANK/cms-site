from django.urls import path
from accounts import views

urlpatterns = [

    path('register/',views.register, name='register'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
    
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customers/<str:pk>/', views.customers, name='customers'),

    path('create_customer/', views.create_customer, name='create_customer'),

    path('create_order/<str:pk>', views.create_order, name='create_order'),
    path('update_order/<str:pk>', views.update_order, name='update_order'),
    path('delete_order/<str:pk>', views.delete_order, name='delete_order'),
    
    path('user/', views.user_page, name='user_page'),
    path('account_settings/', views.account_settings, name='account_settings'),

]
