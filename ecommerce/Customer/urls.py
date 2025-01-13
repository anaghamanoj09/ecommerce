from django.urls import path,include
from Customer import views
urlpatterns = [
    path('customer_home',views.customer_home,name='customer_home'),
    path('customer_logout',views.customer_logout,name='customer_logout'),
    path('product_details/<int:id>',views.product_details,name='product_details'),
    path('add_tocart/<int:id>',views.add_tocart,name='add_tocart'),
    path('view_cart',views.view_cart,name='view_cart'),
    path('less_quantity/<int:id>',views.less_quantity,name='less_quantity'),
    path('add_count/<int:id>',views.add_count,name='add_count'),
    path('delete_cart/<int:id>',views.delete_cart,name='delete_cart'),
    path('summary',views.summary,name='summary'),
    path('place_order',views.place_order,name='place_order'),
    path('success/', views.SuccessView.as_view(), name="success"),    
    path('cancelled/', views.CancelledView.as_view(),name="cancelled"), 
    path('order_manage',views.order_manage,name='order_manage'),
    path('details',views.details,name='details'),
    path('status_details/<int:id>',views.status_details,name='status_details'),
    path('cancel/<int:id>',views.cancel,name='cancel'),
    path('change_psswd',views.change_psswd,name='change_psswd'),
    path('my_account',views.my_account,name='my_account'),
]
