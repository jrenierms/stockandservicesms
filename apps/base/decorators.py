from django.contrib.auth.mixins import *
from django.http import HttpResponse
from django.shortcuts import redirect


class AllowedUsers(UserPassesTestMixin):
    login_url = 'login'

    def test_func(self):
        group = None
        if self.request.user.groups.exists():
            group = self.request.user.groups.all()[0].name
        return group in self.allowed_roles

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            return redirect('security:error_403')
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_base:index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func()


def allowed_users_old(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You do not have permission to see this page')
        return wrapper_func()
    return decorator()
