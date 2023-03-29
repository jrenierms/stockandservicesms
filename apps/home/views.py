from apps.base.decorators import AllowedUsers
from apps.base.texts import dialogs, message_texts, months
from apps.base.utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import View


class Home(AllowedUsers, LoginRequiredMixin, View):
    allowed_roles = ['Administrator', 'Commercial', 'Bookkeeper', 'Juridical', 'Representative']
    login_url = 'security/login'
    model = User
    template_name = 'home/index.html'
    items = None
    data = {}

    def get(self, request, *args, **kwargs):
        context = {
            'view_url': '/',
            'list_url': '/',
            'title': _('Dashboard'),
            'user_data': get_user_data(request),
            'dialogs': dialogs,
            'message_texts': message_texts,
            'data': self.data
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            if request.POST.get('action', None) == 'daily_sales':
                context = {
                    'status': 'ok',
                    'lineChartData': {
                        'labels': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14',
                                   '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28',
                                   '29', '30', '31'],
                        'datasets': get_daily_sales()
                    }
                }
            elif request.POST.get('action', None) == 'monthly_sales':
                context = {
                    'status': 'ok',
                    'barChartData': {
                        'labels': months,
                        'datasets': get_monthly_sales()
                    }
                }
            elif request.POST.get('action', None) == 'product_sales':
                context = {
                    'status': 'ok',
                    'donutData': get_product_sales()
                }
            elif request.POST.get('action', None) == 'product_profit':
                context = {
                    'status': 'ok',
                    'pieData': get_product_profit()
                }
            else:
                messages.error(request, message_texts['error']['information_load_failed'])
                context = {
                    'status': 'ko',
                    'messages_group': get_messages_group(request)
                }
        except Exception as e:
            context = {
                'status': 'ko',
                'messages_group': {'1': {'type': 'error', 'title': str(e)}}
            }

        return JsonResponse(context, safe=False)
