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
    #add manufactuer products
    path('manufacturer_product',views.manufacturer_product,name='manufacturer_product'),
    path('add_product_manufacturer',views.add_product_manufacturer,name='add_product_manufacturer'),
    path('edit_product_manufacturer/<int:product_id>/',views.edit_product_manufacturer,name='edit_product_manufacturer'),
    path('delete_product_manufacturer/<int:product_id>/', views.delete_product_manufacturer, name='delete_product_manufacturer'),
    #see orders for my products
    path('all_manu_orders',views.all_manu_orders,name='all_manu_orders'),
    path('manu_order_details/<int:order_id>/',views.manu_order_details,name='manu_order_details'),
    #alerts
    path('alerts/<int:product_id>/',views.alerts,name='alerts'),
    path('delete_alerts/<int:product_id>/',views.delete_alerts,name='delete_alerts'),
    #storing rating
    path('store_rating/<int:order_id>/', views.store_rating, name='store_rating'),

    #retailer
    path('retailer_home',views.retailer_home,name='retailer_home'),
    path('retailer_profile',views.retailer_profile,name='retailer_profile'),
    #placing orders(adding to cart)
    path('order_raw_goods',views.order_raw_goods,name='order_raw_goods'),
    path('order_products',views.order_products,name='order_products'),
    path('search_supplier_for_retailer',views.search_supplier_for_retailer,name='search_supplier_for_retailer'),
    #cart to order
    path('orders_retailer', views.orders_retailer, name='orders_retailer'),
    path('remove_from_cart_retailer/<int:order_id>/', views.remove_from_cart_retailer, name='remove_from_cart_retailer'),
    path('transfer_to_record_db_retailer', views.transfer_to_record_db_retailer, name='transfer_to_record_db_retailer'),
    path('customer_cancel_retailer/<int:order_id>/', views.customer_cancel_retailer, name='customer_cancel_retailer'),
    path('purchase_orders_retailer', views.purchase_orders_retailer, name='purchase_orders_retailer'),
    path('search_manufacturer_for_retailer',views.search_manufacturer_for_retailer,name='search_manufacturer_for_retailer'),
    #order manufactureres products from retailer 
    path('add_products_to_cart', views.add_products_to_cart, name='add_products_to_cart'),
    path('remove_prod_from_cart_retailer/<int:order_id>/', views.remove_prod_from_cart_retailer, name='remove_prod_from_cart_retailer'),
    path('prod_transfer_to_record_db_retailer', views.prod_transfer_to_record_db_retailer, name='prod_transfer_to_record_db_retailer'),
    path('manu_customer_cancel_retailer/<int:order_id>/', views.manu_customer_cancel_retailer, name='manu_customer_cancel_retailer'),
    path('manu_purchase_orders_retailer', views.manu_purchase_orders_retailer, name='manu_purchase_orders_retailer'),
    #storing rating 
    path('store_rating_retailer/<int:order_id>/', views.store_rating_retailer, name='store_rating_retailer'),
    path('manu_store_rating_retailer/<int:order_id>/', views.manu_store_rating_retailer, name='manu_store_rating_retailer'),
   
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