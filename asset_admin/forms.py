import operator
from difflib import get_close_matches
from distutils.command.clean import clean
from functools import reduce

from django import forms
from django.db.models import Q
from asset_admin.models import AssetType, Asset


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100,
                            error_messages=
                            {'required': 'Please enter your email address.'}
                            )
    password = forms.CharField(widget=forms.PasswordInput(),
                               error_messages=
                               {'required': 'Please enter your password.'}
                               )
    remember_me = forms.BooleanField(required=False)


class CreateAssetTypeForm(forms.ModelForm):
    name = forms.CharField(max_length=50, error_messages={
        'required': 'Please enter the asset type',

    })
    description = forms.CharField(widget=forms.Textarea(), error_messages={
        'required': 'Please enter description of the asset type',
    })

    class Meta:
        model = AssetType
        fields = ['name', 'description']


class CreateAssetForm(forms.ModelForm):
    name = forms.CharField(max_length=50, error_messages={
        'required': 'Please enter the asset type',
    })
    asset_type = forms.ModelChoiceField(
        queryset=AssetType.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        error_messages={
            'required': 'Please choose an asset type',
        }

    )
    is_active = forms.BooleanField(required=False)
    class Meta:
        model = Asset
        fields = ['name', 'asset_type', 'is_active']


    def clean_name(self):
        cleaned_data = super(CreateAssetForm, self).clean()
        name = cleaned_data.get('name')
        splitted_name = name.split(' ')

        related_data = Asset.objects \
            .filter(
            Q(name__icontains=name) |
            reduce(operator.or_,
                   (
                       Q(name__icontains=text)
                       for text in splitted_name
                   )
                   )
        ).values_list('name', flat=True)

        if related_data.exists():

            similar_names = get_close_matches(name,
                                              related_data,
                                              n=3,
                                              cutoff=0.9)

            if similar_names:
                raise forms.ValidationError(
                    "Oops! it seems asset name is already present, please provide "
                    "another asset name")

        return name
