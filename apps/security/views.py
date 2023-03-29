from apps.base.texts import dialogs, message_texts
from apps.base.decorators import AllowedUsers
from apps.base.utils import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import get_language, gettext_lazy as _
from django.views.generic import View

from .forms import *


class Error403(LoginRequiredMixin, View):
    login_url = 'security/login'
    template_name = 'security/error_403.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'list_url': '/%(lang)s/security/error_403/' % {'lang': get_language()},
            'title': _('403 Error'),
            'user_data': get_user_data(request)
        }

        return render(request, self.template_name, context)


# @unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home_base:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home:index')
            else:
                messages.error(request, _('The username or password is incorrect'))

        context = {
            'title': _('Login'),
        }

        return render(request, 'security/login.html', context)


# @login_required(login_url='login')
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='Representative')
            user.groups.add(group)

            messages.success(request, _('The %(username)s user account was created successfully') %
                             {'username': username})

            return redirect('login')

    context = {
        'title': _('Register'),
        'form': form
    }
    return render(request, 'security/register.html', context)


class ProfilePage(LoginRequiredMixin, View):
    login_url = 'security/login'
    model = User
    form_class_user = ProfileForm
    template_name = 'security/profile.html'

    def get(self, request, *args, **kwargs):
        try:
            item = self.model.objects.get(username=request.user)
            form_user = self.form_class_user(instance=item)
        except:
            item = None

        if item is None:
            form_user = self.form_class_user()

        # 'view_url': '/%(lang)s/security/profile/' % {'lang': get_language()},
        context = {
            'view_url': '/security/profile/',
            'list_url': '',
            'title': _('Profile'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'item': item,
            'form_user': form_user
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        item_user = self.model.objects.get(username=request.user)
        form_user = self.form_class_user(request.POST, request.FILES, instance=item_user)
        is_valid = form_user.is_valid()
        if is_valid:
            if not self.request.accepts('application/json'):
                messages.success(request, message_texts['success']['record_successfully_saved'])
                item_user = form_user.save(commit=False)
                # item_user.set_password(form_user.cleaned_data['password2'])
                item_user.save()

                form_user = self.form_class_user()
                context = {
                    'user_data': get_user_data(request),
                    'form_user': form_user,
                    'status': 'ok',
                    'messages_group': get_messages_group(request)
                }

                return redirect('security/profile')
                # return render(request, self.template_name, context)
            else:
                if request.POST.get('action', None) == 'save':
                    messages.success(request, message_texts['success']['record_successfully_saved'])
                    item_user = form_user.save(commit=False)
                    # item_user.set_password(form_user.cleaned_data['password2'])
                    item_user.save()

                context = {
                    'cleaned_data': list(form_user.cleaned_data),
                    'status': 'ok',
                    'messages_group': get_messages_group(request)
                }

                return JsonResponse(context)
        else:
            if not request.is_ajax():
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])
                context = {
                    'user_data': get_user_data(request),
                    'form_user': form_user,
                    'cleaned_data': list(form_user.cleaned_data),
                    'errors': form_user.errors.get_json_data(escape_html=False),
                    'status': 'ko',
                    'messages_group': get_messages_group(request)
                }

                return render(request, self.template_name, context)
            else:
                if request.POST.get('action', None) == 'save':
                    messages.error(request, message_texts['error']['error_validation_encountered'])
                    messages.info(request, message_texts['info']['check_data_entered'])

                context = {
                    'cleaned_data': list(form_user.cleaned_data),
                    'errors': form_user.errors.get_json_data(escape_html=False),
                    'status': 'ko',
                    'messages_group': get_messages_group(request)
                }

                return JsonResponse(context)


class PasswordReset(LoginRequiredMixin, View):
    login_url = 'security/login'
    model = User
    form_class_user = ResetearClaveForm
    template_name = 'security/password_reset.html'

    def get(self, request, *args, **kwargs):
        try:
            item = self.model.objects.get(username=request.user)
            form_user = self.form_class_user(instance=item)
        except:
            item = None

        if item is None:
            form_user = self.form_class_user()

        context = {
            'view_url': '/security/password_reset/',
            'list_url': '/%(lang)s/security/login/' % {'lang': get_language()},
            'title': _('Password reset'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'item': item,
            'form_user': form_user
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # messages_group = {}
        item_user = self.model.objects.get(username=request.user)
        form_user = self.form_class_user(request.POST, request.FILES, instance=item_user)
        is_valid = form_user.is_valid()
        if is_valid:
            if request.POST.get('action', None) == 'save':
                messages.success(request, _('Password successfully reset'))
                item_user = form_user.save(commit=False)
                item_user.set_password(form_user.cleaned_data['password2'])
                item_user.save()

            context = {
                'cleaned_data': list(form_user.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request)
            }

            # return redirect('security/logout')
            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])

            context = {
                'cleaned_data': list(form_user.cleaned_data),
                'errors': form_user.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


@login_required(login_url='security/login')
def logoutUser(request):
    logout(request)
    return redirect('security:login')


class ViewAudit(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator']
    login_url = 'security/login'
    model = Audit
    template_name = 'security/view_audit.html'
    items = None

    def get(self, request, *args, **kwargs):
        self.items = self.model.objects.filter(active=True)
        data_list = []
        for i in self.items:
            item = i.to_json()
            data_list.append(item)

        context = {
            'view_url': '/security/view_audit/',
            'list_url': '/%(lang)s/security/view_audit/' % {'lang': get_language()},
            'title': _('Audit'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': data_list
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        column_order = request.POST.get('order[0][column]')
        column_name = request.POST.get('columns[0][data]'.replace('0', column_order))
        if request.POST.get('order[0][dir]') == 'desc':
            column_name = '-' + column_name

        initial_date = request.POST.get('initial_date', None)
        final_date = request.POST.get('final_date', None)

        search = request.POST.get('search[value]')
        if search:
            self.items = self.model.objects.filter(
                active=True,
                date_time__date__range=[initial_date, final_date]
            ).filter(
                Q(user__username__icontains=search) |
                Q(access__icontains=search) |
                Q(comment__icontains=search)
            ).distinct().order_by(column_name)
        else:
            self.items = self.model.objects.filter(
                active=True,
                date_time__date__range=[initial_date, final_date]
            ).order_by(column_name)

        data_list = []
        for i in self.items:
            item = i.convertir_JSON()
            data_list.append(item)

        data = get_data_table_page(request, data_list)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data, safe=False)
