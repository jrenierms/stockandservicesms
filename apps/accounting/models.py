from apps.base.choices import transaction_type
from apps.base.models import BaseModel
from apps.commercial.models import Product, Supplier, Customer, ProductConversion
from apps.security.models import User
from django.db import models
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _


class Store(BaseModel):
    code = models.CharField(_('Code'), max_length=10, db_index=True)
    description = models.CharField(_('Description'), max_length=100, db_index=True)

    class Meta:
        ordering = ['code']
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')

    def __str__(self):
        return "{0}, {1}".format(self.code, self.description)

    def to_json(self):
        item = model_to_dict(self)
        return item


class Area(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='areas')
    code = models.CharField(_('Code'), max_length=10, db_index=True)
    description = models.CharField(_('Description'), max_length=100, db_index=True)

    class Meta:
        ordering = ['code']
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')

    def __str__(self):
        return "{0}, {1}".format(self.code, self.description)

    def to_json(self):
        item = model_to_dict(self)
        item['store'] = self.store.description
        return item


class Location(BaseModel):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='locations')
    code = models.CharField(_('Code'), max_length=10, db_index=True)
    description = models.CharField(_('Description'), max_length=100, db_index=True)

    class Meta:
        ordering = ['code']
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __str__(self):
        return "{0}, {1}".format(self.code, self.description)

    def to_json(self):
        item = model_to_dict(self)
        item['area'] = self.area.description
        return item


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks_product')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='stocks_area')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='stocks_location')
    cost_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    input_date = models.DateField(null=True, blank=True)
    input_quantity = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    input_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    input_return_date = models.DateField(null=True, blank=True)
    input_return_quantity = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    input_return_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    input_adjustment_date = models.DateField(null=True, blank=True)
    input_adjustment_quantity = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    input_adjustment_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    output_date = models.DateField(null=True, blank=True)
    output_quantity = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    output_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    output_return_date = models.DateField(null=True, blank=True)
    output_return_quantity = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    output_return_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    output_adjustment_date = models.DateField(null=True, blank=True)
    output_adjustment_quantity = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    output_adjustment_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    previous_date = models.DateField(null=True, blank=True)
    previous_quantity = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    previous_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    actual_date = models.DateField(null=True, blank=True)
    actual_quantity = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    actual_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['product']
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

    def __str__(self):
        return "{0}, {1}".format(self.product, self.location)

    def to_json(self):
        item = model_to_dict(self)
        item['product'] = self.product.to_json()
        item['location'] = self.location.description
        return item


class TransactionNumber(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_type = models.PositiveSmallIntegerField(default=1, choices=transaction_type)
    number = models.PositiveIntegerField()

    class Meta:
        ordering = ['transaction_type']
        verbose_name = 'Transaction number'
        verbose_name_plural = 'Transaction numbers'

    def __str__(self):
        return self.get_transaction_type_display()

    def to_json(self):
        item = model_to_dict(self)
        item['transaction_type'] = {'id': self.transaction_type, 'name': self.get_transaction_type_display()}
        return item


class TransactionSummary(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_type = models.PositiveSmallIntegerField(default=1, choices=transaction_type)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='summaries_supplier')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='summaries_customer')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='summaries_area')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summaries_user')
    document = models.CharField(max_length=20)
    source_document = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateField()
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['transaction_type', 'document']
        verbose_name = 'Transaction summary'
        verbose_name_plural = 'Transaction summaries'

    def __str__(self):
        return "{0}, {1}".format(self.document, self.get_transaction_type_display())

    def to_json(self):
        item = model_to_dict(self, exclude=['supplier', 'customer', 'user', 'source_document', 'comment'])
        item['transaction_type'] = {'id': self.transaction_type, 'name': self.get_transaction_type_display()}
        if self.supplier is not None:
            item['supplier'] = self.supplier.to_json()
        if self.customer is not None:
            item['customer'] = self.customer.to_json()
        if self.source_document is not None:
            item['source_document'] = self.source_document
        item['date'] = self.date.strftime('%Y-%m-%d')
        if self.comment is not None:
            item['comment'] = self.comment
        return item


class TransactionDetail(models.Model):
    id = models.AutoField(primary_key=True)
    summary = models.ForeignKey(TransactionSummary, on_delete=models.CASCADE, related_name='details_summary')
    product_conversion = models.ForeignKey(ProductConversion, on_delete=models.CASCADE, related_name='details_product')
    quantity = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    actual_quantity = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    cost_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sale_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    returned_quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0.00000)

    class Meta:
        ordering = ['summary', 'product_conversion']
        verbose_name = 'Transaction detail'
        verbose_name_plural = 'Transaction details'

    def __str__(self):
        return "{0}, {1}, {2}".format(self.summary.document, self.summary.get_transaction_type_display(),
                                      self.product_conversion.product.description)

    def to_json(self):
        item = model_to_dict(self)
        item['summary'] = self.summary.to_json()
        item['product_conversion'] = self.product_conversion.to_json()
        return item
