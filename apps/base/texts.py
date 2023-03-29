from django.utils.translation import gettext_lazy as _


table_language = {
    'processing': _('Processing...'),
    'search': _('Search:'),
    'lengthMenu': _('Show _MENU_ entries'),
    'info': _('Showing _START_ to _END_ of _TOTAL_ entries'),
    'infoEmpty': _('Showing 0 to 0 of 0 entries'),
    'infoFiltered': _('(filtered from _MAX_ total entries)'),
    'infoPostFix': '',
    'loadingRecords': _('Loading...'),
    'zeroRecords': _('No matching records found'),
    'emptyTable': _('No data available in table'),
    'paginate': {
        'first': _('First'),
        'previous': _('Previous'),
        'next': _('Next'),
        'last': _('Last')
    },
    'aria': {
        'sortAscending': _(': activate to sort column ascending'),
        'sortDescending': _(': activate to sort column descending')
    }
}


dialogs = {
    'save_modal_question': _('Are you sure you want to save the information?'),
    'undo_modal_warning': _('You will not be able to undo the action after it is done!'),
    'confirm_modal_button': _('Yes, save'),
    'cancel_modal_button': _('No, cancel'),
    'delete_modal_question': _('Are you sure you want to delete the record?'),
    'delete_modal_button': _('Yes, delete'),
    'apply_picker_button': _('Apply'),
    'cancel_picker_button': _('Cancel'),
    'table_language': table_language,
    'edit_link_button': _('Edit'),
    'delete_link_button': _('Delete'),
    'print_link_button': _('Print'),
    'delete_product_question': _('Are you sure you want to delete the product?')
}


message_texts = {
    'success': {
        'record_successfully_saved': _('Record successfully saved'),
        'record_successfully_deleted': _('Record successfully deleted'),
        'transaction_successfully_saved': _('Transaction successfully saved')
    },
    'error': {
        'error_validation_encountered': _('Error encountered during validation'),
        'record_deletion_failed': _('Record deletion failed'),
        'record_edition_failed': _('Record edition failed'),
        'transaction_save_failed': _('Transaction save failed'),
        'information_load_failed': _('Information load failed')
    },
    'info': {
        'check_data_entered': _('Please check the data entered'),
        'record_not_found': _('Record not found'),
        'record_deletion_related': _('Record related to other data'),
        'product_measurement_related': _('Product measurement related to other data'),
        'product_already_added': _('Product is already added'),
        'product_no_added': _('No product has been added'),
        'wrong_quantities_entered': _('Wrong quantities and/or prices entered'),
        'wrong_prices_entered': _('Wrong prices entered'),
        'product_without_location': _('There is one or more products without a location'),
        'quantities_greater_available': _('There are quantities greater than available')
    }
}


months = [
    _('January'),
    _('February'),
    _('March'),
    _('April'),
    _('May'),
    _('June'),
    _('July'),
    _('August'),
    _('September'),
    _('October'),
    _('November'),
    _('December')
]
