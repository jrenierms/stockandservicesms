import json
from datetime import datetime
from decimal import Decimal

from apps.accounting.models import *
from apps.base.choices import colors
from apps.commercial.models import *
from apps.security.models import User, Audit
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _


def get_user_data(request):
    user_data = {}
    if request.user.is_authenticated:
        my_user = User.objects.get(username=request.user)
        user_data['name'] = my_user.first_name + ' ' + my_user.last_name.split(' ')[0]
        groups = list(my_user.groups.all())
        if groups.__len__() > 0:
            user_data['profile'] = groups[0].__str__()
        else:
            user_data['profile'] = _('Anonymous')
        user_data['joined'] = my_user.date_joined.date()
    else:
        user_data['name'] = _('Anonymous')
        user_data['profile'] = _('Anonymous')
        user_data['joined'] = '-'

    return user_data


def get_data_page(request, items=None):
    data = {}
    page = request.POST.get('page', None)
    paginator = Paginator(items, 8)
    if not page:
        page = 1
    elif page == 'last':
        page = paginator.num_pages
    items = paginator.get_page(page)

    if paginator.count == 0:
        data['items'] = items
        is_paginated = False
    else:
        is_paginated = True
        data['items'] = items.object_list
        pagination = {
            'start_index': items.start_index(),
            'end_index': items.end_index(),
            'count': items.paginator.count,
            'has_previous': items.has_previous(),
            'page_range': list(items.paginator.page_range),
            'number': items.number,
            'has_next': items.has_next(),
            'num_pages': items.paginator.num_pages
        }
        if items.has_previous():
            pagination['previous_page_number'] = items.previous_page_number()
        if items.has_next():
            pagination['next_page_number'] = items.next_page_number()
        data['pagination'] = pagination

    data['is_paginated'] = is_paginated

    return data


