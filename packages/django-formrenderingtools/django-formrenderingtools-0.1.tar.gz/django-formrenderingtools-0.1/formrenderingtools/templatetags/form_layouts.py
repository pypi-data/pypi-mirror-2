import os.path

from django import template
from django.template import loader

from templateaddons.utils import decode_tag_arguments, parse_tag_argument

from django.conf import settings


register = template.Library()


class ElementNode(template.Node):
    """
    Base class for template tags of the "form_layouts" library.
    
    Subclasses must have an "element" property.
    """
    def _template_names(self, layout_names, template_names):
        """
        Return a generator over template names. Used by render() to select the
        most accurate template.
        
        The returned generator contains values which look like the following: 
        '<settings.FORMRENDERINGTOOLS_TEMPLATE_DIR>/<layout>/<element>/<template>'
        
        element is the form element name, i.e. one in:
        
        * 'form'
        * 'form_errors'
        * 'field_list'
        * 'field'
        * 'field_errors'
        * 'label'
        * 'help_text'
        
        layout_names is a string or a list of strings.
        
        template_names is a string or a list of strings.
        """
        if not layout_names:
            layout_names = []
        elif isinstance(layout_names, basestring):
            layout_names = [layout_names]
        if not template_names:
            template_names = []
        elif isinstance(template_names, basestring):
            template_names = [template_names]
        if not settings.FORMRENDERINGTOOLS_DEFAULT_LAYOUT in layout_names:
            layout_names.append(settings.FORMRENDERINGTOOLS_DEFAULT_LAYOUT)
        default_template_name = getattr(settings, 'FORMRENDERINGTOOLS_DEFAULT_%s_TEMPLATE' % self.element.upper())
        if not default_template_name in template_names:
            template_names.append(default_template_name)
        for template_name in template_names:
            for layout_name in layout_names:
                yield os.path.join(settings.FORMRENDERINGTOOLS_TEMPLATE_DIR,
                                   layout_name,
                                   self.element,
                                   template_name)


class FormElementNode(ElementNode):
    def __init__(self, element, form=None, layout=None, fields=None, exclude_fields=None, template=None):
        self.element = element
        self.form = form or 'form'
        self.layout = layout
        self.fields = fields
        self.exclude_fields = exclude_fields
        self.template_name = template
    
    def render(self, context):
        form = parse_tag_argument(self.form, context)
        layout = parse_tag_argument(self.layout, context)
        fields = parse_tag_argument(self.fields, context)
        exclude_fields = parse_tag_argument(self.exclude_fields, context)
        template_name = parse_tag_argument(self.template_name, context)
        
        if self.element == 'field_list':
            if fields:
                if isinstance(fields, basestring):
                    fields = fields.split(',')
            else:
                fields = [field.name for field in form] # default field list
            if exclude_fields:
                if isinstance(exclude_fields, basestring):
                    exclude_fields = exclude_fields.split(',')
            else:
                exclude_fields = []
            fields = [field for field in fields if field not in exclude_fields]
            tmp = []
            for field_name in fields:
                for field in form:
                    if field.name == field_name:
                        tmp.append(field)
                        break
            fields = tmp
        
        template_names = self._template_names(layout, template_name)
        template_object = loader.select_template(template_names)
        
        context.push()
        context['form'] = form
        context['layout'] = layout
        context['fields'] = fields
        context['exclude_fields'] = exclude_fields
        output = template_object.render(context)
        context.pop()
        
        return output


def render_form_element(element, parser, token):
    default_arguments = {}
    default_arguments['form'] = None
    default_arguments['layout'] = None
    default_arguments['fields'] = None
    default_arguments['exclude_fields'] = None
    default_arguments['template'] = None
    arguments = decode_tag_arguments(token, default_arguments)
    
    return FormElementNode(element, **arguments)


@register.tag
def form(parser, token):
    return render_form_element('form', parser, token)


@register.tag
def form_errors(parser, token):
    return render_form_element('form_errors', parser, token)


@register.tag
def field_list(parser, token):
    return render_form_element('field_list', parser, token)


class FieldElementNode(ElementNode):
    def __init__(self, element, field=None, layout=None, template=None):
        self.element = element
        self.field = field or 'field'
        self.layout = layout
        self.template_name = template
    
    def render(self, context):
        field = parse_tag_argument(self.field, context)
        layout = parse_tag_argument(self.layout, context)
        template_name = parse_tag_argument(self.template_name, context)
        
        template_names = []
        if template_name:
            template_names.append(template_name)
        template_names.append('%s.html' % field.html_name)
        
        template_names = self._template_names(layout, template_names)
        template_object = loader.select_template(template_names)
        
        context.push()
        context['field'] = field
        context['field_id'] = field.field.widget.id_for_label(field.field.widget.attrs.get('id') or field.auto_id) # code from django/forms/forms.py, BoundField.label_tag()
        context['layout'] = layout
        context['template'] = template_name
        output = template_object.render(context)
        context.pop()
        
        return output


def render_field_element(element, parser, token):
    default_arguments = {}
    default_arguments['field'] = None
    default_arguments['layout'] = None
    default_arguments['template'] = None
    arguments = decode_tag_arguments(token, default_arguments)
    
    return FieldElementNode(element, **arguments)


@register.tag
def field(parser, token):
    return render_field_element('field', parser, token)


@register.tag
def field_errors(parser, token):
    return render_field_element('field_errors', parser, token)


@register.tag
def label(parser, token):
    return render_field_element('label', parser, token)


@register.tag
def help_text(parser, token):
    return render_field_element('help_text', parser, token)


# Deprecated template tags. They still exist for backward compatibility.
@register.tag
def render_form(*args, **kwargs):
    """
    Deprecated. See form().
    
    Exists for backward compatibility.
    """
    return form(*args, **kwargs)


@register.tag
def render_form_errors(*args, **kwargs):
    """
    Deprecated. See form_errors().
    
    Exists for backward compatibility.
    """
    return form_errors(*args, **kwargs)


@register.tag
def render_field_list(*args, **kwargs):
    """
    Deprecated. See field_list().
    
    Exists for backward compatibility.
    """
    return field_list(*args, **kwargs)


@register.tag
def render_field(*args, **kwargs):
    """
    Deprecated. See field().
    
    Exists for backward compatibility.
    """
    return field(*args, **kwargs)


@register.tag
def render_field_errors(*args, **kwargs):
    """
    Deprecated. See field_errors().
    
    Exists for backward compatibility.
    """
    return field_errors(*args, **kwargs)


@register.tag
def render_label(*args, **kwargs):
    """
    Deprecated. See label().
    
    Exists for backward compatibility.
    """
    return label(*args, **kwargs)


@register.tag
def render_help_text(*args, **kwargs):
    """
    Deprecated. See help_text().
    
    Exists for backward compatibility.
    """
    return help_text(*args, **kwargs)
