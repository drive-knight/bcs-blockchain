from django.urls import path
from .views import tx_list, detail_description, add_description, user_login, user_logout

urlpatterns = [
    path('', tx_list, name='home'),
    path('admin-dash/', add_description, name='admin'),
    path('tx/<str:txid>/', detail_description, name='tx-detail'),
    path('accounts/login/', user_login, name='login'),
    path('accounts/logout/', user_logout, name='logout'),
]