from django.urls import path,include
from  home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('rolls',views.rolls,name='rolls'),
    path('supplier_home',views.supplier_home,name='supplier_home'),
    path('manufacturer_home',views.manufacturer_home,name='manufacturer_home'),
    path('retailer_home',views.retailer_home,name='retailer_home'),



   
    path('user_logout',views.user_logout,name='user_logout'),
    path('user_signup',views.user_signup,name='user_signup'),
    path('user_login',views.user_login,name='user_login'),

     path('admin_home',views.admin_home,name='admin_home'),
]