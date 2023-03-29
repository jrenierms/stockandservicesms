from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import *


class StoreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['autofocus'] = True

    def clean_code(self):
        data = self.cleaned_data['code']

        if 'id' in self.data:
            item_exist = Store.objects.filter(active=True, code__iexact=data).exclude(id=self.data['id']).exists()
        else:
            item_exist = Store.objects.filter(active=True, code__iexact=data).exists()

        if item_exist:
            raise ValidationError(_('The code entered is contained by at least one other record'), code='danger')

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        if 'id' in self.data:
            item_exist = Store.objects.filter(active=True, description__iexact=data).exclude(id=self.data['id']).exists()
        else:
            item_exist = Store.objects.filter(active=True, description__iexact=data).exists()

        if item_exist:
            raise ValidationError(_('The description entered is contained by at least one other record'), code='danger')

        return data

    class Meta:
        model = Store
        fields = ['code', 'description']
        labels = {
            'code': _('Code:'),
            'description': _('Description:')
        }
        help_texts = {
            'code': _('Enter a code of maximum length 10 characters'),
            'description': _('Enter a description of maximum length 30 characters')
        }
        error_messages = {
            'code': {
                'required': _('It is required to enter a code')
            },
            'description': {
                'required': _('It is required to enter a description')
            }
        }
        widgets = {
            'code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('code'),
                    'id': 'code',
                    'name': 'code',
                    'oninvalid': 'validate("code", "TextInput")',
                    'onkeyup': 'validate("code", "TextInput")'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('description'),
                    'id': 'description',
                    'name': 'description',
                    'oninvalid': 'validate("description", "TextInput")',
                    'onkeyup': 'validate("description", "TextInput")'
                }
            )
        }


class AreaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['store'].widget.attrs['autofocus'] = True

    def clean_store(self):
        data = self.cleaned_data['store']

        if data is None:
            raise ValidationError(_('It is required to select a store'), code='danger')

        return data

    def clean_code(self):
        data = self.cleaned_data['code']

        if 'id' in self.data:
            item_exist = Area.objects.filter(active=True, code__iexact=data).exclude(id=self.data['id']).exists()
        else:
            item_exist = Area.objects.filter(active=True, code__iexact=data).exists()

        if item_exist:
            raise ValidationError(_('The code entered is contained by at least one other record'), code='danger')

        return data

    def clean_description(self):
        data = self.cleaned_data['description']
        data_store = self.data['store']
        if data_store == '':
            data_store = None

        if 'id' in self.data:
            item_exist = Area.objects.filter(
                active=True, description__iexact=data, store_id=data_store
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = Area.objects.filter(
                active=True, description__iexact=data, store_id=data_store
            ).exists()

        if item_exist:
            raise ValidationError(_('The description entered is contained by at least one other record'), code='danger')

        return data

    class Meta:
        model = Area
        fields = ['store', 'code', 'description']
        labels = {
            'store': _('Store:'),
            'code': _('Code:'),
            'description': _('Description:')
        }
        help_texts = {
            'store': _('Select a store associated with the area'),
            'code': _('Enter a code of maximum length 10 characters'),
            'description': _('Enter a description of maximum length 150 characters')
        }
        error_messages = {
            'store': {
                'required': _('It is required to select a store')
            },
            'code': {
                'required': _('It is required to enter a code')
            },
            'description': {
                'required': _('It is required to enter a description')
            }
        }
        widgets = {
            'store': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'store',
                    'name': 'store',
                    'onchange': 'validate("store", "Select")'
                }
            ),
            'code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('code'),
                    'id': 'code',
                    'name': 'code',
                    'oninvalid': 'validate("code", "TextInput")',
                    'onkeyup': 'validate("code", "TextInput")'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('description'),
                    'id': 'description',
                    'name': 'description',
                    'oninvalid': 'validate("description", "TextInput")',
                    'onkeyup': 'validate("description", "TextInput")'
                }
            )
        }


