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
    path('asset-types/', views.AssetTypeListView.as_view(),
         name='asset_type_list'),
    path('asset-types-list/', views.get_asset_types,
         name='ajax_asset_type_list'),
    path('create-asset-type/', views.CreateAssetTypeView.as_view(),
         name="create_asset_type"),
    path('assets/', views.AssetListView.as_view(), name='asset_list'),
    path('assets-list/', views.get_assets, name='ajax_assets_list'),
    path('create-asset/', views.CreateAssetView.as_view(),
         name="create_asset"),
]