def get_data_table_page(request, items=None):
    data = {}
    page_start = int(request.POST.get('start', None))
    page_length = int(request.POST.get('length', None))
    page = (page_start // page_length) + 1
    paginator = Paginator(items, 10)

    if paginator.count == 0:
        is_paginated = False
        data['data'] = items
        data['pagination'] = {}
        data['recordsTotal'] = items.__len__()
        data['recordsFiltered'] = items.__len__()
    else:
        is_paginated = True
        items = paginator.get_page(page)
        data['data'] = items.object_list
        pagination = {
            'start_index': items.start_index(),
            'end_index': items.end_index(),
            'has_previous': items.has_previous(),
            'page_range': list(items.paginator.page_range),
            'number': items.number,
            'has_next': items.has_next(),
            'num_pages': items.paginator.num_pages
        }
        if items.has_previous():
            pagination['previous_page_number'] = items.previous_page_number()
        if items.has_next():
            pagination['next_page_number'] = items.next_page_number()
        data['pagination'] = pagination
        data['recordsTotal'] = items.paginator.count
        data['recordsFiltered'] = items.paginator.count

    data['is_paginated'] = is_paginated

    return data


def get_messages_group(request):
    messages_group = {}
    reference_date = datetime(1980, 10, 25, 0, 0, 0, 0)

    got_messages = messages.get_messages(request)
    if got_messages:
        for message in got_messages:
            time_elapsed = datetime.now() - reference_date
            identity = str(time_elapsed.days).strip() + str(time_elapsed.microseconds).strip()
            if identity in messages_group:
                x = 1
                while identity in messages_group:
                    identity = str(time_elapsed.days).strip() + str(time_elapsed.microseconds + x).strip()
                    x = x + 1

            messages_group[identity] = {'type': message.tags, 'title': str(message)}

    return messages_group


def event_log(user_id, action, access, comment=None):
    audit = Audit()
    audit.user_id = user_id
    audit.action = action
    audit.access = access
    audit.comment = comment

    audit.save()


def get_customer_category(search):
    if search:
        items = list(CustomerCategory.objects.filter(active=True).filter(
            Q(code__icontains=search) |
            Q(description__icontains=search)
        ).distinct().order_by('description').values('id', 'code', 'description'))[0:10]
    else:
        items = list(CustomerCategory.objects.filter(active=True).order_by('description').values(
            'id', 'code', 'description'
        ))[0:10]

    new_items = []
    for item in items:
        new_items.append({'id': item['id'], 'text': item['code'] + ', ' + item['description']})

    return new_items


def get_family_group(search):
    if search:
        items = list(FamilyGroup.objects.filter(active=True).filter(
            Q(code__icontains=search) |
            Q(description__icontains=search)
        ).distinct().order_by('description').values('id', 'code', 'description'))[0:10]
    else:
        items = list(FamilyGroup.objects.filter(active=True).order_by('description').values(
            'id', 'code', 'description'
        ))[0:10]

    new_items = []
    for item in items:
        new_items.append({'id': item['id'], 'text': item['code'] + ', ' + item['description']})

    return new_items


def get_family_activity(search):
    if search:
        items = list(FamilyActivity.objects.filter(active=True).filter(
            Q(code__icontains=search) |
            Q(description__icontains=search)
        ).distinct().order_by('description').values('id', 'code', 'description'))[0:10]
    else:
        items = list(FamilyActivity.objects.filter(active=True).order_by('description').values(
            'id', 'code', 'description'
        ))[0:10]

    new_items = []
    for item in items:
        new_items.append({'id': item['id'], 'text': item['code'] + ', ' + item['description']})

    return new_items


def get_family(search):
    if search:
        items = list(Family.objects.filter(active=True).filter(
            Q(code__icontains=search) |
            Q(description__icontains=search)
        ).distinct().order_by('description').values('id', 'code', 'description'))[0:10]
    else:
        items = list(Family.objects.filter(active=True).order_by('description').values(
            'id', 'code', 'description'
        ))[0:10]

    new_items = []
    for item in items:
        new_items.append({'id': item['id'], 'text': item['code'] + ', ' + item['description']})

    return new_items


def get_measurement(search):
    if search:
        items = list(Measurement.objects.filter(active=True).filter(
            Q(code__icontains=search) |
            Q(description__icontains=search)
        ).distinct().order_by('description').values('id', 'code', 'description'))[0:10]
    else:
        items = list(Measurement.objects.filter(active=True).order_by('description').values(
            'id', 'code', 'description'
        ))[0:10]

    new_items = []
    for item in items:
        new_items.append({'id': item['id'], 'text': item['code'] + ', ' + item['description']})

    return new_items


def get_product(search):
    if search:
        items = list(Product.objects.filter(active=True).filter(
            Q(code__icontains=search) |
            Q(description__icontains=search)
        ).distinct().order_by('description').values('id', 'code', 'description'))[0:10]
    else:
        items = list(Product.objects.filter(active=True).order_by('description').values(
            'id', 'code', 'description'
        ))[0:10]

    new_items = []
    for item in items:
        new_items.append({'id': item['id'], 'text': item['code'] + ', ' + item['description']})

    return new_items


def get_store(search):
    if search:
        items = list(Store.objects.filter(active=True).filter(
            Q(code__icontains=search) |
            Q(description__icontains=search)
        ).distinct().order_by('description').values('id', 'code', 'description'))[0:10]
    else:
        items = list(Store.objects.filter(active=True).order_by('description').values('id', 'code', 'description'))[
                0:10]

    new_items = []
    for item in items:
        new_items.append({'id': item['id'], 'text': item['code'] + ', ' + item['description']})

    return new_items


def get_area(search, store=None):
    if search:
        items = list(Area.objects.filter(active=True, store_id=store).filter(
            Q(code__icontains=search) |
            Q(description__icontains=search)
        ).distinct().order_by('description').values('id', 'code', 'description'))[0:10]
    else:
        items = list(Store.objects.filter(active=True, store_id=store).order_by('description').
                     values('id', 'code', 'description'))[0:10]

    new_items = []
    for item in items:
        new_items.append({'id': item['id'], 'text': item['code'] + ', ' + item['description']})

    return new_items


def get_location(search, area=None):
    if search:
        items = list(Location.objects.filter(active=True, area_id=area).filter(
            Q(code__icontains=search) |
            Q(description__icontains=search)
        ).distinct().order_by('description').values('id', 'code', 'description'))[0:10]
    else:
        items = list(Location.objects.filter(active=True, area_id=area).order_by('description').
                     values('id', 'code', 'description'))[0:10]

    new_items = []
    for item in items:
        # new_items.append({'id': item['id'], 'text': item['code'] + ', ' + item['description']})
        new_items.append({'id': item['id'], 'value': item['description']})

    return new_items


def get_supplier(search):
    if search:
        items = list(Supplier.objects.filter(active=True).filter(
            Q(code__icontains=search) |
            Q(description__icontains=search)
        ).distinct().order_by('description').values('id', 'code', 'description'))[0:10]
    else:
        items = list(Supplier.objects.filter(active=True).order_by('description').
                     values('id', 'code', 'description'))[0:10]

    new_items = []
    for item in items:
        new_items.append({'id': item['id'], 'text': item['code'] + ', ' + item['description']})

    return new_items


def get_customer(search):
    if search:
        items = list(Customer.objects.filter(active=True).filter(
            Q(code__icontains=search) |
            Q(description__icontains=search)
        ).distinct().order_by('description').values('id', 'code', 'description'))[0:10]
    else:
        items = list(Customer.objects.filter(active=True).order_by('description').
                     values('id', 'code', 'description'))[0:10]

    new_items = []
    for item in items:
        new_items.append({'id': item['id'], 'text': item['code'] + ', ' + item['description']})

    return new_items


def get_purchase_product(search):
    if search:
        items = list(ProductConversion.objects.filter(active=True).filter(
            Q(product__code__icontains=search) |
            Q(product__description__icontains=search)
        ).distinct().order_by(
            'product__description'
        ).values(
            'id', 'product_id', 'product__code', 'product__description', 'measurement__description'
        ))[0:10]
    else:
        items = list(ProductConversion.objects.filter(active=True).order_by(
            'product__description'
        ).values(
            'id', 'product_id', 'product__code', 'product__description', 'measurement__description'
        ))[0:10]

    new_items = []
    for item in items:
        new_items.append({
            'id': item['id'],
            'primary_id': item['product_id'],
            'product': item['product__description'] + ', ' + item['measurement__description'],
            'text': item['product__code'] + ', ' + item['product__description'] + ', ' +
                    item['measurement__description']
        })

    return new_items


def get_sale_product(search, area):
    if search:
        items = ProductConversion.objects.filter(active=True).filter(
            Q(product__code__icontains=search) |
            Q(product__description__icontains=search)
        ).distinct().order_by('product__description')[0:10]
    else:
        items = ProductConversion.objects.filter(active=True).order_by('product__description')[0:10]

    data = []
    for i in items:
        item = i.to_json()
        item['text'] = i.product.code + ', ' + i.product.description + ', ' + i.measurement.description
        item['primary_id'] = i.product_id
        item['product'] = i.product.description + ', ' + i.measurement.description
        item['price'] = round(i.product.sale_price * i.value, 2)
        item['available'] = 0
        for s in Stock.objects.filter(product_id=i.product.id, area_id=area, actual_quantity__gt=0):
            item['available'] += s.actual_quantity

        if item['available'] > 0:
            item['available'] = round(item['available'] / i.value, 5)
            data.append(item)

    return data


def get_sale(search):
    if search:
        items = TransactionSummary.objects.filter(transaction_type=2).filter(
            Q(document__icontains=search) |
            Q(customer__description__icontains=search)
        ).distinct().order_by('document')[0:10]
    else:
        items = TransactionSummary.objects.filter(transaction_type=2).order_by('document')[0:10]

    data = []
    for i in items:
        item = i.to_json()
        item['text'] = i.document + ', ' + i.customer.description
        item['customer_id'] = i.customer.id
        item['customer'] = i.customer.description
        item['source_document'] = i.source_document
        item['store_id'] = i.area.store_id
        item['store'] = i.area.store.description
        item['area_id'] = i.area.id
        item['area'] = i.area.description
        detail = []
        for d in TransactionDetail.objects.filter(summary_id=i.id, quantity__gt=F('returned_quantity')):
            cost_price = round(d.cost_price / d.product_conversion.value, 2)
            possible_quantity = 0
            for s in d.product_conversion.product.stocks_product.filter(
                area=i.area, cost_price=cost_price, output_quantity__gt=F('output_return_quantity')
            ):
                possible_quantity += s.output_quantity - s.output_return_quantity
            if possible_quantity > 0:
                if round(possible_quantity / d.product_conversion.value, 5)  < d.quantity - d.returned_quantity:
                    available_quantity = round(possible_quantity / d.product_conversion.value, 5)
                else:
                    available_quantity = d.quantity - d.returned_quantity

                detail.append(
                    {
                        'id': d.product_conversion_id,
                        'product': d.product_conversion.product.description + ', ' +
                                   d.product_conversion.measurement.description,
                        'available': available_quantity,
                        'price': d.sale_price,
                        'cost_price': d.cost_price
                     }
                )

        item['detail'] = detail
        if detail.__len__() > 0:
            data.append(item)

    return data


def get_purchase(search):
    if search:
        items = TransactionSummary.objects.filter(transaction_type=1).filter(
            Q(document__icontains=search) |
            Q(customer__description__icontains=search)
        ).distinct().order_by('document')[0:10]
    else:
        items = TransactionSummary.objects.filter(transaction_type=1).order_by('document')[0:10]

    data = []
    for i in items:
        item = i.to_json()
        item['text'] = i.document + ', ' + i.supplier.description
        item['supplier_id'] = i.supplier.id
        item['supplier'] = i.supplier.description
        item['source_document'] = i.source_document
        item['store_id'] = i.area.store_id
        item['store'] = i.area.store.description
        item['area_id'] = i.area.id
        item['area'] = i.area.description
        detail = []
        for d in TransactionDetail.objects.filter(summary_id=i.id, quantity__gt=F('returned_quantity')):
            cost_price = round(d.cost_price / d.product_conversion.value, 2)
            possible_quantity = 0
            for s in d.product_conversion.product.stocks_product.filter(
                area=i.area, cost_price=cost_price, input_quantity__gt=F('input_return_quantity')
            ):
                possible_quantity += s.input_quantity - s.input_return_quantity
            if possible_quantity > 0:
                if round(possible_quantity / d.product_conversion.value, 5)  < d.quantity - d.returned_quantity:
                    available_quantity = round(possible_quantity / d.product_conversion.value, 5)
                else:
                    available_quantity = d.quantity - d.returned_quantity

                detail.append({'id': d.product_conversion_id,
                               'product': d.product_conversion.product.description + ', ' +
                                          d.product_conversion.measurement.description,
                               'available': available_quantity,
                               'price': d.cost_price,
                               'cost_price': d.cost_price})

        item['detail'] = detail
        if detail.__len__() > 0:
            data.append(item)

    return data


def get_positive_adjustment_product(search, area):
    if search:
        items = ProductConversion.objects.filter(active=True).filter(
            Q(product__code__icontains=search) |
            Q(product__description__icontains=search)
        ).distinct().order_by('product__description')[0:10]
    else:
        items = ProductConversion.objects.filter(active=True).order_by('product__description')[0:10]

    data = []
    for i in items:
        item = i.to_json()
        item['text'] = i.product.code + ', ' + i.product.description + ', ' + i.measurement.description
        item['primary_id'] = i.product_id
        item['product'] = i.product.description + ', ' + i.measurement.description
        item['available'] = 0

        stock = Stock.objects.filter(product_id=i.product.id, area_id=area)
        if len(stock) > 0:
            item['price'] = round(stock.last().cost_price * i.value, 2)
            for s in stock:
                item['available'] += s.actual_quantity

            if item['available'] > 0:
                item['available'] = round(item['available'] / i.value, 5)

            data.append(item)

    return data


def get_negative_adjustment_product(search, area):
    if search:
        items = ProductConversion.objects.filter(active=True).filter(
            Q(product__code__icontains=search) |
            Q(product__description__icontains=search)
        ).distinct().order_by('product__description')[0:10]
    else:
        items = ProductConversion.objects.filter(active=True).order_by('product__description')[0:10]

    data = []
    for i in items:
        if Stock.objects.filter(product_id=i.product.id, area_id=area, actual_quantity__gt=0).exists():
            for s in Stock.objects.filter(
                    product_id=i.product.id, area_id=area, actual_quantity__gt=0
            ).order_by('product_id', 'cost_price').distinct('product_id', 'cost_price'):
                item = i.to_json()
                item['text'] = i.product.code + ', ' + i.product.description + ', ' + i.measurement.description + \
                               ' --> ' + str(_('Cost price: ')) + str(round(s.cost_price * i.value, 2))
                item['primary_id'] = i.product_id
                item['product'] = i.product.description + ', ' + i.measurement.description
                item['primary_price'] = s.cost_price
                item['price'] = round(s.cost_price * i.value, 2)
                item['available'] = 0

                for t in Stock.objects.filter(product_id=s.product_id, area_id=s.area_id, cost_price=s.cost_price):
                    item['available'] += t.actual_quantity

                item['available'] = round(item['available'] / i.value, 5)
                data.append(item)

    return data


def build_transaction(request, form):
    try:
        with transaction.atomic():
            transact = json.loads(request.POST.get('transaction'))

            tn = TransactionNumber.objects.get(transaction_type=int(transact['type']))
            tn.number += 1
            tn.save()
            sn = str(tn.number)
            x = 6 - sn.__len__()
            while x != 0:
                x = x - 1
                sn = '0' + sn
            document = str(datetime.now().year) + sn

            summary = form.save(commit=False)
            summary.transaction_type = int(transact['type'])
            summary.area_id = int(transact['area'])
            summary.user = User.objects.get(username=request.user)
            summary.document = document
            summary.save()

            positive_value_products = []
            negative_value_products = []

            for product in transact['products']:
                if summary.transaction_type == 1:
                    detail = TransactionDetail()
                    detail.summary_id = summary.id
                    detail.product_conversion_id = int(product['id'])
                    detail.quantity = float(product['quantity'])
                    detail.cost_price = float(product['price'])

                    detail.save()

                    pc = ProductConversion.objects.get(id=int(product['id']))
                    cost_price = round(float(product['price']) / float(pc.value), 2)
                    quantity = round(float(product['quantity']) * float(pc.value), 5)

                    stock = Stock()
                    stock.product_id = pc.product_id
                    stock.area_id = int(transact['area'])
                    stock.location_id = int(product['location_id'])
                    stock.cost_price = cost_price
                    stock.input_date = transact['date']
                    stock.input_quantity = quantity
                    stock.input_value = round(quantity * cost_price, 2)
                    stock.actual_date = transact['date']
                    stock.actual_quantity = quantity
                    stock.actual_value = round(quantity * cost_price, 2)

                    stock.save()

                if summary.transaction_type == 2:
                    pc = ProductConversion.objects.get(id=int(product['id']))
                    quantity = round(float(product['quantity']) * float(pc.value), 5)

                    for prod in Stock.objects.filter(
                            product_id=pc.product_id, area=summary.area, actual_quantity__gt=0
                    ).order_by('input_date'):
                        detail = TransactionDetail()
                        detail.summary_id = summary.id
                        detail.product_conversion_id = int(product['id'])
                        detail.actual_quantity = round(prod.actual_quantity / pc.value, 5)
                        detail.cost_price = round(prod.cost_price * pc.value, 2)
                        detail.sale_price = float(product['price'])

                        prod.output_date = transact['date']
                        prod.actual_date = transact['date']

                        if prod.actual_quantity >= quantity:
                            detail.quantity = round(quantity / float(pc.value), 5)
                            detail.save()

                            prod.output_quantity = float(prod.output_quantity) + quantity
                            prod.output_value = float(prod.output_value) + round(quantity * float(prod.cost_price), 2)
                            prod.actual_quantity = Decimal(float(prod.actual_quantity) - quantity)
                            summed_value = Decimal(
                                float(prod.actual_value) - round(quantity * float(prod.cost_price), 2)
                            )
                            quantity = 0
                        else:
                            available = prod.actual_quantity
                            detail.quantity = round(available / pc.value, 5)
                            detail.save()

                            prod.output_quantity += available
                            prod.output_value += round(available * prod.cost_price, 2)
                            prod.actual_quantity -= available
                            summed_value = prod.actual_value - round(available * prod.cost_price, 2)
                            quantity -= float(available)

                        prod.actual_value = round(prod.actual_quantity * prod.cost_price, 2)
                        difference = round(prod.actual_value - summed_value, 2)

                        if difference > 0:
                            print('difference > 0')
                            print('Code: {0}, Descripction: {1}'.format(prod.product.code, prod.product.description))
                            print('actual value: {0} --> summed value: {1}'.format(prod.actual_value, summed_value))
                            print(difference)
                            prod.input_adjustment_value += difference
                            positive_value_products.append({
                                'id': detail.product_conversion_id,
                                'actual_quantity': prod.actual_quantity,
                                'cost_price': difference
                            })
                        elif difference < 0:
                            print('difference < 0')
                            print('Code: {0}, Descripction: {1}'.format(prod.product.code, prod.product.description))
                            print('actual value: {0} --> summed value: {1}'.format(prod.actual_value, summed_value))
                            print(difference)
                            prod.output_adjustment_value += abs(difference)
                            negative_value_products.append({
                                'id': detail.product_conversion_id,
                                'actual_quantity': prod.actual_quantity,
                                'cost_price': difference
                            })

                        prod.save()

                        if quantity == 0:
                            break

                if summary.transaction_type == 3:
                    pc = ProductConversion.objects.get(id=int(product['id']))
                    devolution = float(product['quantity'])
                    quantity = round(float(product['quantity']) * float(pc.value), 5)

                    for det in TransactionDetail.objects.filter(
                        summary_id=int(transact['source_summary']), product_conversion=pc
                    ):
                        if devolution <= det.quantity - det.returned_quantity:
                            det.returned_quantity = float(det.returned_quantity) + devolution
                            det.save()
                            devolution = 0
                        else:
                            available = det.quantity - det.returned_quantity
                            det.returned_quantity += available
                            det.save()
                            devolution -= float(available)

                    cost_price = round(float(product['cost_price']) / float(pc.value), 2)
                    for prod in Stock.objects.filter(product_id=pc.product_id, area=summary.area,
                                                     cost_price=cost_price,
                                                     output_quantity__gt=F('output_return_quantity')
                    ).order_by('-output_date'):
                        available = prod.output_quantity - prod.output_return_quantity

                        detail = TransactionDetail()
                        detail.summary_id = summary.id
                        detail.product_conversion_id = int(product['id'])
                        detail.actual_quantity = round(prod.actual_quantity / pc.value, 5)
                        detail.cost_price = round(prod.cost_price * pc.value, 2)
                        detail.sale_price = float(product['price'])

                        prod.output_return_date = transact['date']
                        prod.actual_date = transact['date']

                        if available > quantity:
                            detail.quantity = round(quantity / float(pc.value), 5)
                            detail.save()

                            prod.output_return_quantity = float(prod.output_return_quantity) + quantity
                            prod.output_return_value = float(prod.output_return_value) + round(
                                quantity * float(prod.cost_price), 2
                            )
                            prod.actual_quantity = float(prod.actual_quantity) +  quantity
                            summed_value = Decimal(
                                float(prod.actual_value) + round(quantity * float(prod.cost_price), 2)
                            )
                            quantity = 0
                        else:
                            detail.quantity = round(available / pc.value, 5)
                            detail.save()

                            prod.output_return_quantity += available
                            prod.output_return_value += round(available * prod.cost_price, 2)
                            prod.actual_quantity += available
                            summed_value = prod.actual_value + round(available * prod.cost_price, 2)
                            quantity -= float(available)

                        prod.actual_value = round(prod.actual_quantity * prod.cost_price, 2)
                        difference = prod.actual_value - summed_value

                        if difference > 0:
                            prod.input_adjustment_value += difference
                            positive_value_products.append({
                                'id': detail.product_conversion_id,
                                'actual_quantity': prod.actual_quantity,
                                'cost_price': difference
                            })
                        elif difference < 0:
                            prod.output_adjustment_value += abs(difference)
                            negative_value_products.append({
                                'id': detail.product_conversion_id,
                                'actual_quantity': prod.actual_quantity,
                                'cost_price': difference
                            })

                        prod.save()

                        if quantity == 0:
                            break

                if summary.transaction_type == 4:
                    pc = ProductConversion.objects.get(id=int(product['id']))
                    devolution = float(product['quantity'])
                    quantity = round(float(product['quantity']) * float(pc.value), 5)

                    for det in TransactionDetail.objects.filter(
                        summary_id=int(transact['source_summary']), product_conversion=pc
                    ):
                        if devolution <= det.quantity - det.returned_quantity:
                            det.returned_quantity = float(det.returned_quantity) + devolution
                            det.save()
                            devolution = 0
                        else:
                            available = det.quantity - det.returned_quantity
                            det.returned_quantity += available
                            det.save()
                            devolution -= float(available)

                    cost_price = round(float(product['cost_price']) / float(pc.value), 2)
                    for prod in Stock.objects.filter(product_id=pc.product_id, area=summary.area,
                                                     cost_price=cost_price,
                                                     input_quantity__gt=F('input_return_quantity')
                    ).order_by('-input_date'):
                        if prod.actual_quantity < prod.input_quantity - prod.input_return_quantity:
                            available = prod.actual_quantity
                        else:
                            available = prod.input_quantity - prod.input_return_quantity

                        detail = TransactionDetail()
                        detail.summary_id = summary.id
                        detail.product_conversion_id = int(product['id'])
                        detail.actual_quantity = round(prod.actual_quantity / pc.value, 5)
                        detail.cost_price = round(prod.cost_price * pc.value, 2)

                        prod.input_return_date = transact['date']
                        prod.actual_date = transact['date']

                        if available > quantity:
                            detail.quantity = round(quantity / float(pc.value), 5)
                            detail.save()

                            prod.input_return_quantity = float(prod.input_return_quantity) + quantity
                            prod.input_return_value = float(prod.input_return_value) + round(
                                quantity * float(prod.cost_price), 2
                            )
                            prod.actual_quantity = float(prod.actual_quantity) -  quantity
                            prod.actual_value = float(prod.actual_value) - round(quantity * float(prod.cost_price), 2)
                            prod.save()
                            quantity = 0
                        else:
                            available = prod.actual_quantity
                            detail.quantity = round(available / pc.value, 5)
                            detail.save()

                            prod.input_return_quantity += available
                            prod.input_return_value += round(available * prod.cost_price, 2)
                            prod.actual_quantity -= available
                            prod.actual_value -= round(available * prod.cost_price, 2)
                            prod.save()
                            quantity -= float(available)
                        if quantity == 0:
                            break

                if summary.transaction_type == 5:
                    pc = ProductConversion.objects.get(id=int(product['id']))
                    quantity = round(float(product['quantity']) * float(pc.value), 5)

                    prod = Stock.objects.filter(product_id=pc.product_id, area=summary.area).last()

                    detail = TransactionDetail()
                    detail.summary_id = summary.id
                    detail.product_conversion_id = int(product['id'])
                    detail.actual_quantity = round(prod.actual_quantity / pc.value, 5)
                    detail.cost_price = round(prod.cost_price * pc.value, 2)
                    detail.quantity = float(product['quantity'])
                    detail.save()

                    prod.input_adjustment_date = transact['date']
                    prod.actual_date = transact['date']

                    prod.input_adjustment_quantity = float(prod.input_adjustment_quantity) + quantity
                    prod.input_adjustment_value = float(prod.input_adjustment_value) + round(
                        quantity * float(prod.cost_price), 2
                    )
                    prod.actual_quantity = float(prod.actual_quantity) + quantity
                    prod.actual_value = float(prod.actual_value) + round(quantity * float(prod.cost_price), 2)
                    prod.save()

                if summary.transaction_type == 6:
                    pc = ProductConversion.objects.get(id=int(product['id']))
                    quantity = round(float(product['quantity']) * float(pc.value), 5)
                    print('Ajuste negativo --> Product: {0}, Measurement: {1}'.format(
                        pc.product.description, pc.measurement
                    ))
                    print('product_id: {0}'.format(pc.product_id))
                    print('area: {0}'.format(summary.area))
                    print('cost_price: {0}'.format(Decimal(product['primary_price'])))

                    for prod in Stock.objects.filter(
                            product_id=pc.product_id, area=summary.area, cost_price=Decimal(product['primary_price']),
                            actual_quantity__gt=0
                    ).order_by('input_date'):
                        detail = TransactionDetail()
                        detail.summary_id = summary.id
                        detail.product_conversion_id = int(product['id'])
                        detail.actual_quantity = round(prod.actual_quantity / pc.value, 5)
                        detail.cost_price = round(prod.cost_price * pc.value, 2)

                        prod.output_adjustment_date = transact['date']
                        prod.actual_date = transact['date']

                        if prod.actual_quantity > quantity:
                            detail.quantity = float(product['quantity'])
                            detail.save()

                            prod.output_adjustment_quantity = float(prod.output_adjustment_quantity) + quantity
                            prod.output_adjustment_value = float(prod.output_adjustment_value) + \
                                                           round(quantity * float(prod.cost_price), 2)
                            prod.actual_quantity = float(prod.actual_quantity) - quantity
                            prod.actual_value = float(prod.actual_value) - round(quantity * float(prod.cost_price), 2)
                            prod.save()
                            quantity = 0
                        else:
                            available = prod.actual_quantity
                            detail.quantity = round(available / pc.value, 5)
                            detail.save()

                            prod.output_adjustment_quantity += available
                            prod.output_adjustment_value += round(available * prod.cost_price, 2)
                            prod.actual_quantity -= available
                            prod.actual_value -= round(available * prod.cost_price, 2)
                            prod.save()
                            quantity -= float(available)
                        if quantity == 0:
                            break

            data = {
                'summary': summary,
                'status': 'ok'
            }

            value_adjustments = []
            if len(positive_value_products) > 0 or len(negative_value_products) > 0:
                comment = 'Source transaction type: {0}'.format(summary.get_transaction_type_display())
            if len(positive_value_products) > 0:
                adjust = build_value_adjustment_transaction(
                    7,summary.area_id, request.user, summary.document, summary.date, comment, positive_value_products
                )
                if adjust['status'] == 'ok':
                    event_log(User.objects.get(username=request.user).id, 1,
                              'apps.accounting.views.CreatePositiveValueAdjustment', 'summary_id: ' +
                              str(adjust['summary'].id) + ' | transaction_type: ' +
                              str(adjust['summary'].transaction_type) + ' | document: ' + adjust['summary'].document +
                              ' | date: ' + adjust['summary'].date.strftime('%Y-%m-%d'))
                if not adjust['summary'] is None:
                    value_adjustments.append({
                        'type': 'positive',
                        'transact_id': adjust['summary'].id
                    })
            if len(negative_value_products) > 0:
                adjust = build_value_adjustment_transaction(
                    8, summary.area_id, request.user, summary.document, summary.date, comment, negative_value_products
                )
                if adjust['status'] == 'ok':
                    event_log(User.objects.get(username=request.user).id, 1,
                              'apps.accounting.views.CreateNegativeValueAdjustment', 'summary_id: ' +
                              str(adjust['summary'].id) + ' | transaction_type: ' +
                              str(adjust['summary'].transaction_type) + ' | document: ' + adjust['summary'].document +
                              ' | date: ' + adjust['summary'].date.strftime('%Y-%m-%d'))
                if not adjust['summary'] is None:
                    value_adjustments.append({
                        'type': 'negative',
                        'transact_id': adjust['summary'].id
                    })
            if len(value_adjustments) > 0:
                data['value_adjustments'] = value_adjustments

            return data

    except Exception as e:
        print('build_transaction')
        print(e)

        data = {
            'summary': None,
            'status': 'ko',
        }

        return data


def build_value_adjustment_transaction(type, area, user, source, date, comment, products):
    try:
        with transaction.atomic():
            tn = TransactionNumber.objects.get(transaction_type=type)
            tn.number += 1
            tn.save()
            sn = str(tn.number)
            x = 6 - sn.__len__()
            while x != 0:
                x = x - 1
                sn = '0' + sn
            document = str(datetime.now().year) + sn

            summary = TransactionSummary()
            summary.transaction_type = type
            summary.area_id = area
            summary.user = User.objects.get(username=user)
            summary.document = document
            summary.source_document = source
            summary.date = date
            summary.comment = comment
            summary.save()

            for product in products:
                pc = ProductConversion.objects.get(id=product['id'])

                detail = TransactionDetail()
                detail.summary_id = summary.id
                detail.product_conversion_id = product['id']
                detail.actual_quantity = round(product['actual_quantity'] / pc.value, 5)
                detail.cost_price = round(product['cost_price'] * pc.value, 2)
                detail.save()

            data = {
                'summary': summary,
                'status': 'ok'
            }

            return data

    except Exception as e:
        print('build_value_adjustment_transaction')
        print(e)

        data = {
            'summary': None,
            'status': 'ko'
        }

        return data


def get_daily_sales():
    data = []
    year = datetime.now().year
    month = datetime.now().month
    try:
        for s in Store.objects.filter(active=True):
            x = len(data) - ((len(data) // len(colors)) * len(colors))
            item = {
                'label': s.description,
                'backgroundColor': colors[x][1],
                'borderColor': colors[x][1],
                'data': []
            }

            for n in range(1, 32):
                # Comprehension list sum
                sale = sum(
                    round((d.quantity - d.returned_quantity) * d.sale_price, 2)
                    for d in TransactionDetail.objects.filter(
                        summary__transaction_type=2, summary__area__store_id=s.id, summary__date__year=year,
                        summary__date__month=month, summary__date__day=n)
                )

                item['data'].append(sale)

            data.append(item)
    except Exception as e:
        print('Exception:', str(e))

    return data


def get_monthly_sales():
    data = []
    year = datetime.now().year
    try:
        for s in Store.objects.filter(active=True):
            x = len(data) - ((len(data) // len(colors)) * len(colors))
            item = {
                'label': s.description,
                'backgroundColor': colors[x][1],
                'borderColor': colors[x][1],
                'borderWidth': 1,
                'data': []
            }

            for m in range(1, 13):
                # Comprehension list sum
                sale = sum(
                    round((d.quantity - d.returned_quantity) * d.sale_price, 2)
                    for d in TransactionDetail.objects.filter(
                        summary__transaction_type=2, summary__area__store_id=s.id, summary__date__year=year,
                        summary__date__month=m)
                )

                item['data'].append(sale)

            data.append(item)
    except Exception as e:
        print('Exception:', str(e))

    return data


def get_product_sales():
    labels = []
    data = []
    backgroundColor = []
    datasets = []
    year = datetime.now().year
    data_unsorted = []
    try:
        for p in Product.objects.filter(active=True):
            # Comprehension list sum
            profit = sum(
                (round((d.quantity - d.returned_quantity) * d.sale_price, 2))
                for d in TransactionDetail.objects.filter(
                    summary__transaction_type=2, product_conversion__product_id=p.id, summary__date__year=year)
            )
            item = {
                'label': p.description,
                'data': profit
            }

            data_unsorted.append(item)

        data_sorted = sorted(data_unsorted, key=lambda item: item['data'], reverse=True)

        for ds in data_sorted[:10]:
            if ds['data'] > 0:
                labels.append(ds['label'])
                x = len(data) - ((len(data) // len(colors)) * len(colors))
                backgroundColor.append(colors[x][0])
                data.append(ds['data'])

        item = {
            'data': data,
            'backgroundColor': backgroundColor
        }
        datasets.append(item)

        info = {
            'labels': labels,
            'datasets': datasets
        }


    except Exception as e:
        print('Exception:', str(e))

    return info


def get_product_profit():
    labels = []
    data = []
    backgroundColor = []
    datasets = []
    year = datetime.now().year
    data_unsorted = []
    try:
        for p in Product.objects.filter(active=True):
            # Comprehension list sum
            profit = sum(
                (round((d.quantity - d.returned_quantity) * d.sale_price, 2) -
                 round((d.quantity - d.returned_quantity) * d.cost_price, 2))
                for d in TransactionDetail.objects.filter(
                    summary__transaction_type=2, product_conversion__product_id=p.id, summary__date__year=year)
            )
            item = {
                'label': p.description,
                'data': profit
            }

            data_unsorted.append(item)

        data_sorted = sorted(data_unsorted, key=lambda item: item['data'], reverse=True)

        for ds in data_sorted[:10]:
            if ds['data'] > 0:
                labels.append(ds['label'])
                x = len(data) - ((len(data) // len(colors)) * len(colors))
                backgroundColor.append(colors[x][0])
                data.append(ds['data'])

        item = {
            'data': data,
            'backgroundColor': backgroundColor
        }
        datasets.append(item)

        info = {
            'labels': labels,
            'datasets': datasets
        }


    except Exception as e:
        print('Exception:', str(e))

    return info
