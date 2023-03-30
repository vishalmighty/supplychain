from django.urls import path,include
from  home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('rolls',views.rolls,name='rolls'),

    #supplier
    path('supplier_home',views.supplier_home,name='supplier_home'),
    path('supplier_profile',views.supplier_profile,name='supplier_profile'),
    path('add_product_supplier',views.add_product_supplier,name='add_product_supplier'),
    path('edit_product_supplier/<int:product_id>/',views.edit_product_supplier,name='edit_product_supplier'),
    path('delete_product_supplier/<int:product_id>/', views.delete_product_supplier, name='delete_product_supplier'),
    path('all_orders',views.all_orders,name='all_orders'),
    path('order_details/<int:order_id>/',views.order_details,name='order_details'),

    #manufacturer
    path('manufacturer_home',views.manufacturer_home,name='manufacturer_home'),
    path('search_supplier',views.search_supplier,name='search_supplier'),
    path('manufacturer_profile',views.manufacturer_profile,name='manufacturer_profile'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('orders', views.order_list, name='order_list'),
    path('transfer_to_record_db', views.transfer_to_record_db, name='transfer_to_record_db'),
    path('customer_cancel/<int:order_id>/', views.customer_cancel, name='customer_cancel'),
    path('purchase_orders', views.purchase_orders, name='purchase_orders'),
    path('remove_from_cart/<int:order_id>/', views.remove_from_cart, name='remove_from_cart'),

    #retailer
    path('retailer_home',views.retailer_home,name='retailer_home'),
    path('retailer_profile',views.retailer_profile,name='retailer_profile'),


   
    path('user_logout',views.user_logout,name='user_logout'),
    path('user_signup',views.user_signup,name='user_signup'),
    path('user_login',views.user_login,name='user_login'),

     path('supplier_admin',views.supplier_admin,name='admin_home'),
     path('manufacturer_admin',views.manufacturer_admin,name='manufacturer_admin'),
     path('retailer_admin',views.retailer_admin,name='retailer_admin'),
     path('supplier_details/<int:supplier_id>/',views.supplier_details,name='supplier_details'),
     path('manufacturer_details/<int:supplier_id>/',views.manufacturer_details,name='manufacturer_details'),
     path('retailer_details/<int:supplier_id>/',views.retailer_details,name='retailer_details'),
]