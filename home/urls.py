from django.urls import path,include
from  home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('rolls',views.rolls,name='rolls'),
    path('supplier_home',views.supplier_home,name='supplier_home'),
    path('manufacturer_home',views.manufacturer_home,name='manufacturer_home'),
    path('retailer_home',views.retailer_home,name='retailer_home'),



    path('admin_home',views.admin_home,name='admin_home'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('admin_signup',views.admin_signup,name='admin_signup'),
    path('admin_login',views.admin_login,name='admin_login'),
]