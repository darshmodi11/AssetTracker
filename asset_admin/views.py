from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from asset_admin.forms import LoginForm
from django.contrib.auth import authenticate, login


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
                messages.error(self.request, "User not found with the provided credentials.")
                return self.get(request, *args, **kwargs)
        else:
            form = {'form_error': form.errors}
            return self.get(request, **form)

class IndexView(LoginRequiredMixin, View):
    login_url = reverse_lazy("asset_admin:admin_login")

    def get(self, request, *args, **kwargs):

        return render(self.request,
        'asset_admin/index.html',
                      context={}
                      )
