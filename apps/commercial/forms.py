from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import *


class CustomerCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['autofocus'] = True

    def clean_code(self):
        data = self.cleaned_data['code']

        if 'id' in self.data:
            item_exist = CustomerCategory.objects.filter(
                active=True, code__iexact=data
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = CustomerCategory.objects.filter(
                active=True, code__iexact=data
            ).exists()

        if item_exist:
            raise ValidationError(_('The code entered is contained by at least one other record'), code='danger')

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        if 'id' in self.data:
            item_exist = CustomerCategory.objects.filter(
                active=True, description__iexact=data
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = CustomerCategory.objects.filter(
                active=True, description__iexact=data
            ).exists()

        if item_exist:
            raise ValidationError(_('The description entered is contained by at least one other record'), code='danger')

        return data

    class Meta:
        model = CustomerCategory
        fields = ['code', 'description', 'discount']
        labels = {
            'code': _('Code:'),
            'description': _('Description:'),
            'discount': _('Discount:')
        }
        help_texts = {
            'code': _('Enter a code of maximum length 10 characters'),
            'description': _('Enter a description of maximum length 30 characters'),
            'discount': _('Enter a discount associated with the category')
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
            ),
            'discount': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('discount'),
                    'id': 'discount',
                    'name': 'discount'
                }
            )
        }


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['autofocus'] = True

    def clean_code(self):
        data = self.cleaned_data['code']

        if 'id' in self.data:
            item_exist = Customer.objects.filter(active=True, code__iexact=data).exclude(id=self.data['id']).exists()
        else:
            item_exist = Customer.objects.filter(active=True, code__iexact=data).exists()

        if item_exist:
            raise ValidationError(_('The code entered is contained by at least one other record'), code='danger')

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        if 'id' in self.data:
            item_exist = Customer.objects.filter(
                active=True, description__iexact=data
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = Customer.objects.filter(
                active=True, description__iexact=data
            ).exists()

        if item_exist:
            raise ValidationError(_('The description entered is contained by at least one other record'), code='danger')

        return data

    def clean_category(self):
        data = self.cleaned_data['category']

        if data is None:
            raise ValidationError(_('It is required to select a category'), code='danger')

        return data

    class Meta:
        model = Customer
        fields = ['code', 'description', 'owner', 'landline', 'mobile_phone', 'email', 'address', 'category']
        labels = {
            'code': _('Code:'),
            'description': _('Description:'),
            'owner': _('Owner:'),
            'landline': _('Landline:'),
            'mobile_phone': _('Mobile phone:'),
            'email': _('Email:'),
            'address': _('Address:'),
            'category': _('Category:')
        }
        help_texts = {
            'code': _('Enter a code of maximum length 10 characters'),
            'description': _('Enter a description of maximum length 150 characters'),
            'owner': _('Enter a owner of maximum length 150 characters'),
            'landline': _('Enter a landline of maximum length 50 characters'),
            'mobile_phone': _('Enter a mobile phone of maximum length 50 characters'),
            'email': _('Enter a email of maximum length 150 characters'),
            'address': _('Enter a address of maximum length 150 characters'),
            'category': _('Select an category associated with the customer')
        }
        error_messages = {
            'code': {
                'required': _('It is required to enter a code')
            },
            'description': {
                'required': _('It is required to enter a description')
            },
            'category': {
                'required': _('It is required to select a category')
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
            ),
            'owner': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('owner'),
                    'id': 'owner',
                    'name': 'owner'
                }
            ),
            'landline': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('landline'),
                    'id': 'landline',
                    'name': 'landline'
                }
            ),
            'mobile_phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('mobile phone'),
                    'id': 'mobile_phone',
                    'name': 'mobile_phone'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('email'),
                    'id': 'email',
                    'name': 'email'
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('address'),
                    'id': 'address',
                    'name': 'address'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'category',
                    'name': 'category',
                    'onchange': 'validate("category", "Select")'
                }
            )
        }


