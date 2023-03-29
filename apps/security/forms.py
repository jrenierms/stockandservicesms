from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import *


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(label=_('Password:'),
                                help_text=_('Enter a password of at least 8 characters'),
                                error_messages={
                                    'required': _('It is required enter a password')
                                },
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': _('password'),
                                        'id': 'password1',
                                        'name': 'password1',
                                        'oninvalid': 'validate("password1", "TextInput")',
                                        'onkeyup': 'validate("password1", "TextInput")'
                                    }
                                ))
    password2 = forms.CharField(label=_('Confirm password:'),
                                help_text=_('Confirm the password previously entered'),
                                error_messages={
                                    'required': _('It is required to confirm the password')
                                },
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': _('confirm password'),
                                        'id': 'password2',
                                        'name': 'password2',
                                        'oninvalid': 'validate("password2", "TextInput")',
                                        'onkeyup': 'validate("password2", "TextInput")'
                                    }
                                ))

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError(_('The password entered does not match the previous one'), code='danger')

        return self.cleaned_data['password2']

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': _('User:'),
            'first_name': _('Name:'),
            'last_name': _('Last name:'),
            'email': _('Email:')
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('user'),
                    'id': 'username',
                    'name': 'username',
                    'oninvalid': 'validate("username", "TextInput")',
                    'onkeyup': 'validate("username", "TextInput")'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('name'),
                    'id': 'first_name',
                    'name': 'first_name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('last name'),
                    'id': 'last_name',
                    'name': 'last_name'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('email'),
                    'id': 'email',
                    'name': 'email'
                }
            )
        }


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password:'),
                                help_text=_('Enter a password of at least 8 characters'),
                                error_messages={
                                    'required': _('It is required enter a password')
                                },
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': _('password'),
                                        'id': 'password1',
                                        'name': 'password1',
                                        'oninvalid': 'validate("password1", "TextInput")',
                                        'onkeyup': 'validate("password1", "TextInput")'
                                    }
                                ))
    password2 = forms.CharField(label=_('Confirm password:'),
                                help_text=_('Confirm the password previously entered'),
                                error_messages={
                                    'required': _('It is required to confirm the password')
                                },
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': _('confirm password'),
                                        'id': 'password2',
                                        'name': 'password2',
                                        'oninvalid': 'validate("password2", "TextInput")',
                                        'onkeyup': 'validate("password2", "TextInput")'
                                    }
                                ))

    def clean_password2(self):

        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError(_('The password entered does not match the previous one'), code='danger')

        return self.cleaned_data['password2']

    def clean_id_card(self):
        data = self.cleaned_data['id_card']

        if self.instance.id:
            list_items = list(User.objects.filter(is_active=True).exclude(id=self.instance.id).
                              filter(id_card__iexact=data)).__len__()
        else:
            list_items = list(User.objects.filter(is_active=True).
                              filter(id_card__iexact=data)).__len__()

        if list_items > 0:
            raise ValidationError(_('The ID card entered is contained by at least one other record'), code='danger')

        return data

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'id_card', 'gender', 'image', 'address', 'landline',
                  'mobile_phone']
        labels = {
            'username': _('User:'),
            'first_name': _('Name:'),
            'last_name': _('Last name:'),
            'email': _('Email:'),
            'id_card': _('ID card:'),
            'gender': _('Sexual gender:'),
            'image': _('Image:'),
            'address': _('Address:'),
            'landline': _('Landline:'),
            'mobile_phone': _('Mobile phone:')
        }
        help_texts = {
            'username': _('Enter a user using letters, digits and @/./+/-/_'),
            'first_name': _('Enter a name of maximum length 30 characters'),
            'last_name': _('Enter a surname of maximum length 150 characters'),
            'email': _('Enter a email of maximum length 254 characters'),
            'id_card': _('Enter a ID card of maximum length 11 characters'),
            'gender': _('Select the gender associated with the user'),
            'image': _('Select an image associated with the user'),
            'address': _('Enter an address of maximum length 150 characters'),
            'landline': _('Enter a landline of maximum length 50 characters'),
            'mobile_phone': _('Enter a mobile phone of maximum length 50 characters')
        }
        error_messages = {
            'username': {
                'required': _('It is required to enter a user')
            },
            'id_card': {
                'required': _('It is required to enter an ID card')
            }
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('user'),
                    'id': 'username',
                    'name': 'username',
                    'oninvalid': 'validate("username", "TextInput")',
                    'onkeyup': 'validate("username", "TextInput")'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('name'),
                    'id': 'first_name',
                    'name': 'first_name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('last name'),
                    'id': 'last_name',
                    'name': 'last_name'
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
            'id_card': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('ID card'),
                    'id': 'id_card',
                    'name': 'id_card',
                    'oninvalid': 'validate("id_card", "TextInput")',
                    'onkeyup': 'validate("id_card", "TextInput")'
                }
            ),
            'gender': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'gender',
                    'name': 'gender'
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={
                    'id': 'image',
                    'name': 'image'
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
            )
        }


