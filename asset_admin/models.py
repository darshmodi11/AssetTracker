import uuid

from django.db import models


def get_uuid_digits():
    return str(uuid.uuid4().int)[:16]

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class AssetType(TimestampModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Asset Types'

    def __str__(self):
        return self.name


class Asset(TimestampModel):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(verbose_name="Asset Code",
                            max_length=16,
                            unique=True,
                            default=get_uuid_digits,
                            editable=False)
    asset_type = models.ForeignKey(AssetType,
                                   on_delete=models.CASCADE,
                                   related_name='assets')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AssetImage(TimestampModel):
    image = models.ImageField(upload_to='images/asset_images/%Y/%m/%d')
    asset = models.ForeignKey(Asset,
                              on_delete=models.CASCADE,
                              related_name='asset_images')

    class Meta:
        verbose_name_plural = 'Asset Images'

    def __str__(self):
        return str(self.pk)
