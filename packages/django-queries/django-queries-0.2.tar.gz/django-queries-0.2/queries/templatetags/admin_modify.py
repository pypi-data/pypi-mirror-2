from django import template

register = template.Library()

def prepopulated_fields_js(context):
    """
    Creates a list of prepopulated_fields that should render Javascript for
    the prepopulated fields for both the query form and inlines.
    """
    prepopulated_fields = []
    if context['add'] and 'queryform' in context:
        prepopulated_fields.extend(context['queryform'].prepopulated_fields)
    if 'inline_query_formsets' in context:
        for inline_query_formset in context['inline_query_formsets']:
            for inline_query_form in inline_query_formset:
                if inline_query_form.original is None:
                    prepopulated_fields.extend(inline_query_form.prepopulated_fields)
    context.update({'prepopulated_fields': prepopulated_fields})
    return context
prepopulated_fields_js = register.inclusion_tag('query/prepopulated_fields_js.html', takes_context=True)(prepopulated_fields_js)

def submit_row(context):
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    return {
        'onclick_attrib': (opts.get_ordered_objects() and change
                            and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': (not is_popup and context['has_delete_permission']
                              and (change or context['show_delete'])),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and 
                            not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True
    }
submit_row = register.inclusion_tag('query/submit_line.html', takes_context=True)(submit_row)