class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['autofocus'] = True

    def clean_code(self):
        data = self.cleaned_data['code']

        if 'id' in self.data:
            item_exist = Supplier.objects.filter(active=True, code__iexact=data).exclude(id=self.data['id']).exists()
        else:
            item_exist = Supplier.objects.filter(active=True, code__iexact=data).exists()

        if item_exist:
            raise ValidationError(_('The code entered is contained by at least one other record'), code='danger')

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        if 'id' in self.data:
            item_exist = Supplier.objects.filter(
                active=True, description__iexact=data
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = Supplier.objects.filter(
                active=True, description__iexact=data
            ).exists()

        if item_exist:
            raise ValidationError(_('The description entered is contained by at least one other record'), code='danger')

        return data

    class Meta:
        model = Supplier
        fields = ['code', 'description', 'owner', 'landline', 'mobile_phone', 'email', 'address']
        labels = {
            'code': _('Code:'),
            'description': _('Description:'),
            'owner': _('Owner:'),
            'landline': _('Landline:'),
            'mobile_phone': _('Mobile phone:'),
            'email': _('Email:'),
            'address': _('Address:')
        }
        help_texts = {
            'code': _('Enter a code of maximum length 10 characters'),
            'description': _('Enter a description of maximum length 150 characters'),
            'owner': _('Enter a owner of maximum length 150 characters'),
            'landline': _('Enter a landline of maximum length 50 characters'),
            'mobile_phone': _('Enter a mobile phone of maximum length 50 characters'),
            'email': _('Enter a email of maximum length 150 characters'),
            'address': _('Enter a address of maximum length 150 characters')
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
            ),
            'owner': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('owner'),
                    'id': 'owner',
                    'name': 'owner'
                }
            ),
            'landline': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('landline'),
                    'id': 'landline',
                    'name': 'landline'
                }
            ),
            'mobile_phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('mobile phone'),
                    'id': 'mobile_phone',
                    'name': 'mobile_phone'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('email'),
                    'id': 'email',
                    'name': 'email'
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('address'),
                    'id': 'address',
                    'name': 'address'
                }
            )
        }


class FamilyGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['autofocus'] = True

    def clean_code(self):
        data = self.cleaned_data['code']

        if 'id' in self.data:
            item_exist = FamilyGroup.objects.filter(active=True, code__iexact=data).exclude(id=self.data['id']).exists()
        else:
            item_exist = FamilyGroup.objects.filter(active=True, code__iexact=data).exists()

        if item_exist:
            raise ValidationError(_('The code entered is contained by at least one other record'), code='danger')

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        if 'id' in self.data:
            item_exist = FamilyGroup.objects.filter(
                active=True, description__iexact=data
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = FamilyGroup.objects.filter(
                active=True, description__iexact=data
            ).exists()

        if item_exist:
            raise ValidationError(_('The description entered is contained by at least one other record'), code='danger')

        return data

    class Meta:
        model = FamilyGroup
        fields = ['code', 'description']
        labels = {
            'code': _('Code:'),
            'description': _('Description:')
        }
        help_texts = {
            'code': _('Enter a code of maximum length 10 characters'),
            'description': _('Enter a description of maximum length 100 characters')
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


class FamilyActivityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['autofocus'] = True

    def clean_code(self):
        data = self.cleaned_data['code']

        if 'id' in self.data:
            item_exist = FamilyActivity.objects.filter(
                active=True, code__iexact=data
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = FamilyActivity.objects.filter(
                active=True, code__iexact=data
            ).exists()

        if item_exist:
            raise ValidationError(_('The code entered is contained by at least one other record'), code='danger')

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        if 'id' in self.data:
            item_exist = FamilyActivity.objects.filter(
                active=True, description__iexact=data
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = FamilyActivity.objects.filter(
                active=True, description__iexact=data
            ).exists()

        if item_exist:
            raise ValidationError(_('The description entered is contained by at least one other record'), code='danger')

        return data

    class Meta:
        model = FamilyActivity
        fields = ['code', 'description']
        labels = {
            'code': _('Code:'),
            'description': _('Description:')
        }
        help_texts = {
            'code': _('Enter a code of maximum length 10 characters'),
            'description': _('Enter a description of maximum length 100 characters')
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


class FamilyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['autofocus'] = True

    def clean_code(self):
        data = self.cleaned_data['code']

        if 'id' in self.data:
            item_exist = Family.objects.filter(active=True, code__iexact=data).exclude(id=self.data['id']).exists()
        else:
            item_exist = Family.objects.filter(active=True, code__iexact=data).exists()

        if item_exist:
            raise ValidationError(_('The code entered is contained by at least one other record'), code='danger')

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        if 'id' in self.data:
            item_exist = Family.objects.filter(
                active=True, description__iexact=data
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = Family.objects.filter(
                active=True, description__iexact=data
            ).exists()

        if item_exist:
            raise ValidationError(_('The description entered is contained by at least one other record'), code='danger')

        return data

    def clean_group(self):
        data = self.cleaned_data['group']

        if data is None:
            raise ValidationError(_('It is required to select a group'), code='danger')

        return data

    def clean_activity(self):
        data = self.cleaned_data['activity']

        if data is None:
            raise ValidationError(_('It is required to select an activity'), code='danger')

        return data

    class Meta:
        model = Family
        fields = ['code', 'description', 'increment', 'group', 'activity']
        labels = {
            'code': _('Code:'),
            'description': _('Description:'),
            'increment': _('Increment:'),
            'group': _('Group:'),
            'activity': _('Activity:')
        }
        help_texts = {
            'code': _('Enter a code of maximum length 10 characters'),
            'description': _('Enter a description of maximum length 150 characters'),
            'increment': _('Enter an increment associated with the family'),
            'group': _('Select a group associated with the family'),
            'activity': _('Select an activity associated with the family')
        }
        error_messages = {
            'code': {
                'required': _('It is required to enter a code')
            },
            'description': {
                'required': _('It is required to enter a description')
            },
            'group': {
                'required': _('It is required to select a group')
            },
            'activity': {
                'required': _('It is required to select an activity')
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
            ),
            'increment': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('increment'),
                    'id': 'increment',
                    'name': 'increment'
                }
            ),
            'group': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'group',
                    'name': 'group',
                    'onchange': 'validate("group", "Select")'
                }
            ),
            'activity': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'activity',
                    'name': 'activity',
                    'onchange': 'validate("activity", "Select")'
                }
            )
        }


class MeasurementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['autofocus'] = True

    def clean_code(self):
        data = self.cleaned_data['code']

        if 'id' in self.data:
            item_exist = Measurement.objects.filter(active=True, code__iexact=data).exclude(id=self.data['id']).exists()
        else:
            item_exist = Measurement.objects.filter(active=True, code__iexact=data).exists()

        if item_exist:
            raise ValidationError(_('The code entered is contained by at least one other record'), code='danger')

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        if 'id' in self.data:
            item_exist = Measurement.objects.filter(
                active=True, description__iexact=data
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = Measurement.objects.filter(
                active=True, description__iexact=data
            ).exists()

        if item_exist:
            raise ValidationError(_('The description entered is contained by at least one other record'), code='danger')

        return data

    class Meta:
        model = Measurement
        fields = ['code', 'description']
        labels = {
            'code': _('Code:'),
            'description': _('Description:')
        }
        help_texts = {
            'code': _('Enter a code of maximum length 10 characters'),
            'description': _('Enter a description of maximum length 100 characters')
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


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['autofocus'] = True

    def clean_code(self):
        data = self.cleaned_data['code']

        if 'id' in self.data:
            item_exist = Product.objects.filter(active=True, code__iexact=data).exclude(id=self.data['id']).exists()
        else:
            item_exist = Product.objects.filter(active=True, code__iexact=data).exists()

        if item_exist:
            raise ValidationError(_('The code entered is contained by at least one other record'), code='danger')

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        if 'id' in self.data:
            item_exist = Product.objects.filter(
                active=True, description__iexact=data
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = Product.objects.filter(
                active=True, description__iexact=data
            ).exists()

        if item_exist:
            raise ValidationError(_('The description entered is contained by at least one other record'), code='danger')

        return data

    def clean_family(self):
        data = self.cleaned_data['family']

        if data is None:
            raise ValidationError(_('It is required to select a family'), code='danger')

        return data

    def clean_measurement(self):
        data = self.cleaned_data['measurement']

        if data is None:
            raise ValidationError(_('It is required to select a measurement'), code='danger')

        return data

    class Meta:
        model = Product
        fields = ['code', 'description', 'measurement', 'sale_price', 'family']
        labels = {
            'code': _('Code:'),
            'description': _('Description:'),
            'measurement': _('Measurement:'),
            'sale_price': _('Sale price:'),
            'family': _('Family:')
        }
        help_texts = {
            'code': _('Enter a code of maximum length 10 characters'),
            'description': _('Enter a description of maximum length 150 characters'),
            'measurement': _('Select a measurement associated with the product'),
            'sale_price': _('Enter a sale_price associated with the product'),
            'family': _('Select a family associated with the product')
        }
        error_messages = {
            'code': {
                'required': _('It is required to enter a code')
            },
            'description': {
                'required': _('It is required to enter a description')
            },
            'measurement': {
                'required': _('It is required to select a measurement')
            },
            'family': {
                'required': _('It is required to select a family')
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
            ),
            'measurement': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'measurement',
                    'name': 'measurement',
                    'onchange': 'validate("measurement", "Select")'
                }
            ),
            'sale_price': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('sale_price'),
                    'id': 'sale_price',
                    'name': 'sale_price'
                }
            ),
            'family': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'family',
                    'name': 'family',
                    'onchange': 'validate("family", "Select")'
                }
            )
        }


class ProductConversionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['autofocus'] = True

    def clean_value(self):
        data = self.cleaned_data['value']

        if data == 0.00000:
            raise ValidationError(_('The entered value cannot be zero'), code='danger')

        return data

    def clean_product(self):
        data = self.cleaned_data['product']

        if data is None:
            raise ValidationError(_('It is required to select a product'), code='danger')

        return data

    def clean_measurement(self):
        data = self.cleaned_data['measurement']

        if data is None:
            raise ValidationError(_('It is required to select a measurement'), code='danger')

        data_product = self.data['product']
        if data_product == '':
            data_product = None

        if 'id' in self.data:
            item_exist = ProductConversion.objects.filter(
                active=True, product__id=data_product, measurement__id=data.id
            ).exclude(id=self.data['id']).exists()
        else:
            item_exist = ProductConversion.objects.filter(
                active=True, product__id=data_product, measurement__id=data.id
            ).exists()

        if item_exist:
            raise ValidationError(_('The measurement entered is contained by at least one other record'), code='danger')

        return data

    class Meta:
        model = ProductConversion
        fields = ['product', 'value', 'measurement']
        labels = {
            'product': _('Product:'),
            'value': _('Value:'),
            'measurement': _('Measurement:')
        }
        help_texts = {
            'product': _('Select a product associated with the conversion'),
            'value': _('Enter a value associated with the conversion'),
            'measurement': _('Select a measurement associated with the conversion')
        }
        error_messages = {
            'product': {
                'required': _('It is required to select a product')
            },
            'value': {
                'required': _('It is required to enter a value')
            },
            'measurement': {
                'required': _('It is required to select a measurement')
            }
        }
        widgets = {
            'product': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'product',
                    'name': 'product',
                    'onchange': 'validate("product", "Select")'
                }
            ),
            'value': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('value'),
                    'id': 'value',
                    'name': 'value'
                }
            ),
            'measurement': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'measurement',
                    'name': 'measurement',
                    'onchange': 'validate("measurement", "Select")'
                }
            )
        }
