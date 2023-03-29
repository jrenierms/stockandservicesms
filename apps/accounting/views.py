import os
from io import BytesIO

from apps.base.decorators import AllowedUsers
from apps.base.models import Setting
from apps.base.texts import dialogs, message_texts
from apps.base.utils import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import get_language, gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from stockandservicesms.settings import MEDIA_ROOT, MEDIA_URL
from xhtml2pdf import pisa

from .forms import *


class ListStore(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Store
    template_name = 'accounting/list_store.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/accounting/list_store/',
            'list_url': '/%(lang)s/accounting/list_store/' % {'lang': get_language()},
            'create_url': '/%(lang)s/accounting/create_store/' % {'lang': get_language()},
            'edit_url': '/%(lang)s/accounting/edit_store/' % {'lang': get_language()},
            'delete_url': '/%(lang)s/accounting/delete_store/' % {'lang': get_language()},
            'title': _('List of stores'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(active=True).values('id', 'code', 'description'))
        }

        event_log(User.objects.get(username=request.user).id, 2, self.__str__().split(' ')[0].split('<')[1])

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        column_order = request.POST.get('order[0][column]')
        column_name = request.POST.get('columns[0][data]'.replace('0', column_order))
        if request.POST.get('order[0][dir]') == 'desc':
            column_name = '-' + column_name

        search = request.POST.get('search[value]')
        if search:
            self.items = list(self.model.objects.filter(active=True).filter(
                Q(code__icontains=search) |
                Q(description__icontains=search)
            ).distinct().order_by(column_name).values('id', 'code', 'description'))
        else:
            self.items = list(self.model.objects.filter(active=True).order_by(column_name).
                              values('id', 'code', 'description'))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreateStore(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Store
    form_class = StoreForm
    template_name = 'accounting/create_store.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/accounting/create_store/',
            'list_url': '/%(lang)s/accounting/list_store/' % {'lang': get_language()},
            'title': _('New store'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save()
                messages.success(request, message_texts['success']['record_successfully_saved'])
                event_log(User.objects.get(username=request.user).id, 1,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description)
            context = {
                'cleaned_data': list(form.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'errors': form.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


class EditStore(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Store
    form_class = StoreForm
    template_name = 'accounting/create_store.html'

    def get(self, request, pk=None, *args, **kwargs):
        try:
            item = self.model.objects.get(id=pk)
            form = self.form_class(instance=item)
        except:
            item = None

        if item is None:
            form = self.form_class()

        context = {
            'view_url': '/accounting/edit_store/' + str(item.id) + '/',
            'list_url': '/%(lang)s/accounting/list_store/' % {'lang': get_language()},
            'title': _('Edit store'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'item': item,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, pk=None, *args, **kwargs):
        item = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=item)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save()
                messages.success(request, message_texts['success']['record_successfully_saved'])
                event_log(User.objects.get(username=request.user).id, 3,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description)
            context = {
                'cleaned_data': list(form.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])
            context = {
                'cleaned_data': list(form.cleaned_data),
                'errors': form.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


class DeleteStore(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Store

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('id', None)
        try:
            item = self.model.objects.get(id=pk)
        except:
            item = None

        if item is None:
            messages.error(request, message_texts['error']['record_deletion_failed'])
            messages.info(request, message_texts['info']['record_not_found'])
            context = {
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }
        else:
            item_exist = Area.objects.filter(active=True, store=item).exists()
            if item_exist:
                messages.error(request, message_texts['error']['record_deletion_failed'])
                messages.info(request, message_texts['info']['record_deletion_related'])
                context = {
                    'status': 'ko',
                    'messages_group': get_messages_group(request)
                }
            else:
                item.active = False
                item.save()
                messages.success(request, message_texts['success']['record_successfully_deleted'])
                event_log(User.objects.get(username=request.user).id, 4,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description)
                context = {
                    'status': 'ok',
                    'messages_group': get_messages_group(request)
                }

        return JsonResponse(context)


class ListArea(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'accounting/login'
    model = Area
    template_name = 'accounting/list_area.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/accounting/list_area/',
            'list_url': '/%(lang)s/accounting/list_area/' % {'lang': get_language()},
            'create_url': '/%(lang)s/accounting/create_area/' % {'lang': get_language()},
            'edit_url': '/%(lang)s/accounting/edit_area/' % {'lang': get_language()},
            'delete_url': '/%(lang)s/accounting/delete_area/' % {'lang': get_language()},
            'title': _('List of areas'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(active=True).values(
                'id', 'code', 'description', 'store__description'))
        }

        event_log(User.objects.get(username=request.user).id, 2, self.__str__().split(' ')[0].split('<')[1])

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        column_order = request.POST.get('order[0][column]')
        column_name = request.POST.get('columns[0][data]'.replace('0', column_order))
        if request.POST.get('order[0][dir]') == 'desc':
            column_name = '-' + column_name

        search = request.POST.get('search[value]')
        if search:
            self.items = list(self.model.objects.filter(active=True).filter(
                Q(code__icontains=search) |
                Q(description__icontains=search) |
                Q(store__description__icontains=search)
            ).distinct().order_by(column_name).values('id', 'code', 'description', 'store__description'))
        else:
            self.items = list(self.model.objects.filter(active=True).order_by(column_name).
                              values('id', 'code', 'description', 'store__description'))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreateArea(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Area
    form_class = AreaForm
    template_name = 'accounting/create_area.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/accounting/create_area/',
            'list_url': '/%(lang)s/accounting/list_area/' % {'lang': get_language()},
            'title': _('New area'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'search_store':
            search = request.POST.get('q', None)

            data = get_store(search)

            return JsonResponse(data, safe=False)

        form = self.form_class(request.POST)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save(commit=False)
                item.store = get_object_or_404(Store, id=request.POST.get('store'))
                item.save()
                messages.success(request, message_texts['success']['record_successfully_saved'])
                event_log(User.objects.get(username=request.user).id, 1,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description + ' | store: ' + item.store.description)
            context = {
                'cleaned_data': list(form.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'errors': form.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


class EditArea(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Area
    form_class = AreaForm
    template_name = 'accounting/create_area.html'

    def get(self, request, pk=None, *args, **kwargs):
        try:
            item = self.model.objects.get(id=pk)
            form = self.form_class(instance=item)
        except:
            item = None

        if item is None:
            form = self.form_class()

        context = {
            'view_url': '/accounting/edit_area/' + str(item.id) + '/',
            'list_url': '/%(lang)s/accounting/list_area/' % {'lang': get_language()},
            'title': _('Edit area'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'item': item,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, pk=None, *args, **kwargs):
        if request.POST.get('action', None) == 'search_store':
            search = request.POST.get('q', None)

            data = get_store(search)

            return JsonResponse(data, safe=False)

        item = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=item)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save(commit=False)
                item.store = get_object_or_404(Store, id=request.POST.get('store'))
                item.save()
                messages.success(request, message_texts['success']['record_successfully_saved'])
                event_log(User.objects.get(username=request.user).id, 3,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description + ' | store: ' + item.store.description)
            context = {
                'cleaned_data': list(form.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])
            context = {
                'cleaned_data': list(form.cleaned_data),
                'errors': form.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


class DeleteArea(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Area

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('id', None)
        try:
            item = self.model.objects.get(id=pk)
        except:
            item = None

        if item is None:
            messages.error(request, message_texts['error']['record_deletion_failed'])
            messages.info(request, message_texts['info']['record_not_found'])
            context = {
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }
        else:
            item_exist = Location.objects.filter(active=True, area=item).exists()
            if item_exist:
                messages.error(request, message_texts['error']['record_deletion_failed'])
                messages.info(request, message_texts['info']['record_deletion_related'])
                context = {
                    'status': 'ko',
                    'messages_group': get_messages_group(request)
                }
            else:
                item.active = False
                item.save()
                messages.success(request, message_texts['success']['record_successfully_deleted'])
                event_log(User.objects.get(username=request.user).id, 4,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description + ' | store: ' + item.store.description)
                context = {
                    'status': 'ok',
                    'messages_group': get_messages_group(request)
                }

        return JsonResponse(context)


class ListLocation(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Location
    template_name = 'accounting/list_location.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/accounting/list_location/',
            'list_url': '/%(lang)s/accounting/list_location/' % {'lang': get_language()},
            'create_url': '/%(lang)s/accounting/create_location/' % {'lang': get_language()},
            'edit_url': '/%(lang)s/accounting/edit_location/' % {'lang': get_language()},
            'delete_url': '/%(lang)s/accounting/delete_location/' % {'lang': get_language()},
            'title': _('List of locations'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(active=True).values(
                'id', 'code', 'description', 'area__description', 'area__store__description'))
        }

        event_log(User.objects.get(username=request.user).id, 2, self.__str__().split(' ')[0].split('<')[1])

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        column_order = request.POST.get('order[0][column]')
        column_name = request.POST.get('columns[0][data]'.replace('0', column_order))
        if request.POST.get('order[0][dir]') == 'desc':
            column_name = '-' + column_name

        search = request.POST.get('search[value]')
        if search:
            self.items = list(self.model.objects.filter(active=True).filter(
                Q(code__icontains=search) |
                Q(description__icontains=search) |
                Q(area__description__icontains=search) |
                Q(area__store__description__icontains=search)
            ).distinct().order_by(column_name).values('id', 'code', 'description', 'area__description',
                                                      'area__store__description'))
        else:
            self.items = list(self.model.objects.filter(active=True).order_by(column_name).
                              values('id', 'code', 'description', 'area__description', 'area__store__description'))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreateLocation(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Location
    form_class = LocationForm
    template_name = 'accounting/create_location.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/accounting/create_location/',
            'list_url': '/%(lang)s/accounting/list_location/' % {'lang': get_language()},
            'title': _('New location'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'search_store':
            search = request.POST.get('q', None)

            data = get_store(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_area':
            search = request.POST.get('q', None)
            store = request.POST.get('store', None)

            data = get_area(search, store)

            return JsonResponse(data, safe=False)

        form = self.form_class(request.POST)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save(commit=False)
                item.area = get_object_or_404(Area, id=request.POST.get('area'))
                item.save()
                messages.success(request, message_texts['success']['record_successfully_saved'])
                event_log(User.objects.get(username=request.user).id, 1,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description + ' | area: ' + item.area.description +
                          ' | store: ' + item.area.store.description)
            context = {
                'cleaned_data': list(form.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'errors': form.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


class EditLocation(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Location
    form_class = LocationForm
    template_name = 'accounting/create_location.html'

    def get(self, request, pk=None, *args, **kwargs):
        try:
            item = self.model.objects.get(id=pk)
            form = self.form_class(initial={'store': item.area.store}, instance=item)
        except:
            item = None

        if item is None:
            form = self.form_class()

        context = {
            'view_url': '/accounting/edit_location/' + str(item.id) + '/',
            'list_url': '/%(lang)s/accounting/list_location/' % {'lang': get_language()},
            'title': _('Edit location'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'item': item,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, pk=None, *args, **kwargs):
        if request.POST.get('action', None) == 'search_store':
            search = request.POST.get('q', None)

            data = get_store(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_area':
            search = request.POST.get('q', None)
            store = request.POST.get('store', None)

            data = get_area(search, store)

            return JsonResponse(data, safe=False)

        item = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=item)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save(commit=False)
                item.area = get_object_or_404(Area, id=request.POST.get('area'))
                item.save()
                messages.success(request, message_texts['success']['record_successfully_saved'])
                event_log(User.objects.get(username=request.user).id, 3,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description + ' | area: ' + item.area.description +
                          ' | store: ' + item.area.store.description)
            context = {
                'cleaned_data': list(form.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])
            context = {
                'cleaned_data': list(form.cleaned_data),
                'errors': form.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


class DeleteLocation(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Location

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('id', None)
        try:
            item = self.model.objects.get(id=pk)
        except:
            item = None

        if item is None:
            messages.error(request, message_texts['error']['record_deletion_failed'])
            messages.info(request, message_texts['info']['record_not_found'])
            context = {
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }
        else:
            item_exist = Product.objects.filter(active=True, family=item).exists()
            if item_exist:
                messages.error(request, message_texts['error']['record_deletion_failed'])
                messages.info(request, message_texts['info']['record_deletion_related'])
                context = {
                    'status': 'ko',
                    'messages_group': get_messages_group(request)
                }
            else:
                item.active = False
                item.save()
                messages.success(request, message_texts['success']['record_successfully_deleted'])
                event_log(User.objects.get(username=request.user).id, 4,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description + ' | area: ' + item.area.description +
                          ' | store: ' + item.area.store.description)
                context = {
                    'status': 'ok',
                    'messages_group': get_messages_group(request)
                }

        return JsonResponse(context)


class ListPurchase(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    template_name = 'accounting/list_purchase.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/accounting/list_purchase/',
            'list_url': '/%(lang)s/accounting/list_purchase/' % {'lang': get_language()},
            'create_url': '/%(lang)s/accounting/create_purchase/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_purchase/' % {'lang': get_language()},
            'title': _('List of purchases'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(transaction_type=1).values(
                'id', 'supplier__description', 'document', 'source_document', 'date', 'comment'))
        }

        event_log(User.objects.get(username=request.user).id, 2, self.__str__().split(' ')[0].split('<')[1])

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        column_order = request.POST.get('order[0][column]')
        column_name = request.POST.get('columns[0][data]'.replace('0', column_order))
        if request.POST.get('order[0][dir]') == 'desc':
            column_name = '-' + column_name

        search = request.POST.get('search[value]')
        if search:
            self.items = list(self.model.objects.filter(transaction_type=1).filter(
                Q(document__icontains=search) |
                Q(supplier__description__icontains=search)
            ).distinct().order_by(column_name).values(
                'id', 'supplier__description', 'document', 'source_document', 'date', 'comment'
            ))
        else:
            self.items = list(self.model.objects.filter(transaction_type=1).order_by(column_name).values(
                'id', 'supplier__description', 'document', 'source_document', 'date', 'comment'
            ))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreatePurchase(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    form_class = PurchaseSummaryForm
    template_name = 'accounting/create_purchase.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/accounting/create_purchase/',
            'list_url': '/%(lang)s/accounting/list_purchase/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_purchase/' % {'lang': get_language()},
            'title': _('New purchase'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'message_texts': message_texts,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'search_store':
            search = request.POST.get('q', None)

            data = get_store(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_area':
            search = request.POST.get('q', None)
            store = request.POST.get('store', None)

            data = get_area(search, store)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_location':
            search = request.POST.get('q', None)
            area = request.POST.get('area', None)

            data = get_location(search, area)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_supplier':
            search = request.POST.get('q', None)

            data = get_supplier(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_product':
            search = request.POST.get('q', None)

            data = get_purchase_product(search)

            return JsonResponse(data, safe=False)

        form = self.form_class(request.POST)
        if form.is_valid():
            data = {}
            if request.POST.get('action', None) == 'save':
                data = build_transaction(request, form)
                if data['status'] == 'ok':
                    messages.success(request, message_texts['success']['transaction_successfully_saved'])
                    event_log(User.objects.get(username=request.user).id, 1, self.__str__().split(' ')[0].split('<')[1],
                              'summary_id: ' + str(data['summary'].id) + ' | transaction_type: ' +
                              str(data['summary'].transaction_type) + ' | document: ' + data['summary'].document +
                              ' | date: ' + data['summary'].date.strftime('%Y-%m-%d'))
                else:
                    messages.error(request, message_texts['error']['transaction_save_failed'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request)
            }

            if 'status' in data:
                context['status'] = data['status']
            if 'summary' in data and not data['summary'] is None:
                context['transact_id'] = data['summary'].id

            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'errors': form.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


class PrintPurchase(View):
    success_url = reverse_lazy('accounting:list_purchase')
    template_path = 'accounting/print_purchase.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            template = get_template(self.template_path)
            summary = TransactionSummary.objects.get(pk=self.kwargs['pk']).to_json()
            items = TransactionDetail.objects.filter(summary_id=self.kwargs['pk'])
            detail = []
            total = 0
            for i in items:
                item = i.to_json()
                item['subtotal'] = round(i.quantity * i.cost_price, 2)
                detail.append(item)
                total += item['subtotal']
            summary['total'] = total

            supplier_id = summary['supplier']['id']
            context = {
                'setting': Setting.objects.first(),
                'summary': summary,
                'detail': detail,
            }
            html = template.render(context)
            result = BytesIO()
            links = lambda uri, rel: os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ''))
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8', link_callback=links)

            event_log(User.objects.get(username=request.user).id, 5, self.__str__().split(' ')[0].split('<')[1])
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.success_url)


class ListSale(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    template_name = 'accounting/list_sale.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/accounting/list_sale/',
            'list_url': '/%(lang)s/accounting/list_sale/' % {'lang': get_language()},
            'create_url': '/%(lang)s/accounting/create_sale/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_sale/' % {'lang': get_language()},
            'title': _('List of sales'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(transaction_type=2).values(
                'id', 'customer__description', 'document', 'source_document', 'date', 'comment'))
        }

        event_log(User.objects.get(username=request.user).id, 2, self.__str__().split(' ')[0].split('<')[1])

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        column_order = request.POST.get('order[0][column]')
        column_name = request.POST.get('columns[0][data]'.replace('0', column_order))
        if request.POST.get('order[0][dir]') == 'desc':
            column_name = '-' + column_name

        search = request.POST.get('search[value]')
        if search:
            self.items = list(self.model.objects.filter(transaction_type=2).filter(
                Q(document__icontains=search) |
                Q(customer__description__icontains=search)
            ).distinct().order_by(column_name).values(
                'id', 'customer__description', 'document', 'source_document', 'date', 'comment'
            ))
        else:
            self.items = list(self.model.objects.filter(transaction_type=2).order_by(column_name).values(
                'id', 'customer__description', 'document', 'source_document', 'date', 'comment'
            ))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreateSale(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    form_class = SaleSummaryForm
    template_name = 'accounting/create_sale.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/accounting/create_sale/',
            'lang_url': '/%(lang)s/accounting/' % {'lang': get_language()},
            'list_url': '/%(lang)s/accounting/list_sale/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_sale/' % {'lang': get_language()},
            'title': _('New sale'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'message_texts': message_texts,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'search_store':
            search = request.POST.get('q', None)

            data = get_store(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_area':
            search = request.POST.get('q', None)
            store = request.POST.get('store', None)

            data = get_area(search, store)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_customer':
            search = request.POST.get('q', None)

            data = get_customer(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_product':
            search = request.POST.get('q', None)
            area = request.POST.get('area', None)

            data = get_sale_product(search, area)

            return JsonResponse(data, safe=False)

        form = self.form_class(request.POST)
        if form.is_valid():
            data = {}
            if request.POST.get('action', None) == 'save':
                data = build_transaction(request, form)
                if data['status'] == 'ok':
                    messages.success(request, message_texts['success']['transaction_successfully_saved'])
                    event_log(User.objects.get(username=request.user).id, 1, self.__str__().split(' ')[0].split('<')[1],
                              'summary_id: ' + str(data['summary'].id) + ' | transaction_type: ' +
                              str(data['summary'].transaction_type) + ' | document: ' + data['summary'].document +
                              ' | date: ' + data['summary'].date.strftime('%Y-%m-%d'))
                else:
                    messages.error(request, message_texts['error']['transaction_save_failed'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request),
                'value_adjustments': []
            }

            if 'status' in data:
                context['status'] = data['status']
            if 'summary' in data and not data['summary'] is None:
                context['transact_id'] = data['summary'].id
            if 'value_adjustments' in data:
                context['value_adjustments'] = data['value_adjustments']

            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'errors': form.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


class PrintSale(View):
    success_url = reverse_lazy('accounting:list_sale')
    template_path = 'accounting/print_sale.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            template = get_template(self.template_path)
            summary = TransactionSummary.objects.get(pk=self.kwargs['pk']).to_json()
            items = TransactionDetail.objects.filter(summary_id=self.kwargs['pk'])
            detail = []
            total = 0
            for i in items:
                item = i.to_json()
                item['subtotal'] = round(i.quantity * i.sale_price, 2)
                detail.append(item)
                total += item['subtotal']
            summary['total'] = total

            customer_id = summary['customer']['id']
            context = {
                'setting': Setting.objects.first(),
                'summary': summary,
                'detail': detail,
            }
            html = template.render(context)
            result = BytesIO()
            links = lambda uri, rel: os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ''))
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8', link_callback=links)

            event_log(User.objects.get(username=request.user).id, 5, self.__str__().split(' ')[0].split('<')[1])
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.success_url)


class ListSaleReturn(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    template_name = 'accounting/list_sale_return.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/accounting/list_sale_return/',
            'list_url': '/%(lang)s/accounting/list_sale_return/' % {'lang': get_language()},
            'create_url': '/%(lang)s/accounting/create_sale_return/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_sale_return/' % {'lang': get_language()},
            'title': _('List of sales returns'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(transaction_type=3).values(
                'id', 'customer__description', 'document', 'source_document', 'date', 'comment'))
        }

        event_log(User.objects.get(username=request.user).id, 2, self.__str__().split(' ')[0].split('<')[1])

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        column_order = request.POST.get('order[0][column]')
        column_name = request.POST.get('columns[0][data]'.replace('0', column_order))
        if request.POST.get('order[0][dir]') == 'desc':
            column_name = '-' + column_name

        search = request.POST.get('search[value]')
        if search:
            self.items = list(self.model.objects.filter(transaction_type=3).filter(
                Q(document__icontains=search) |
                Q(customer__description__icontains=search)
            ).distinct().order_by(column_name).values(
                'id', 'customer__description', 'document', 'source_document', 'date', 'comment'
            ))
        else:
            self.items = list(self.model.objects.filter(transaction_type=3).order_by(column_name).values(
                'id', 'customer__description', 'document', 'source_document', 'date', 'comment'
            ))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreateSaleReturn(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    form_class = SaleReturnSummaryForm
    template_name = 'accounting/create_sale_return.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/accounting/create_sale_return/',
            'list_url': '/%(lang)s/accounting/list_sale_return/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_sale_return/' % {'lang': get_language()},
            'title': _('New sale return'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'message_texts': message_texts,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'search_sale':
            search = request.POST.get('q', None)

            data = get_sale(search)

            return JsonResponse(data, safe=False)

        form = self.form_class(request.POST)
        if form.is_valid():
            data = {}
            if request.POST.get('action', None) == 'save':
                data = build_transaction(request, form)
                if data['status'] == 'ok':
                    messages.success(request, message_texts['success']['transaction_successfully_saved'])
                    event_log(User.objects.get(username=request.user).id, 1, self.__str__().split(' ')[0].split('<')[1],
                              'summary_id: ' + str(data['summary'].id) + ' | transaction_type: ' +
                              str(data['summary'].transaction_type) + ' | document: ' + data['summary'].document +
                              ' | date: ' + data['summary'].date.strftime('%Y-%m-%d'))
                else:
                    messages.error(request, message_texts['error']['transaction_save_failed'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request)
            }

            if 'status' in data:
                context['status'] = data['status']
            if 'summary' in data and not data['summary'] is None:
                context['transact_id'] = data['summary'].id

            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'errors': form.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


class PrintSaleReturn(View):
    success_url = reverse_lazy('accounting:list_sale_return')
    template_path = 'accounting/print_sale_return.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            template = get_template(self.template_path)
            summary = TransactionSummary.objects.get(pk=self.kwargs['pk']).to_json()
            items = TransactionDetail.objects.filter(summary_id=self.kwargs['pk'])
            detail = []
            total = 0
            for i in items:
                item = i.to_json()
                item['subtotal'] = round(i.quantity * i.sale_price, 2)
                detail.append(item)
                total += item['subtotal']
            summary['total'] = total

            customer_id = summary['customer']['id']
            context = {
                'setting': Setting.objects.first(),
                'summary': summary,
                'detail': detail,
            }
            html = template.render(context)
            result = BytesIO()
            links = lambda uri, rel: os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ''))
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8', link_callback=links)

            event_log(User.objects.get(username=request.user).id, 5, self.__str__().split(' ')[0].split('<')[1])
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.success_url)


class ListPurchaseReturn(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    template_name = 'accounting/list_purchase_return.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/accounting/list_purchase_return/',
            'list_url': '/%(lang)s/accounting/list_purchase_return/' % {'lang': get_language()},
            'create_url': '/%(lang)s/accounting/create_purchase_return/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_purchase_return/' % {'lang': get_language()},
            'title': _('List of purchases returns'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(transaction_type=4).values(
                'id', 'supplier__description', 'document', 'source_document', 'date', 'comment'))
        }

        event_log(User.objects.get(username=request.user).id, 2, self.__str__().split(' ')[0].split('<')[1])

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        column_order = request.POST.get('order[0][column]')
        column_name = request.POST.get('columns[0][data]'.replace('0', column_order))
        if request.POST.get('order[0][dir]') == 'desc':
            column_name = '-' + column_name

        search = request.POST.get('search[value]')
        if search:
            self.items = list(self.model.objects.filter(transaction_type=4).filter(
                Q(document__icontains=search) |
                Q(supplier__description__icontains=search)
            ).distinct().order_by(column_name).values(
                'id', 'supplier__description', 'document', 'source_document', 'date', 'comment'
            ))
        else:
            self.items = list(self.model.objects.filter(transaction_type=4).order_by(column_name).values(
                'id', 'supplier__description', 'document', 'source_document', 'date', 'comment'
            ))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreatePurchaseReturn(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    form_class = PurchaseReturnSummaryForm
    template_name = 'accounting/create_purchase_return.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/accounting/create_purchase_return/',
            'list_url': '/%(lang)s/accounting/list_purchase_return/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_purchase_return/' % {'lang': get_language()},
            'title': _('New purchase return'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'message_texts': message_texts,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'search_purchase':
            search = request.POST.get('q', None)

            data = get_purchase(search)

            return JsonResponse(data, safe=False)

        form = self.form_class(request.POST)
        if form.is_valid():
            data = {}
            if request.POST.get('action', None) == 'save':
                data = build_transaction(request, form)
                if data['status'] == 'ok':
                    messages.success(request, message_texts['success']['transaction_successfully_saved'])
                    event_log(User.objects.get(username=request.user).id, 1, self.__str__().split(' ')[0].split('<')[1],
                              'summary_id: ' + str(data['summary'].id) + ' | transaction_type: ' +
                              str(data['summary'].transaction_type) + ' | document: ' + data['summary'].document +
                              ' | date: ' + data['summary'].date.strftime('%Y-%m-%d'))
                else:
                    messages.error(request, message_texts['error']['transaction_save_failed'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request)
            }

            if 'status' in data:
                context['status'] = data['status']
            if 'summary' in data and not data['summary'] is None:
                context['transact_id'] = data['summary'].id

            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'errors': form.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


class PrintPurchaseReturn(View):
    success_url = reverse_lazy('accounting:list_purchase_return')
    template_path = 'accounting/print_purchase_return.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            template = get_template(self.template_path)
            summary = TransactionSummary.objects.get(pk=self.kwargs['pk']).to_json()
            items = TransactionDetail.objects.filter(summary_id=self.kwargs['pk'])
            detail = []
            total = 0
            for i in items:
                item = i.to_json()
                item['subtotal'] = round(i.quantity * i.cost_price, 2)
                detail.append(item)
                total += item['subtotal']
            summary['total'] = total

            supplier_id = summary['supplier']['id']
            context = {
                'setting': Setting.objects.first(),
                'summary': summary,
                'detail': detail,
            }
            html = template.render(context)
            result = BytesIO()
            links = lambda uri, rel: os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ''))
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8', link_callback=links)

            event_log(User.objects.get(username=request.user).id, 5, self.__str__().split(' ')[0].split('<')[1])
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.success_url)


class ListPositiveAdjustment(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    template_name = 'accounting/list_positive_adjustment.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/accounting/list_positive_adjustment/',
            'list_url': '/%(lang)s/accounting/list_positive_adjustment/' % {'lang': get_language()},
            'create_url': '/%(lang)s/accounting/create_positive_adjustment/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_positive_adjustment/' % {'lang': get_language()},
            'title': _('List of positive adjustments'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(transaction_type=5).values(
                'id', 'document', 'source_document', 'date', 'comment'))
        }

        event_log(User.objects.get(username=request.user).id, 2, self.__str__().split(' ')[0].split('<')[1])

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        column_order = request.POST.get('order[0][column]')
        column_name = request.POST.get('columns[0][data]'.replace('0', column_order))
        if request.POST.get('order[0][dir]') == 'desc':
            column_name = '-' + column_name

        search = request.POST.get('search[value]')
        if search:
            self.items = list(self.model.objects.filter(transaction_type=5).filter(
                Q(document__icontains=search) |
                Q(source_document__icontains=search)
            ).distinct().order_by(column_name).values(
                'id', 'document', 'source_document', 'date', 'comment'
            ))
        else:
            self.items = list(self.model.objects.filter(transaction_type=5).order_by(column_name).values(
                'id', 'document', 'source_document', 'date', 'comment'
            ))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreatePositiveAdjustment(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    form_class = AdjustmentSummaryForm
    template_name = 'accounting/create_positive_adjustment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/accounting/create_positive_adjustment/',
            'list_url': '/%(lang)s/accounting/list_positive_adjustment/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_positive_adjustment/' % {'lang': get_language()},
            'title': _('New positive adjustment'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'message_texts': message_texts,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'search_store':
            search = request.POST.get('q', None)

            data = get_store(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_area':
            search = request.POST.get('q', None)
            store = request.POST.get('store', None)

            data = get_area(search, store)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_positive_adjustment_product':
            search = request.POST.get('q', None)
            area = request.POST.get('area', None)

            data = get_positive_adjustment_product(search, area)

            return JsonResponse(data, safe=False)

        form = self.form_class(request.POST)
        if form.is_valid():
            data = {}
            if request.POST.get('action', None) == 'save':
                data = build_transaction(request, form)
                if data['status'] == 'ok':
                    messages.success(request, message_texts['success']['transaction_successfully_saved'])
                    event_log(User.objects.get(username=request.user).id, 1, self.__str__().split(' ')[0].split('<')[1],
                              'summary_id: ' + str(data['summary'].id) + ' | transaction_type: ' +
                              str(data['summary'].transaction_type) + ' | document: ' + data['summary'].document +
                              ' | date: ' + data['summary'].date.strftime('%Y-%m-%d'))
                else:
                    messages.error(request, message_texts['error']['transaction_save_failed'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request)
            }

            if 'status' in data:
                context['status'] = data['status']
            if 'summary' in data and not data['summary'] is None:
                context['transact_id'] = data['summary'].id

            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'errors': form.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


class PrintPositiveAdjustment(View):
    success_url = reverse_lazy('accounting:list_positive_adjustment')
    template_path = 'accounting/print_positive_adjustment.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            template = get_template(self.template_path)
            summary = TransactionSummary.objects.get(pk=self.kwargs['pk']).to_json()
            items = TransactionDetail.objects.filter(summary_id=self.kwargs['pk'])
            detail = []
            total = 0
            for i in items:
                item = i.to_json()
                item['subtotal'] = round(i.quantity * i.cost_price, 2)
                detail.append(item)
                total += item['subtotal']
            summary['total'] = total

            context = {
                'setting': Setting.objects.first(),
                'summary': summary,
                'detail': detail,
            }
            html = template.render(context)
            result = BytesIO()
            links = lambda uri, rel: os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ''))
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8', link_callback=links)

            event_log(User.objects.get(username=request.user).id, 5, self.__str__().split(' ')[0].split('<')[1])
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.success_url)


class ListNegativeAdjustment(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    template_name = 'accounting/list_negative_adjustment.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/accounting/list_negative_adjustment/',
            'list_url': '/%(lang)s/accounting/list_negative_adjustment/' % {'lang': get_language()},
            'create_url': '/%(lang)s/accounting/create_negative_adjustment/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_negative_adjustment/' % {'lang': get_language()},
            'title': _('List of negative adjustments'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(transaction_type=6).values(
                'id', 'document', 'source_document', 'date', 'comment'))
        }

        event_log(User.objects.get(username=request.user).id, 2, self.__str__().split(' ')[0].split('<')[1])

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        column_order = request.POST.get('order[0][column]')
        column_name = request.POST.get('columns[0][data]'.replace('0', column_order))
        if request.POST.get('order[0][dir]') == 'desc':
            column_name = '-' + column_name

        search = request.POST.get('search[value]')
        if search:
            self.items = list(self.model.objects.filter(transaction_type=6).filter(
                Q(document__icontains=search) |
                Q(source_document__icontains=search)
            ).distinct().order_by(column_name).values(
                'id', 'document', 'source_document', 'date', 'comment'
            ))
        else:
            self.items = list(self.model.objects.filter(transaction_type=6).order_by(column_name).values(
                'id', 'document', 'source_document', 'date', 'comment'
            ))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreateNegativeAdjustment(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    form_class = AdjustmentSummaryForm
    template_name = 'accounting/create_negative_adjustment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/accounting/create_negative_adjustment/',
            'list_url': '/%(lang)s/accounting/list_negative_adjustment/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_negative_adjustment/' % {'lang': get_language()},
            'title': _('New negative adjustment'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'message_texts': message_texts,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'search_store':
            search = request.POST.get('q', None)

            data = get_store(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_area':
            search = request.POST.get('q', None)
            store = request.POST.get('store', None)

            data = get_area(search, store)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_negative_adjustment_product':
            search = request.POST.get('q', None)
            area = request.POST.get('area', None)

            data = get_negative_adjustment_product(search, area)

            return JsonResponse(data, safe=False)

        form = self.form_class(request.POST)
        if form.is_valid():
            data = {}
            if request.POST.get('action', None) == 'save':
                data = build_transaction(request, form)
                if data['status'] == 'ok':
                    messages.success(request, message_texts['success']['transaction_successfully_saved'])
                    event_log(User.objects.get(username=request.user).id, 1, self.__str__().split(' ')[0].split('<')[1],
                              'summary_id: ' + str(data['summary'].id) + ' | transaction_type: ' +
                              str(data['summary'].transaction_type) + ' | document: ' + data['summary'].document +
                              ' | date: ' + data['summary'].date.strftime('%Y-%m-%d'))
                else:
                    messages.error(request, message_texts['error']['transaction_save_failed'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'status': 'ok',
                'messages_group': get_messages_group(request)
            }

            if 'status' in data:
                context['status'] = data['status']
            if 'summary' in data and not data['summary'] is None:
                context['transact_id'] = data['summary'].id

            return JsonResponse(context)
        else:
            if request.POST.get('action', None) == 'save':
                messages.error(request, message_texts['error']['error_validation_encountered'])
                messages.info(request, message_texts['info']['check_data_entered'])

            context = {
                'cleaned_data': list(form.cleaned_data),
                'errors': form.errors.get_json_data(escape_html=False),
                'status': 'ko',
                'messages_group': get_messages_group(request)
            }

            return JsonResponse(context)


class PrintNegativeAdjustment(View):
    success_url = reverse_lazy('accounting:list_negative_adjustment')
    template_path = 'accounting/print_negative_adjustment.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            template = get_template(self.template_path)
            summary = TransactionSummary.objects.get(pk=self.kwargs['pk']).to_json()
            items = TransactionDetail.objects.filter(summary_id=self.kwargs['pk'])
            detail = []
            total = 0
            for i in items:
                item = i.to_json()
                item['subtotal'] = round(i.quantity * i.cost_price, 2)
                detail.append(item)
                total += item['subtotal']
            summary['total'] = total

            context = {
                'setting': Setting.objects.first(),
                'summary': summary,
                'detail': detail,
            }
            html = template.render(context)
            result = BytesIO()
            links = lambda uri, rel: os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ''))
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8', link_callback=links)

            event_log(User.objects.get(username=request.user).id, 5, self.__str__().split(' ')[0].split('<')[1])
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.success_url)


class ListPositiveValueAdjustment(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    template_name = 'accounting/list_positive_value_adjustment.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/accounting/list_positive_value_adjustment/',
            'list_url': '/%(lang)s/accounting/list_positive_value_adjustment/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_positive_value_adjustment/' % {'lang': get_language()},
            'title': _('List of positive value adjustments'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(transaction_type=7).values(
                'id', 'document', 'source_document', 'date', 'comment'))
        }

        event_log(User.objects.get(username=request.user).id, 2, self.__str__().split(' ')[0].split('<')[1])

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        column_order = request.POST.get('order[0][column]')
        column_name = request.POST.get('columns[0][data]'.replace('0', column_order))
        if request.POST.get('order[0][dir]') == 'desc':
            column_name = '-' + column_name

        search = request.POST.get('search[value]')
        if search:
            self.items = list(self.model.objects.filter(transaction_type=7).filter(
                Q(document__icontains=search) |
                Q(source_document__icontains=search)
            ).distinct().order_by(column_name).values(
                'id', 'document', 'source_document', 'date', 'comment'
            ))
        else:
            self.items = list(self.model.objects.filter(transaction_type=7).order_by(column_name).values(
                'id', 'document', 'source_document', 'date', 'comment'
            ))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class PrintPositiveValueAdjustment(View):
    success_url = reverse_lazy('accounting:list_positive_value_adjustment')
    template_path = 'accounting/print_positive_value_adjustment.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            template = get_template(self.template_path)
            summary = TransactionSummary.objects.get(pk=self.kwargs['pk']).to_json()
            items = TransactionDetail.objects.filter(summary_id=self.kwargs['pk'])
            detail = []
            total = 0
            for i in items:
                item = i.to_json()
                item['subtotal'] = i.cost_price
                detail.append(item)
                total += item['subtotal']
            summary['total'] = total

            context = {
                'setting': Setting.objects.first(),
                'summary': summary,
                'detail': detail,
            }
            html = template.render(context)
            result = BytesIO()
            links = lambda uri, rel: os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ''))
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8', link_callback=links)

            event_log(User.objects.get(username=request.user).id, 5, self.__str__().split(' ')[0].split('<')[1])
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.success_url)


class ListNegativeValueAdjustment(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper']
    login_url = 'security/login'
    model = TransactionSummary
    template_name = 'accounting/list_negative_value_adjustment.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/accounting/list_negative_value_adjustment/',
            'list_url': '/%(lang)s/accounting/list_negative_value_adjustment/' % {'lang': get_language()},
            'print_url': '/%(lang)s/accounting/print_negative_value_adjustment/' % {'lang': get_language()},
            'title': _('List of negative value adjustments'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(transaction_type=8).values(
                'id', 'document', 'source_document', 'date', 'comment'))
        }

        event_log(User.objects.get(username=request.user).id, 2, self.__str__().split(' ')[0].split('<')[1])

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        column_order = request.POST.get('order[0][column]')
        column_name = request.POST.get('columns[0][data]'.replace('0', column_order))
        if request.POST.get('order[0][dir]') == 'desc':
            column_name = '-' + column_name

        search = request.POST.get('search[value]')
        if search:
            self.items = list(self.model.objects.filter(transaction_type=8).filter(
                Q(document__icontains=search) |
                Q(source_document__icontains=search)
            ).distinct().order_by(column_name).values(
                'id', 'document', 'source_document', 'date', 'comment'
            ))
        else:
            self.items = list(self.model.objects.filter(transaction_type=8).order_by(column_name).values(
                'id', 'document', 'source_document', 'date', 'comment'
            ))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class PrintNegativeValueAdjustment(View):
    success_url = reverse_lazy('accounting:list_negative_value_adjustment')
    template_path = 'accounting/print_negative_value_adjustment.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            template = get_template(self.template_path)
            summary = TransactionSummary.objects.get(pk=self.kwargs['pk']).to_json()
            items = TransactionDetail.objects.filter(summary_id=self.kwargs['pk'])
            detail = []
            total = 0
            for i in items:
                item = i.to_json()
                item['subtotal'] = i.cost_price
                detail.append(item)
                total += item['subtotal']
            summary['total'] = total

            context = {
                'setting': Setting.objects.first(),
                'summary': summary,
                'detail': detail,
            }
            html = template.render(context)
            result = BytesIO()
            links = lambda uri, rel: os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ''))
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8', link_callback=links)

            event_log(User.objects.get(username=request.user).id, 5, self.__str__().split(' ')[0].split('<')[1])
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.success_url)