class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['store'].widget.attrs['autofocus'] = True

    store = forms.ModelChoiceField(label=_('Store:'),
                                   help_text=_('Select a store associated with the area'),
                                   error_messages={
                                       'required': _('It is required to select a store')
                                   },
                                   queryset=Store.objects.filter(active=True),
                                   widget=forms.Select(
                                       attrs={
                                           'class': 'form-control select2',
                                           'id': 'store',
                                           'name': 'store',
                                           'onchange': 'validate("store", "Select")'
                                       }
                                   ))

    def clean_store(self):
        data = self.cleaned_data['store']

        if data is None:
            raise ValidationError(_('It is required to select a store'), code='danger')

        return data

    def clean_area(self):
        data = self.cleaned_data['area']

        if data is None:
            raise ValidationError(_('It is required to select an area'), code='danger')

        return data

    def clean_code(self):
        data = self.cleaned_data['code']

        if 'id' in self.data:
            item_exist = Location.objects.filter(active=True, code__iexact=data).exclude(id=self.data['id']).exists()
        else:
            item_exist = Location.objects.filter(active=True, code__iexact=data).exists()

        if item_exist:
            raise ValidationError(_('The code entered is contained by at least one other record'), code='danger')

        return data

    def clean_description(self):
        data = self.cleaned_data['description']
        data_area = self.data['area']
        if data_area == '':
            data_area = None

        if 'id' in self.data:
            item_exist = Location.objects.filter(
                active=True, description__iexact=data, area__id=data_area
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = Location.objects.filter(
                active=True, description__iexact=data, area__id=data_area
            ).exists()

        if item_exist:
            raise ValidationError(_('The description entered is contained by at least one other record'), code='danger')

        return data

    class Meta:
        model = Location
        fields = ['area', 'code', 'description']
        labels = {
            'area': _('Area:'),
            'code': _('Code:'),
            'description': _('Description:')
        }
        help_texts = {
            'area': _('Select a area associated with the location'),
            'code': _('Enter a code of maximum length 10 characters'),
            'description': _('Enter a description of maximum length 150 characters')
        }
        error_messages = {
            'area': {
                'required': _('It is required to select an area')
            },
            'code': {
                'required': _('It is required to enter a code')
            },
            'description': {
                'required': _('It is required to enter a description')
            }
        }
        widgets = {
            'area': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'area',
                    'name': 'area',
                    'onchange': 'validate("area", "Select")'
                }
            ),
            'code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('code'),
                    'id': 'code',
                    'name': 'code',
                    'oninvalid': 'validate("code", "TextInput")',
                    'onkeyup': 'validate("code", "TextInput")'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('description'),
                    'id': 'description',
                    'name': 'description',
                    'oninvalid': 'validate("description", "TextInput")',
                    'onkeyup': 'validate("description", "TextInput")'
                }
            )
        }


class PurchaseSummaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['store'].widget.attrs['autofocus'] = True

    store = forms.ModelChoiceField(label=_('Store:'),
                                   help_text=_('Select a store associated with the purchase'),
                                   error_messages={
                                       'required': _('It is required to select a store')
                                   },
                                   queryset=Store.objects.filter(active=True),
                                   widget=forms.Select(
                                       attrs={
                                           'class': 'form-control select2',
                                           'id': 'store',
                                           'name': 'store',
                                           'onchange': 'validate("store", "Select")'
                                       }
                                   ))

    def clean_supplier(self):
        data = self.cleaned_data['supplier']

        if data is None:
            raise ValidationError(_('It is required to select a supplier'), code='danger')

        return data

    def clean_store(self):
        data = self.cleaned_data['store']

        if data is None:
            raise ValidationError(_('It is required to select a store'), code='danger')

        return data

    def clean_area(self):
        data = self.cleaned_data['area']

        if data is None:
            raise ValidationError(_('It is required to select an area'), code='danger')

        return data

    class Meta:
        model = TransactionSummary
        fields = ['supplier', 'area', 'date', 'source_document', 'comment']
        labels = {
            'supplier': _('Supplier:'),
            'area': _('Area:'),
            'date': _('Date:'),
            'source_document': _('Source document:'),
            'comment': _('Comment:')
        }
        help_texts = {
            'supplier': _('Select a supplier associated with the purchase'),
            'area': _('Select an area associated with the purchase'),
            'date': _('Enter a date associated with the purchase'),
            'source_document': _('Enter a source document of maximum length 20 characters'),
            'comment': _('Enter a comment associated with the purchase')
        }
        error_messages = {
            'supplier': {
                'required': _('It is required to select a supplier')
            },
            'area': {
                'required': _('It is required to select an area')
            },
            'date': {
                'required': _('It is required to enter a date')
            }
        }
        widgets = {
            'supplier': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'supplier',
                    'name': 'supplier',
                    'onchange': 'validate("supplier", "Select")'
                }
            ),
            'area': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'area',
                    'name': 'area',
                    'onchange': 'validate("area", "Select")'
                }
            ),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'placeholder': _('date with the format: yyyy-mm-dd'),
                    'id': 'date',
                    'name': 'date',
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'onkeyup': 'validate("date", "TextInput")',
                    'data-target': '#date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'source_document': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('source document'),
                    'id': 'source_document',
                    'name': 'source_document'
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': _('comment about the purchase'),
                    'id': 'comment',
                    'name': 'comment'
                }
            )
        }


class SaleSummaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['store'].widget.attrs['autofocus'] = True

    store = forms.ModelChoiceField(label=_('Store:'),
                                   help_text=_('Select a store associated with the sale'),
                                   error_messages={
                                       'required': _('It is required to select a store')
                                   },
                                   queryset=Store.objects.filter(active=True),
                                   widget=forms.Select(
                                       attrs={
                                           'class': 'form-control select2',
                                           'id': 'store',
                                           'name': 'store',
                                           'onchange': 'validate("store", "Select")'
                                       }
                                   ))

    def clean_customer(self):
        data = self.cleaned_data['customer']

        if data is None:
            raise ValidationError(_('It is required to select a customer'), code='danger')

        return data

    def clean_store(self):
        data = self.cleaned_data['store']

        if data is None:
            raise ValidationError(_('It is required to select a store'), code='danger')

        return data

    def clean_area(self):
        data = self.cleaned_data['area']

        if data is None:
            raise ValidationError(_('It is required to select an area'), code='danger')

        return data

    class Meta:
        model = TransactionSummary
        fields = ['customer', 'area', 'date', 'source_document', 'comment']
        labels = {
            'customer': _('Customer:'),
            'area': _('Area:'),
            'date': _('Date:'),
            'source_document': _('Source document:'),
            'comment': _('Comment:')
        }
        help_texts = {
            'customer': _('Select a customer associated with the sale'),
            'area': _('Select an area associated with the sale'),
            'date': _('Enter a date associated with the sale'),
            'source_document': _('Enter a source document of maximum length 20 characters'),
            'comment': _('Enter a comment associated with the sale')
        }
        error_messages = {
            'customer': {
                'required': _('It is required to select a customer')
            },
            'area': {
                'required': _('It is required to select an area')
            },
            'date': {
                'required': _('It is required to enter a date')
            }
        }
        widgets = {
            'customer': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'customer',
                    'name': 'customer',
                    'onchange': 'validate("customer", "Select")'
                }
            ),
            'area': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'area',
                    'name': 'area',
                    'onchange': 'validate("area", "Select")'
                }
            ),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'placeholder': _('date with the format: yyyy-mm-dd'),
                    'id': 'date',
                    'name': 'date',
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'onkeyup': 'validate("date", "TextInput")',
                    'data-target': '#date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'source_document': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('source document'),
                    'id': 'source_document',
                    'name': 'source_document'
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': _('comment about the sale'),
                    'id': 'comment',
                    'name': 'comment'
                }
            )
        }


class SaleReturnSummaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['autofocus'] = True

    store = forms.CharField(label=_('Store:'),
                            help_text=_('Enter a store associated with the sale return'),
                            error_messages={
                                'required': _('It is required to enter a store')
                            },
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': _('store'),
                                    'id': 'store',
                                    'name': 'store',
                                    'readonly': ''
                                }
                            ))

    def source_document(self):
        data = self.cleaned_data['source_document']

        if data is None:
            raise ValidationError(_('It is required to enter a source document'), code='danger')

        return data

    class Meta:
        model = TransactionSummary
        fields = ['customer', 'area', 'date', 'source_document', 'comment']
        labels = {
            'customer': _('Customer:'),
            'area': _('Area:'),
            'date': _('Date:'),
            'source_document': _('Source document:'),
            'comment': _('Comment:')
        }
        help_texts = {
            'customer': _('Select a customer associated with the sale return'),
            'area': _('Enter an area associated with the sale return'),
            'date': _('Enter a date associated with the sale return'),
            'source_document': _('Enter a source document of maximum length 20 characters'),
            'comment': _('Enter a comment associated with the sale return')
        }
        error_messages = {
            'customer': {
                'required': _('It is required to enter a customer')
            },
            'area': {
                'required': _('It is required to enter an area')
            },
            'date': {
                'required': _('It is required to enter a date')
            }
        }
        widgets = {
            'customer': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('customer'),
                    'id': 'customer',
                    'name': 'customer',
                    'readonly': ''
                }
            ),
            'area': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('area'),
                    'id': 'area',
                    'name': 'area',
                    'readonly': ''
                }
            ),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'placeholder': _('date with the format: yyyy-mm-dd'),
                    'id': 'date',
                    'name': 'date',
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'onkeyup': 'validate("date", "TextInput")',
                    'data-target': '#date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'source_document': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('source document'),
                    'id': 'source_document',
                    'name': 'source_document',
                    'readonly': ''
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': _('comment about the sale return'),
                    'id': 'comment',
                    'name': 'comment'
                }
            )
        }


class PurchaseReturnSummaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['autofocus'] = True

    store = forms.CharField(label=_('Store:'),
                            help_text=_('Enter a store associated with the purchase return'),
                            error_messages={
                                'required': _('It is required to enter a store')
                            },
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': _('store'),
                                    'id': 'store',
                                    'name': 'store',
                                    'readonly': ''
                                }
                            ))

    def source_document(self):
        data = self.cleaned_data['source_document']

        if data is None:
            raise ValidationError(_('It is required to enter a source document'), code='danger')

        return data

    class Meta:
        model = TransactionSummary
        fields = ['supplier', 'area', 'date', 'source_document', 'comment']
        labels = {
            'supplier': _('Supplier:'),
            'area': _('Area:'),
            'date': _('Date:'),
            'source_document': _('Source document:'),
            'comment': _('Comment:')
        }
        help_texts = {
            'supplier': _('Enter a supplier associated with the purchase return'),
            'area': _('Enter an area associated with the purchase return'),
            'date': _('Enter a date associated with the purchase return'),
            'source_document': _('Enter a source document of maximum length 20 characters'),
            'comment': _('Enter a comment associated with the purchase return')
        }
        error_messages = {
            'supplier': {
                'required': _('It is required to enter a supplier')
            },
            'area': {
                'required': _('It is required to enter an area')
            },
            'date': {
                'required': _('It is required to enter a date')
            }
        }
        widgets = {
            'supplier': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('supplier'),
                    'id': 'supplier',
                    'name': 'supplier',
                    'readonly': ''
                }
            ),
            'area': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('area'),
                    'id': 'area',
                    'name': 'area',
                    'readonly': ''
                }
            ),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'placeholder': _('date with the format: yyyy-mm-dd'),
                    'id': 'date',
                    'name': 'date',
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'onkeyup': 'validate("date", "TextInput")',
                    'data-target': '#date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'source_document': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('source document'),
                    'id': 'source_document',
                    'name': 'source_document',
                    'readonly': ''
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': _('comment about the purchase return'),
                    'id': 'comment',
                    'name': 'comment'
                }
            )
        }


class AdjustmentSummaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['autofocus'] = True

    store = forms.ModelChoiceField(label=_('Store:'),
                                   help_text=_('Select a store associated with the adjustment'),
                                   error_messages={
                                       'required': _('It is required to select a store')
                                   },
                                   queryset=Store.objects.filter(active=True),
                                   widget=forms.Select(
                                       attrs={
                                           'class': 'form-control select2',
                                           'id': 'store',
                                           'name': 'store',
                                           'onchange': 'validate("store", "Select")'
                                       }
                                   ))

    def clean_store(self):
        data = self.cleaned_data['store']

        if data is None:
            raise ValidationError(_('It is required to select a store'), code='danger')

        return data

    def clean_area(self):
        data = self.cleaned_data['area']

        if data is None:
            raise ValidationError(_('It is required to select an area'), code='danger')

        return data

    class Meta:
        model = TransactionSummary
        fields = ['area', 'date', 'source_document', 'comment']
        labels = {
            'area': _('Area:'),
            'date': _('Date:'),
            'source_document': _('Source document:'),
            'comment': _('Comment:')
        }
        help_texts = {
            'area': _('Select an area associated with the adjustment'),
            'date': _('Enter a date associated with the adjustment'),
            'source_document': _('Enter a source document of maximum length 20 characters'),
            'comment': _('Enter a comment associated with the adjustment')
        }
        error_messages = {
            'area': {
                'required': _('It is required to select an area')
            },
            'date': {
                'required': _('It is required to enter a date')
            }
        }
        widgets = {
            'area': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'area',
                    'name': 'area',
                    'onchange': 'validate("area", "Select")'
                }
            ),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'placeholder': _('date with the format: yyyy-mm-dd'),
                    'id': 'date',
                    'name': 'date',
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'onkeyup': 'validate("date", "TextInput")',
                    'data-target': '#date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'source_document': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('source document'),
                    'id': 'source_document',
                    'name': 'source_document'
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': _('comment about the adjustment'),
                    'id': 'comment',
                    'name': 'comment'
                }
            )
        }
