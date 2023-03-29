from PIL import Image
from apps.base.choices import sexual_gender, action_type
from apps.base.models import BaseModel
from django.contrib.auth.models import Group, AbstractUser
from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from stockandservicesms.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):

    id_card = models.CharField(_('ID card'), max_length=11, db_index=True)
    image = models.ImageField(_('Image'), upload_to='users', default='AvatarImage0.jpg', null=True, blank=True)
    gender = models.PositiveSmallIntegerField(_('Gender'), default=1, choices=sexual_gender)
    address = models.CharField(_('Address'), max_length=150, null=True, blank=True)
    landline = models.CharField(_('Landline'), max_length=50, null=True, blank=True)
    mobile_phone = models.CharField(_('Mobile phone'), max_length=50, null=True, blank=True)

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'media/users/AvatarImage0.jpg')

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-id']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def to_json(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        return item


class Audit(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit')
    action = models.PositiveSmallIntegerField(_('Action'), default=1, choices=action_type)
    access = models.CharField(_('Access'), max_length=150, db_index=True)
    date_time = models.DateTimeField(_('Date-Time'), auto_now=False, auto_now_add=True)
    comment = models.TextField(_('Comment'), null=True, blank=True)

    class Meta:
        ordering = ['date_time']
        verbose_name = _('Audit')
        verbose_name_plural = _('Audits')

    def __str__(self):
        return "{0}, {1}, {2}, {3}, {4}".format(self.user, self.action, self.access,
                                                self.date_time.strftime('%Y-%m-%d %I:%M:%S %p'), self.comment)

    def to_json(self):
        item = model_to_dict(self)
        item['user'] = self.user.username
        item['action'] = {'id': self.action, 'name': self.get_action_display()}
        item['date_time'] = self.date_time.strftime('%Y-%m-%d %I:%M:%S %p')
        return item
