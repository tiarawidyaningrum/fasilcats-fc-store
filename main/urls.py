from django.urls import path
from . import views
from main.views import edit_product, delete_product

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),

    # routing untuk form dan detail
    path('create-product/', views.create_product, name='create_product'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    
    path('edit-product/<int:id>', edit_product, name='edit_product'),
    path('delete-product/<int:id>', delete_product, name='delete_product'),

    # routing untuk authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # routing 4 fungsi data delivery
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<int:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', views.show_json_by_id, name='show_json_by_id'),
]