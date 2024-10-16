from django.contrib import admin

from asset_admin.models import AssetType, Asset, AssetImage


# Register your models here.
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'name']


class AssetAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'code', 'name', 'is_active']


class AssetImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'asset', 'image']


admin.site.register(AssetType, AssetTypeAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetImage, AssetImageAdmin)