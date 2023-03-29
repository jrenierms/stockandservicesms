from apps.accounting.models import TransactionSummary, Stock, TransactionDetail
from apps.base.decorators import AllowedUsers
from apps.base.texts import dialogs, message_texts
from apps.base.utils import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import get_language, gettext_lazy as _
from django.views.generic import View

from .forms import *


class ListCustomerCategory(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = CustomerCategory
    template_name = 'commercial/list_customer_category.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/commercial/list_customer_category/',
            'list_url': '/%(lang)s/commercial/list_customer_category/' % {'lang': get_language()},
            'create_url': '/%(lang)s/commercial/create_customer_category/' % {'lang': get_language()},
            'edit_url': '/%(lang)s/commercial/edit_customer_category/' % {'lang': get_language()},
            'delete_url': '/%(lang)s/commercial/delete_customer_category/' % {'lang': get_language()},
            'title': _('Customer categories'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(active=True).values('id', 'code', 'description', 'discount'))
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
            ).distinct().order_by(column_name).values('id', 'code', 'description', 'discount'))
        else:
            self.items = list(self.model.objects.filter(active=True).order_by(column_name).
                              values('id', 'code', 'description', 'discount'))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreateCustomerCategory(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = CustomerCategory
    form_class = CustomerCategoryForm
    template_name = 'commercial/create_customer_category.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/commercial/create_customer_category/',
            'list_url': '/%(lang)s/commercial/list_customer_category/' % {'lang': get_language()},
            'title': _('Customer categories'),
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
                          item.code + ' | description: ' + item.description + ' | discount: ' + str(item.discount))
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


