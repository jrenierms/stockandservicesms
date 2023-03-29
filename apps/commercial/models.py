from apps.base.models import BaseModel
from django.db import models
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _


class CustomerCategory(BaseModel):
    code = models.CharField(_('Code'), max_length=10, db_index=True)
    description = models.CharField(_('Description'), max_length=30, db_index=True)
    discount = models.DecimalField(_('Discount'), max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['code']
        verbose_name = _('Customer category')
        verbose_name_plural = _('Customer categories')

    def __str__(self):
        return "{0}, {1}".format(self.code, self.description)

    def to_json(self):
        item = model_to_dict(self)
        return item


class Customer(BaseModel):
    category = models.ForeignKey(CustomerCategory, on_delete=models.CASCADE, related_name='customers')
    code = models.CharField(_('Code'), max_length=10, db_index=True)
    description = models.CharField(_('Description'), max_length=150, db_index=True)
    owner = models.CharField(_('Owner'), max_length=150, db_index=True, null=True, blank=True)
    landline = models.CharField(_('Landline'), max_length=50, null=True, blank=True)
    mobile_phone = models.CharField(_('Mobile phone'), max_length=50, null=True, blank=True)
    email = models.EmailField(_('Email'), max_length=150, null=True, blank=True)
    address = models.CharField(_('Address'), max_length=150, null=True, blank=True)

    class Meta:
        ordering = ['code']
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return "{0}, {1}".format(self.code, self.description)

    def to_json(self):
        item = model_to_dict(self)
        item['category'] = self.category.description
        return item


class Supplier(BaseModel):
    code = models.CharField(_('Code'), max_length=10, db_index=True)
    description = models.CharField(_('Description'), max_length=150, db_index=True)
    owner = models.CharField(_('Owner'), max_length=150, db_index=True, null=True, blank=True)
    landline = models.CharField(_('Landline'), max_length=50, null=True, blank=True)
    mobile_phone = models.CharField(_('Mobile phone'), max_length=50, null=True, blank=True)
    email = models.EmailField(_('Email'), max_length=150, null=True, blank=True)
    address = models.CharField(_('Address'), max_length=150, null=True, blank=True)

    class Meta:
        ordering = ['code']
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')

    def __str__(self):
        return "{0}, {1}".format(self.code, self.description)

    def to_json(self):
        item = model_to_dict(self)
        return item


class FamilyGroup(BaseModel):
    code = models.CharField(_('Code'), max_length=10, db_index=True)
    description = models.CharField(_('Description'), max_length=100, db_index=True)

    class Meta:
        ordering = ['description']
        verbose_name = _('Family group')
        verbose_name_plural = _('Family groups')

    def __str__(self):
        return "{0}, {1}".format(self.code, self.description)

    def to_json(self):
        item = model_to_dict(self)
        return item


class FamilyActivity(BaseModel):
    code = models.CharField(_('Code'), max_length=10, db_index=True)
    description = models.CharField(_('Description'), max_length=100, db_index=True)

    class Meta:
        ordering = ['description']
        verbose_name = _('Family activity')
        verbose_name_plural = _('Family activities')

    def __str__(self):
        return "{0}, {1}".format(self.code, self.description)

    def to_json(self):
        item = model_to_dict(self)
        return item


class Family(BaseModel):
    group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='families_group')
    activity = models.ForeignKey(FamilyActivity, on_delete=models.CASCADE, related_name='families_activity')
    code = models.CharField(_('Code'), max_length=10, db_index=True)
    description = models.CharField(_('Description'), max_length=150, db_index=True)
    increment = models.DecimalField(_('Increment'), max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['code']
        verbose_name = _('Family')
        verbose_name_plural = _('Families')

    def __str__(self):
        return "{0}, {1}".format(self.code, self.description)

    def to_json(self):
        item = model_to_dict(self)
        item['group'] = self.group.description
        item['activity'] = self.activity.description
        return item


class Measurement(BaseModel):
    code = models.CharField(_('Code'), max_length=10, db_index=True)
    description = models.CharField(_('Description'), max_length=100, db_index=True)

    class Meta:
        ordering = ['description']
        verbose_name = _('Measurement')
        verbose_name_plural = _('Measurements')

    def __str__(self):
        return "{0}, {1}".format(self.code, self.description)

    def to_json(self):
        item = model_to_dict(self)
        return item


class Product(BaseModel):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='products_family')
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name='products_measurement')
    code = models.CharField(_('Code'), max_length=20, db_index=True)
    description = models.CharField(_('Description'), max_length=150, db_index=True)
    sale_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['description']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return "{0}, {1}".format(self.code, self.description)

    def to_json(self):
        item = model_to_dict(self)
        item['family'] = self.family.description
        item['measurement'] = self.measurement.description
        return item


class ProductConversion(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='conversions_product')
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name='conversions_measurement')
    value = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)

    class Meta:
        ordering = ['product']
        verbose_name = _('Product conversion')
        verbose_name_plural = _('Product conversions')

    def __str__(self):
        return "{0}, {1}".format(self.product.description, self.measurement.description)

    def to_json(self):
        item = model_to_dict(self)
        item['product'] = self.product.to_json()
        item['measurement'] = self.measurement.to_json()
        return item