class ProfileForm(forms.ModelForm):
    def clean_id_card(self):
        data = self.cleaned_data['id_card']

        if self.instance.id:
            list_items = list(User.objects.filter(is_active=True).exclude(id=self.instance.id).
                              filter(id_card__iexact=data)).__len__()
        else:
            list_items = list(User.objects.filter(is_active=True).
                              filter(id_card__iexact=data)).__len__()

        if list_items > 0:
            raise ValidationError(_('The ID card entered is contained by at least one other record'), code='danger')

        return data

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'id_card', 'gender', 'image', 'address', 'landline',
                  'mobile_phone']
        labels = {
            'username': _('User:'),
            'first_name': _('Name:'),
            'last_name': _('Last name:'),
            'email': _('Email:'),
            'id_card': _('ID card:'),
            'gender': _('Sexual gender:'),
            'image': _('Image:'),
            'address': _('Address:'),
            'landline': _('Landline:'),
            'mobile_phone': _('Mobile phone:')
        }
        help_texts = {
            'username': _('Enter a user using letters, digits and @/./+/-/_'),
            'first_name': _('Enter a name of maximum length 30 characters'),
            'last_name': _('Enter a surname of maximum length 150 characters'),
            'email': _('Enter a email of maximum length 254 characters'),
            'id_card': _('Enter a ID card of maximum length 11 characters'),
            'gender': _('Select the gender associated with the user'),
            'image': _('Select an image associated with the user'),
            'address': _('Enter an address of maximum length 150 characters'),
            'landline': _('Enter a landline of maximum length 50 characters'),
            'mobile_phone': _('Enter a mobile phone of maximum length 50 characters')
        }
        error_messages = {
            'username': {
                'required': _('It is required to enter a user'),
            },
            'id_card': {
                'required': _('It is required to enter an ID card'),
            }
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('user'),
                    'id': 'username',
                    'name': 'username',
                    'oninvalid': 'validate("username", "TextInput")',
                    'onkeyup': 'validate("username", "TextInput")'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('name'),
                    'id': 'first_name',
                    'name': 'first_name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('last name'),
                    'id': 'last_name',
                    'name': 'last_name'
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
            'id_card': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('ID card'),
                    'id': 'id_card',
                    'name': 'id_card',
                    'oninvalid': 'validate("id_card", "TextInput")',
                    'onkeyup': 'validate("id_card", "TextInput")'
                }
            ),
            'gender': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'gender',
                    'name': 'gender'
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={
                    'id': 'image',
                    'name': 'image'
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
            )
        }


class ResetearClaveForm(forms.ModelForm):
    password0 = forms.CharField(label='Current password:',
                                help_text=_('Enter a password of at least 8 characters'),
                                error_messages={
                                    'required': _('It is required to enter the current password')
                                },
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': _('current password'),
                                        'id': 'password0',
                                        'name': 'password0',
                                        'oninvalid': 'validate("password0", "TextInput")',
                                        'onkeyup': 'validate("password0", "TextInput")'
                                    }
                                ))
    password1 = forms.CharField(label='New password:',
                                help_text=_('Enter a password of at least 8 characters'),
                                error_messages={
                                    'required': _('It is required enter the new password')
                                },
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': _('new password'),
                                        'id': 'password1',
                                        'name': 'password1',
                                        'oninvalid': 'validate("password1", "TextInput")',
                                        'onkeyup': 'validate("password1", "TextInput")'
                                    }
                                ))
    password2 = forms.CharField(label=_('Confirm password:'),
                                help_text=_('Confirm the password previously entered'),
                                error_messages={
                                    'required': _('It is required to confirm the password')
                                },
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': _('confirm password'),
                                        'id': 'password2',
                                        'name': 'password2',
                                        'oninvalid': 'validate("password2", "TextInput")',
                                        'onkeyup': 'validate("password2", "TextInput")'
                                    }
                                ))

    def clean_password0(self):

        if not check_password(self.cleaned_data['password0'], self.instance.password):
            raise ValidationError(_('The password entered does not match the current one'), code='danger')

        return self.cleaned_data['password0']

    def clean_password2(self):

        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError(_('The password entered does not match the previous one'), code='danger')

        return self.cleaned_data['password2']

    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': _('User:')
        }
        help_texts = {
            'username': _('Enter a user using letters, digits and @/./+/-/_')
        }
        error_messages = {
            'username': {
                'required': _('It is required to enter a user')
            },
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('user'),
                    'id': 'username',
                    'name': 'username',
                    'oninvalid': 'validate("username", "TextInput")',
                    'onkeyup': 'validate("username", "TextInput")'
                }
            )
        }
