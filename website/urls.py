from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('add-client/', views.add_client, name='add-client'),
    path('client/<int:id>', views.view_client, name='client'),
    path('edit-client/<int:id>', views.edit_client, name='edit-client'),
    path('delete-client/<int:id>', views.delete_client, name='delete-client'),
    path('clients/', views.view_clients, name='clients')
]
