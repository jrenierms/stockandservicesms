from django.db import models
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _
from stockandservicesms.settings import MEDIA_URL, STATIC_URL


class BaseModel(models.Model):
    id = models.AutoField(_('Id'), primary_key=True)
    active = models.BooleanField(_('Active'), default=True)
    created_date = models.DateField(_('Created date'), auto_now=False, auto_now_add=True)
    edited_date = models.DateField(_('Edited date'), auto_now=True, auto_now_add=False)
    deleted_date = models.DateField(_('Edited date'), auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True


class Setting(models.Model):
    id = models.AutoField(primary_key=True)
    company_code = models.CharField(max_length=10)
    company_description = models.CharField(max_length=150)
    company_address = models.CharField(max_length=150, null=True, blank=True)
    company_email = models.EmailField(max_length=150, null=True, blank=True)
    logo = models.ImageField(upload_to='logos', default='logo.jpg', null=True, blank=True)

    def get_image(self):
        if self.logo:
            return '{}{}'.format(MEDIA_URL, self.logo)
        return '{}{}'.format(STATIC_URL, 'media/logo.jpg')

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return "{0}, {1}".format(self.company_code, self.company_description)

    def to_json(self):
        item = model_to_dict(self)
        return item
