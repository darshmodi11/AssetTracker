from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from asset_admin import views

app_name = 'asset_admin'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.AdminLogin.as_view(), name='admin_login'),
    path('logout/', LogoutView.as_view(
        next_page=reverse_lazy('asset_admin:admin_login')
    ),
         name='admin_logout'),

]