class EditCustomerCategory(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = CustomerCategory
    form_class = CustomerCategoryForm
    template_name = 'commercial/create_customer_category.html'

    def get(self, request, pk=None, *args, **kwargs):
        try:
            item = self.model.objects.get(id=pk)
            form = self.form_class(instance=item)
        except:
            item = None

        if item is None:
            form = self.form_class()

        context = {
            'view_url': '/commercial/edit_customer_category/' + str(item.id) + '/',
            'list_url': '/%(lang)s/commercial/list_customer_category/' % {'lang': get_language()},
            'title': _('Customer categories'),
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
                          item.code + ' | description: ' + item.description + ' | discount: ' + str(item.discount))
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


class DeleteCustomerCategory(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = CustomerCategory

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
            item_exist = Customer.objects.filter(active=True, category=item).exists()
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
                          item.code + ' | description: ' + item.description + ' | discount: ' + str(item.discount))
                context = {
                    'status': 'ok',
                    'messages_group': get_messages_group(request)
                }

        print(context['messages_group'])

        return JsonResponse(context)


class ListCustomer(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Customer
    template_name = 'commercial/list_customer.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/commercial/list_customer/',
            'list_url': '/%(lang)s/commercial/list_customer/' % {'lang': get_language()},
            'create_url': '/%(lang)s/commercial/create_customer/' % {'lang': get_language()},
            'edit_url': '/%(lang)s/commercial/edit_customer/' % {'lang': get_language()},
            'delete_url': '/%(lang)s/commercial/delete_customer/' % {'lang': get_language()},
            'title': _('Customers'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(active=True).values(
                'id', 'code', 'description', 'owner', 'category__description'))
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
                Q(owner__icontains=search) |
                Q(category__description__icontains=search)
            ).distinct().order_by(column_name).values('id', 'code', 'description', 'owner', 'category__description'))
        else:
            self.items = list(self.model.objects.filter(active=True).order_by(column_name).
                              values('id', 'code', 'description', 'owner', 'category__description'))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreateCustomer(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Customer
    form_class = CustomerForm
    template_name = 'commercial/create_customer.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/commercial/create_customer/',
            'list_url': '/%(lang)s/commercial/list_customer/' % {'lang': get_language()},
            'title': _('Customers'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'search_customer_category':
            search = request.POST.get('q', None)

            data = get_customer_category(search)

            return JsonResponse(data, safe=False)

        form = self.form_class(request.POST)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save(commit=False)
                item.category = get_object_or_404(CustomerCategory, id=request.POST.get('category'))
                item.save()
                messages.success(request, message_texts['success']['record_successfully_saved'])
                event_log(User.objects.get(username=request.user).id, 1,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description + ' | owner: ' + item.owner +
                          ' | category: ' + item.category.description)
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


class EditCustomer(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Customer
    form_class = CustomerForm
    template_name = 'commercial/create_customer.html'

    def get(self, request, pk=None, *args, **kwargs):
        try:
            item = self.model.objects.get(id=pk)
            form = self.form_class(instance=item)
        except:
            item = None

        if item is None:
            form = self.form_class()

        context = {
            'view_url': '/commercial/edit_customer/' + str(item.id) + '/',
            'list_url': '/%(lang)s/commercial/list_customer/' % {'lang': get_language()},
            'title': _('Customers'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'item': item,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, pk=None, *args, **kwargs):
        if request.POST.get('action', None) == 'search_customer_category':
            search = request.POST.get('q', None)

            data = get_customer_category(search)

            return JsonResponse(data, safe=False)

        item = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=item)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save(commit=False)
                item.category = get_object_or_404(CustomerCategory, id=request.POST.get('category'))
                item.save()
                messages.success(request, message_texts['success']['record_successfully_saved'])
                event_log(User.objects.get(username=request.user).id, 3,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description + ' | owner: ' + item.owner +
                          ' | category: ' + item.category.description)
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


class DeleteCustomer(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Customer

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
            item_exist = TransactionSummary.objects.filter(active=True, customer=item).exists()
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
                          item.code + ' | description: ' + item.description + ' | owner: ' + item.owner +
                          ' | category: ' + item.category.description)
                context = {
                    'status': 'ok',
                    'messages_group': get_messages_group(request)
                }

        return JsonResponse(context)


class ListSupplier(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Supplier
    template_name = 'commercial/list_supplier.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/commercial/list_supplier/',
            'list_url': '/%(lang)s/commercial/list_supplier/' % {'lang': get_language()},
            'create_url': '/%(lang)s/commercial/create_supplier/' % {'lang': get_language()},
            'edit_url': '/%(lang)s/commercial/edit_supplier/' % {'lang': get_language()},
            'delete_url': '/%(lang)s/commercial/delete_supplier/' % {'lang': get_language()},
            'title': _('Suppliers'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(active=True).values(
                'id', 'code', 'description', 'owner', 'address'))
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
                Q(owner__icontains=search)
            ).distinct().order_by(column_name).values('id', 'code', 'description', 'owner', 'address'))
        else:
            self.items = list(self.model.objects.filter(active=True).order_by(column_name).
                              values('id', 'code', 'description', 'owner', 'address'))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreateSupplier(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Supplier
    form_class = SupplierForm
    template_name = 'commercial/create_supplier.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/commercial/create_supplier/',
            'list_url': '/%(lang)s/commercial/list_supplier/' % {'lang': get_language()},
            'title': _('Suppliers'),
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
                          item.code + ' | description: ' + item.description + ' | owner: ' + item.owner)
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


class EditSupplier(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Supplier
    form_class = SupplierForm
    template_name = 'commercial/create_supplier.html'

    def get(self, request, pk=None, *args, **kwargs):
        try:
            item = self.model.objects.get(id=pk)
            form = self.form_class(instance=item)
        except:
            item = None

        if item is None:
            form = self.form_class()

        context = {
            'view_url': '/commercial/edit_supplier/' + str(item.id) + '/',
            'list_url': '/%(lang)s/commercial/list_supplier/' % {'lang': get_language()},
            'title': _('Suppliers'),
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
                          item.code + ' | description: ' + item.description + ' | owner: ' + item.owner)
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


class DeleteSupplier(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Supplier

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
            item_exist = TransactionSummary.objects.filter(active=True, supplier=item).exists()
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
                          item.code + ' | description: ' + item.description + ' | owner: ' + item.owner)
                context = {
                    'status': 'ok',
                    'messages_group': get_messages_group(request)
                }

        return JsonResponse(context)


class ListFamilyGroup(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = FamilyGroup
    template_name = 'commercial/list_family_group.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/commercial/list_family_group/',
            'list_url': '/%(lang)s/commercial/list_family_group/' % {'lang': get_language()},
            'create_url': '/%(lang)s/commercial/create_family_group/' % {'lang': get_language()},
            'edit_url': '/%(lang)s/commercial/edit_family_group/' % {'lang': get_language()},
            'delete_url': '/%(lang)s/commercial/delete_family_group/' % {'lang': get_language()},
            'title': _('Family groups'),
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


class CreateFamilyGroup(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = FamilyGroup
    form_class = FamilyGroupForm
    template_name = 'commercial/create_family_group.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/commercial/create_family_group/',
            'list_url': '/%(lang)s/commercial/list_family_group/' % {'lang': get_language()},
            'title': _('Family groups'),
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


class EditFamilyGroup(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = FamilyGroup
    form_class = FamilyGroupForm
    template_name = 'commercial/create_family_group.html'

    def get(self, request, pk=None, *args, **kwargs):
        try:
            item = self.model.objects.get(id=pk)
            form = self.form_class(instance=item)
        except:
            item = None

        if item is None:
            form = self.form_class()

        context = {
            'view_url': '/commercial/edit_family_group/' + str(item.id) + '/',
            'list_url': '/%(lang)s/commercial/list_family_group/' % {'lang': get_language()},
            'title': _('Family groups'),
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


class DeleteFamilyGroup(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = FamilyGroup

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
            item_exist = Family.objects.filter(active=True, group=item).exists()
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


class ListFamilyActivity(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = FamilyActivity
    template_name = 'commercial/list_family_activity.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/commercial/list_family_activity/',
            'list_url': '/%(lang)s/commercial/list_family_activity/' % {'lang': get_language()},
            'create_url': '/%(lang)s/commercial/create_family_activity/' % {'lang': get_language()},
            'edit_url': '/%(lang)s/commercial/edit_family_activity/' % {'lang': get_language()},
            'delete_url': '/%(lang)s/commercial/delete_family_activity/' % {'lang': get_language()},
            'title': _('Family activities'),
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


class CreateFamilyActivity(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = FamilyActivity
    form_class = FamilyActivityForm
    template_name = 'commercial/create_family_activity.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/commercial/create_family_activity/',
            'list_url': '/%(lang)s/commercial/list_family_activity/' % {'lang': get_language()},
            'title': _('Family activities'),
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


class EditFamilyActivity(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = FamilyActivity
    form_class = FamilyActivityForm
    template_name = 'commercial/create_family_activity.html'

    def get(self, request, pk=None, *args, **kwargs):
        try:
            item = self.model.objects.get(id=pk)
            form = self.form_class(instance=item)
        except:
            item = None

        if item is None:
            form = self.form_class()

        context = {
            'view_url': '/commercial/edit_family_activity/' + str(item.id) + '/',
            'list_url': '/%(lang)s/commercial/list_family_activity/' % {'lang': get_language()},
            'title': _('Family activities'),
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


class DeleteFamilyActivity(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = FamilyActivity

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
            item_exist = Family.objects.filter(active=True, activity=item).exists()
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


class ListFamily(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Family
    template_name = 'commercial/list_family.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/commercial/list_family/',
            'list_url': '/%(lang)s/commercial/list_family/' % {'lang': get_language()},
            'create_url': '/%(lang)s/commercial/create_family/' % {'lang': get_language()},
            'edit_url': '/%(lang)s/commercial/edit_family/' % {'lang': get_language()},
            'delete_url': '/%(lang)s/commercial/delete_family/' % {'lang': get_language()},
            'title': _('Families'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(active=True).values(
                'id', 'code', 'description', 'increment', 'group__description', 'activity__description'))
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
                Q(group__description__icontains=search) |
                Q(activity__description__icontains=search)
            ).distinct().order_by(column_name).values('id', 'code', 'description', 'increment', 'group__description',
                                                      'activity__description'))
        else:
            self.items = list(self.model.objects.filter(active=True).order_by(column_name).
                              values('id', 'code', 'description', 'increment', 'group__description',
                                     'activity__description'))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreateFamily(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Family
    form_class = FamilyForm
    template_name = 'commercial/create_family.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/commercial/create_family/',
            'list_url': '/%(lang)s/commercial/list_family/' % {'lang': get_language()},
            'title': _('Families'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'search_family_group':
            search = request.POST.get('q', None)

            data = get_family_group(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_family_activity':
            search = request.POST.get('q', None)

            data = get_family_activity(search)

            return JsonResponse(data, safe=False)

        form = self.form_class(request.POST)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save(commit=False)
                item.group = get_object_or_404(FamilyGroup, id=request.POST.get('group'))
                item.activity = get_object_or_404(FamilyActivity, id=request.POST.get('activity'))
                item.save()
                messages.success(request, message_texts['success']['record_successfully_saved'])
                event_log(User.objects.get(username=request.user).id, 1,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description + ' | group: ' + item.group.description +
                          ' | activity: ' + item.activity.description)
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


class EditFamily(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Family
    form_class = FamilyForm
    template_name = 'commercial/create_family.html'

    def get(self, request, pk=None, *args, **kwargs):
        try:
            item = self.model.objects.get(id=pk)
            form = self.form_class(instance=item)
        except:
            item = None

        if item is None:
            form = self.form_class()

        context = {
            'view_url': '/commercial/edit_family/' + str(item.id) + '/',
            'list_url': '/%(lang)s/commercial/list_family/' % {'lang': get_language()},
            'title': _('Families'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'item': item,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, pk=None, *args, **kwargs):
        if request.POST.get('action', None) == 'search_family_group':
            search = request.POST.get('q', None)

            data = get_family_group(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_family_activity':
            search = request.POST.get('q', None)

            data = get_family_activity(search)

            return JsonResponse(data, safe=False)

        item = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=item)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save(commit=False)
                item.group = get_object_or_404(FamilyGroup, id=request.POST.get('group'))
                item.activity = get_object_or_404(FamilyActivity, id=request.POST.get('activity'))
                item.save()
                messages.success(request, message_texts['success']['record_successfully_saved'])
                event_log(User.objects.get(username=request.user).id, 3,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                          item.code + ' | description: ' + item.description + ' | group: ' + item.group.description +
                          ' | activity: ' + item.activity.description)
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


class DeleteFamily(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Family

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
                          item.code + ' | description: ' + item.description + ' | group: ' + item.group.description +
                          ' | activity: ' + item.activity.description)
                context = {
                    'status': 'ok',
                    'messages_group': get_messages_group(request)
                }

        return JsonResponse(context)


class ListMeasurement(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Measurement
    template_name = 'commercial/list_measurement.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/commercial/list_measurement/',
            'list_url': '/%(lang)s/commercial/list_measurement/' % {'lang': get_language()},
            'create_url': '/%(lang)s/commercial/create_measurement/' % {'lang': get_language()},
            'edit_url': '/%(lang)s/commercial/edit_measurement/' % {'lang': get_language()},
            'delete_url': '/%(lang)s/commercial/delete_measurement/' % {'lang': get_language()},
            'title': _('Measurements'),
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


class CreateMeasurement(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Measurement
    form_class = MeasurementForm
    template_name = 'commercial/create_measurement.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/commercial/create_measurement/',
            'list_url': '/%(lang)s/commercial/list_measurement/' % {'lang': get_language()},
            'title': _('Measurements'),
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


class EditMeasurement(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Measurement
    form_class = MeasurementForm
    template_name = 'commercial/create_measurement.html'

    def get(self, request, pk=None, *args, **kwargs):
        try:
            item = self.model.objects.get(id=pk)
            form = self.form_class(instance=item)
        except:
            item = None

        if item is None:
            form = self.form_class()

        context = {
            'view_url': '/commercial/edit_measurement/' + str(item.id) + '/',
            'list_url': '/%(lang)s/commercial/list_measurement/' % {'lang': get_language()},
            'title': _('Measurements'),
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


class DeleteMeasurement(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Measurement

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
            item_exist = Product.objects.filter(active=True, measurement=item).exists()
            if not item_exist:
                item_exist = ProductConversion.objects.filter(active=True, measurement=item).exists()
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


class ListProduct(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Product
    template_name = 'commercial/list_product.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/commercial/list_product/',
            'list_url': '/%(lang)s/commercial/list_product/' % {'lang': get_language()},
            'create_url': '/%(lang)s/commercial/create_product/' % {'lang': get_language()},
            'edit_url': '/%(lang)s/commercial/edit_product/' % {'lang': get_language()},
            'delete_url': '/%(lang)s/commercial/delete_product/' % {'lang': get_language()},
            'title': _('Products'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(active=True).values(
                'id', 'code', 'description', 'sale_price', 'family__description', 'measurement__code'))
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
                Q(family__description__icontains=search)
            ).distinct().order_by(column_name).values('id', 'code', 'description', 'sale_price', 'family__description',
                                                      'measurement__code'))
        else:
            self.items = list(self.model.objects.filter(active=True).order_by(column_name).
                              values('id', 'code', 'description', 'sale_price', 'family__description',
                                     'measurement__code'))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreateProduct(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Product
    form_class = ProductForm
    template_name = 'commercial/create_product.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/commercial/create_product/',
            'list_url': '/%(lang)s/commercial/list_product/' % {'lang': get_language()},
            'title': _('Products'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'search_family':
            search = request.POST.get('q', None)

            data = get_family(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_measurement':
            search = request.POST.get('q', None)

            data = get_measurement(search)

            return JsonResponse(data, safe=False)

        form = self.form_class(request.POST)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save(commit=False)
                item.family = get_object_or_404(Family, id=request.POST.get('family'))
                item.measurement = get_object_or_404(Measurement, id=request.POST.get('measurement'))
                with transaction.atomic():
                    item.save()
                    item_pc = ProductConversion()
                    item_pc.product = item
                    item_pc.measurement = item.measurement
                    item_pc.value = 1
                    item_pc.save()
                    messages.success(request, message_texts['success']['record_successfully_saved'])
                    event_log(User.objects.get(username=request.user).id, 1,
                              self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | code: ' +
                              item.code + ' | description: ' + item.description + ' | sale_price: ' +
                              str(item.sale_price) + ' | measurement: ' + item.measurement.description + ' | family: ' +
                              item.family.description)
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


class EditProduct(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Product
    form_class = ProductForm
    template_name = 'commercial/create_product.html'

    def get(self, request, pk=None, *args, **kwargs):
        try:
            item = self.model.objects.get(id=pk)
            form = self.form_class(instance=item)
        except:
            item = None

        if item is None:
            form = self.form_class()

        context = {
            'view_url': '/commercial/edit_product/' + str(item.id) + '/',
            'list_url': '/%(lang)s/commercial/list_product/' % {'lang': get_language()},
            'title': _('Products'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'item': item,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, pk=None, *args, **kwargs):
        if request.POST.get('action', None) == 'search_family':
            search = request.POST.get('q', None)

            data = get_family(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_measurement':
            search = request.POST.get('q', None)

            data = get_measurement(search)

            return JsonResponse(data, safe=False)

        item = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=item)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save(commit=False)
                item.family = get_object_or_404(Family, id=request.POST.get('family'))
                item.measurement = get_object_or_404(Measurement, id=request.POST.get('measurement'))
                item_before = Product.objects.get(id=item.id)
                if not item_before.measurement == item.measurement:
                    item_exist = False
                    for pc in ProductConversion.objects.filter(active=True, product=item):
                        item_exist = TransactionDetail.objects.filter(product_conversion=pc).exists()
                        if item_exist:
                            break
                    if not item_exist:
                        item_exist = Stock.objects.filter(active=True, product=item).exists()
                    if item_exist:
                        messages.error(request, message_texts['error']['record_edition_failed'])
                        messages.info(request, message_texts['info']['product_measurement_related'])
                        context = {
                            'cleaned_data': list(form.cleaned_data),
                            'status': 'ko',
                            'messages_group': get_messages_group(request)
                        }

                        return JsonResponse(context)

                with transaction.atomic():
                    ProductConversion.objects.filter(
                        active=True, product=item, measurement=item_before.measurement
                    ).update(measurement=item.measurement)
                    item.save()
                    messages.success(request, message_texts['success']['record_successfully_saved'])
                    event_log(User.objects.get(username=request.user).id, 3, self.__str__().split(' ')[0].split('<')[1],
                              'id: ' + str(item.id) + ' | code: ' + item.code + ' | description: ' + item.description +
                              ' | sale_price: ' + str(item.sale_price) + ' | measurement: ' +
                              item.measurement.description + ' | family: ' + item.family.description)
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


class DeleteProduct(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = Product

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
            item_exist = False
            for pc in ProductConversion.objects.filter(active=True, product=item):
                item_exist = TransactionDetail.objects.filter(product_conversion=pc).exists()
                if item_exist:
                    break
            if not item_exist:
                item_exist = Stock.objects.filter(active=True, product=item).exists()
            if item_exist:
                messages.error(request, message_texts['error']['record_deletion_failed'])
                messages.info(request, message_texts['info']['record_deletion_related'])
                context = {
                    'status': 'ko',
                    'messages_group': get_messages_group(request)
                }
            else:
                with transaction.atomic():
                    item.conversions_product.update(active=False)
                    item.active = False
                    item.save()
                    messages.success(request, message_texts['success']['record_successfully_deleted'])
                    event_log(User.objects.get(username=request.user).id, 4, self.__str__().split(' ')[0].split('<')[1],
                              'id: ' + str(item.id) + ' | code: ' + item.code + ' | description: ' + item.description +
                              ' | sale_price: ' + str(item.sale_price) + ' | measurement: ' +
                              item.measurement.description + ' | family: ' + item.family.description)
                context = {
                    'status': 'ok',
                    'messages_group': get_messages_group(request)
                }

        return JsonResponse(context)


class ListProductConversion(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = ProductConversion
    template_name = 'commercial/list_product_conversion.html'
    items = None

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/commercial/list_product_conversion/',
            'list_url': '/%(lang)s/commercial/list_product_conversion/' % {'lang': get_language()},
            'create_url': '/%(lang)s/commercial/create_product_conversion/' % {'lang': get_language()},
            'edit_url': '/%(lang)s/commercial/edit_product_conversion/' % {'lang': get_language()},
            'delete_url': '/%(lang)s/commercial/delete_product_conversion/' % {'lang': get_language()},
            'title': _('Product conversions'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'data': list(self.model.objects.filter(active=True).values(
                'id', 'product__code', 'product__description', 'value', 'measurement__code', 'measurement__description'
            ))
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
                Q(product__description__icontains=search) |
                Q(meaasurement__description__icontains=search)
            ).distinct().order_by(column_name).values(
                'id', 'product__description', 'value', 'measurement__description'
            ))
        else:
            self.items = list(self.model.objects.filter(active=True).order_by(column_name).
                              values('id', 'product__description', 'value', 'measurement__description'))

        data = get_data_table_page(request, self.items)
        data['draw'] = int(request.POST.get('draw', None))

        return JsonResponse(data)


class CreateProductConversion(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = ProductConversion
    form_class = ProductConversionForm
    template_name = 'commercial/create_product_conversion.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'view_url': '/commercial/create_product_conversion/',
            'list_url': '/%(lang)s/commercial/list_product_conversion/' % {'lang': get_language()},
            'title': _('Product conversions'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', None) == 'search_product':
            search = request.POST.get('q', None)

            data = get_product(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_measurement':
            search = request.POST.get('q', None)

            data = get_measurement(search)

            return JsonResponse(data, safe=False)

        form = self.form_class(request.POST)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save(commit=False)
                item.product = get_object_or_404(Product, id=request.POST.get('product'))
                item.measurement = get_object_or_404(Measurement, id=request.POST.get('measurement'))
                item.save()
                messages.success(request, message_texts['success']['record_successfully_saved'])
                event_log(User.objects.get(username=request.user).id, 1,
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | product_id: ' +
                          str(item.product.id) + ' | product_description: ' + item.product.description + ' | value: ' +
                          str(item.value) + ' | measurement: ' + item.measurement.description)
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


class EditProductConversion(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = ProductConversion
    form_class = ProductConversionForm
    template_name = 'commercial/create_product_conversion.html'

    def get(self, request, pk=None, *args, **kwargs):
        try:
            item = self.model.objects.get(id=pk)
            form = self.form_class(instance=item)
        except:
            item = None

        if item is None:
            form = self.form_class()

        context = {
            'view_url': '/commercial/edit_product_conversion/' + str(item.id) + '/',
            'list_url': '/%(lang)s/commercial/list_product_conversion/' % {'lang': get_language()},
            'title': _('Product conversions'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'item': item,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, pk=None, *args, **kwargs):
        if request.POST.get('action', None) == 'search_product':
            search = request.POST.get('q', None)

            data = get_product(search)

            return JsonResponse(data, safe=False)

        if request.POST.get('action', None) == 'search_measurement':
            search = request.POST.get('q', None)

            data = get_measurement(search)

            return JsonResponse(data, safe=False)

        item = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=item)
        if form.is_valid():
            if request.POST.get('action', None) == 'save':
                item = form.save(commit=False)
                item.product = get_object_or_404(Product, id=request.POST.get('product'))
                item.measurement = get_object_or_404(Measurement, id=request.POST.get('measurement'))
                item_before = Product.objects.get(id=item.product_id)
                item_exist = Product.objects.filter(
                    active=True, id=item.product_id, measurement=item_before.measurement
                ).exists()
                if not item_exist:
                    item_exist = TransactionDetail.objects.filter(product_conversion=item).exists()
                if item_exist:
                    messages.error(request, message_texts['error']['record_edition_failed'])
                    messages.info(request, message_texts['info']['product_measurement_related'])
                    context = {
                        'cleaned_data': list(form.cleaned_data),
                        'status': 'ko',
                        'messages_group': get_messages_group(request)
                    }

                    return JsonResponse(context)

                item.save()
                messages.success(request, message_texts['success']['record_successfully_saved'])
                event_log(User.objects.get(username=request.user).id, 3, self.__str__().split(' ')[0].split('<')[1],
                          'id: ' + str(item.id) + ' | product_id: ' + str(item.product.id) + ' | product_description: ' +
                          item.product.description + ' | value: ' + str(item.value) + ' | measurement: ' +
                          item.measurement.description)
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


class DeleteProductConversion(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial']
    login_url = 'security/login'
    model = ProductConversion

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
            item_exist = Product.objects.filter(active=True, id=item.product_id, measurement=item.measurement).exists()
            if not item_exist:
                item_exist = TransactionDetail.objects.filter(product_conversion=item).exists()
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
                          self.__str__().split(' ')[0].split('<')[1], 'id: ' + str(item.id) + ' | product_id: ' +
                          str(item.product.id) + ' | product_description: ' + item.product.description + ' | value: ' +
                          str(item.value) + ' | measurement: ' + item.measurement.description)
                context = {
                    'status': 'ok',
                    'messages_group': get_messages_group(request)
                }

        return JsonResponse(context)
