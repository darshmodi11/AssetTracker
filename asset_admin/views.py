from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, TemplateView, \
    UpdateView

from asset_admin.forms import LoginForm, CreateAssetTypeForm, CreateAssetForm, \
    AssetImageFormset
from asset_admin.models import AssetType, Asset, AssetImage


# Create your views here.
class AdminLogin(View):
    def get(self, request, *args, **kwargs):

        return render(self.request,
                      'asset_admin/login.html',
                      context={'form_errors': kwargs.get('form_error')}
                      )

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect(to='asset_admin:index')
            else:
                messages.error(self.request,
                               "User not found with the provided "
                               "credentials.")
                return self.get(request, *args, **kwargs)
        else:
            form = {'form_error': form.errors}
            return self.get(request, **form)


class IndexView(LoginRequiredMixin, View):
    login_url = reverse_lazy("asset_admin:admin_login")

    def get(self, request, *args, **kwargs):
        assets_count_by_type = AssetType.objects.annotate(
            asset_count=Count('assets')).values_list('asset_count', flat=True)
        assets_type_name = AssetType.objects.annotate(
            asset_count=Count('assets')).values_list('name', flat=True)
        total_assets = Asset.objects.count()
        active_assets = Asset.objects.filter(is_active=True).count()
        inactive_assets = total_assets - active_assets

        return render(self.request,
                      'asset_admin/index.html',
                      context={'asset_types': list(assets_type_name),
                               'assets_count': list(assets_count_by_type),
                               'active_assets': active_assets,
                               'inactive_assets': inactive_assets
                               }
                      )


class AssetTypeListView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("asset_admin:admin_login")
    template_name = 'asset_admin/asset_type_list.html'


def get_asset_types(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        draw = int(request.GET.get('draw'))

        search_string = request.GET.get('search[value]')
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get("length", 10))
        queryset = AssetType.objects.filter(
            Q(name__icontains=search_string) |
            Q(description__icontains=search_string)
        ).order_by('-created_at').values('id', 'name', 'description')
        paginator = Paginator(queryset, length)
        page_number = (start // length) + 1
        page_obj = paginator.get_page(page_number)

        return JsonResponse(status=200,
                            data={
                                "success": True,
                                "data": list(page_obj),
                                "serial_number": page_obj.start_index(),
                                "start": start,
                                "draw": draw,
                                "recordsTotal": paginator.count,
                                "recordsFiltered": paginator.count,
                            })
    else:
        return JsonResponse(status=400,
                            data={
                                "success": False,
                                "message": "Invalid request received."
                            })


class CreateAssetTypeView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("asset_admin:admin_login")
    form_class = CreateAssetTypeForm
    template_name = 'asset_admin/create_asset_type.html'
    success_url = reverse_lazy("asset_admin:asset_type_list")

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class AssetListView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("asset_admin:admin_login")
    template_name = 'asset_admin/asset_list.html'


def get_assets(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        draw = int(request.GET.get('draw'))

        search_string = request.GET.get('search[value]')
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get("length", 10))
        queryset = (
            Asset.objects.filter(
                Q(name__icontains=search_string) |
                Q(code__icontains=search_string) |
                Q(asset_type__name__icontains=search_string)
            ).select_related('asset_type')
            .order_by('-created_at')
            .values('id', 'name', 'code', 'asset_type__name')
        )

        paginator = Paginator(queryset, length)
        page_number = (start // length) + 1
        page_obj = paginator.get_page(page_number)

        return JsonResponse(status=200,
                            data={
                                "success": True,
                                "data": list(page_obj),
                                "serial_number": page_obj.start_index(),
                                "start": start,
                                "draw": draw,
                                "recordsTotal": paginator.count,
                                "recordsFiltered": paginator.count,
                            })
    else:
        return JsonResponse(status=400,
                            data={
                                "success": False,
                                "message": "Invalid request received."
                            })


class CreateAssetView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("asset_admin:admin_login")
    form_class = CreateAssetForm
    template_name = 'asset_admin/create_new_asset.html'
    success_url = reverse_lazy("asset_admin:asset_list")

    def get(self, request, *args, **kwargs):
        formset = AssetImageFormset(prefix="asset_image",
                                    queryset=AssetImage.objects.none())
        return render(request,
                      self.template_name,
                      context={
                          "image_formset": formset,
                          "form": self.form_class,
                      })

    def post(self, request, *args, **kwargs):
        formset = AssetImageFormset(self.request.POST,
                                    files=self.request.FILES,
                                    prefix="asset_image"
                                    )
        form = CreateAssetForm(request.POST)

        import pdb;
        pdb.set_trace()

    def form_invalid(self, form):
        return super().form_invalid(form)


def get_asset_type_detail(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        asset_type = AssetType.objects.filter(pk=pk).values().first()
        return JsonResponse(status=200,
                            data={
                                "success": True,
                                "data": asset_type
                            }
                            )
    else:
        return JsonResponse(status=400,
                            data={
                                "success": False,
                                "message": "Invalid request received."
                            })


def delete_asset_type(request, pk):
    if (request.headers.get('x-requested-with') == 'XMLHttpRequest'
            and request.method == 'POST'):
        try:
            AssetType.objects.get(pk=pk).delete()

            return JsonResponse(status=200,
                                data={
                                    "success": True,
                                    "message": "Asset type deleted successfully."
                                })

        except AssetType.DoesNotExist:
            return JsonResponse(status=404,
                                data={
                                    "success": False,
                                    "message": "Asset type does not exist."
                                })


class AssetTypeUpdateView(UpdateView):
    form_class = CreateAssetTypeForm
    model = AssetType
    success_url = reverse_lazy('asset_admin:asset_type_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True,
                                 'message': 'Asset type updated successfully!'})
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        return response
