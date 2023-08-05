from django.conf import settings


# Default settings
default_settings = {
    'FORMRENDERINGTOOLS_TEMPLATE_DIR': 'form_layouts',
    'FORMRENDERINGTOOLS_DEFAULT_LAYOUT': 'default',
    'FORMRENDERINGTOOLS_FORM_TEMPLATE_DIR': 'form',
    'FORMRENDERINGTOOLS_FORM_ERRORS_TEMPLATE_DIR': 'form_errors',
    'FORMRENDERINGTOOLS_FIELD_LIST_TEMPLATE_DIR': 'field_list',
    'FORMRENDERINGTOOLS_FIELD_TEMPLATE_DIR': 'field',
    'FORMRENDERINGTOOLS_FIELD_ERRORS_TEMPLATE_DIR': 'field_errors',
    'FORMRENDERINGTOOLS_LABEL_TEMPLATE_DIR': 'label',
    'FORMRENDERINGTOOLS_HELP_TEXT_TEMPLATE_DIR': 'help_text',
    'FORMRENDERINGTOOLS_DEFAULT_FORM_TEMPLATE': 'default.html',
    'FORMRENDERINGTOOLS_DEFAULT_FORM_ERRORS_TEMPLATE': 'default.html',
    'FORMRENDERINGTOOLS_DEFAULT_FIELD_LIST_TEMPLATE': 'default.html',
    'FORMRENDERINGTOOLS_DEFAULT_FIELD_TEMPLATE': 'default.html',
    'FORMRENDERINGTOOLS_DEFAULT_FIELD_ERRORS_TEMPLATE': 'default.html',
    'FORMRENDERINGTOOLS_DEFAULT_LABEL_TEMPLATE': 'default.html',
    'FORMRENDERINGTOOLS_DEFAULT_HELP_TEXT_TEMPLATE': 'default.html',
}

# Apply default settings if necessary
for key, value in default_settings.iteritems():
    if not hasattr(settings, key):
        setattr(settings, key, value)
