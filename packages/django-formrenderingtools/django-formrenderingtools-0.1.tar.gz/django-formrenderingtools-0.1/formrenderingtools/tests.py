from django.conf import settings
from django import forms
from django.template import Template, Context
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import strip_spaces_between_tags

from formrenderingtools import default_settings


class ContactForm(forms.Form):
    """
    A sample form, for use in test cases.
    """
    subject = forms.CharField(
        label='Subject',
        max_length=100,
    )
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(
        required=False,
        help_text='Send a copy of the message to the sender.',
    )
    
    def clean(self):
        """This sample form never validates!"""
        raise forms.ValidationError('Sorry, but this sample form never validates!')


class FormLayoutsTestCase(TestCase):
    """
    Tests the "form_layouts" template tag library.
    
    Alters settings.FORMRENDERINGTOOLS_TEMPLATE_DIR so that only the "test"
    templates are available. Otherwise, the project's templates could interfere
    with test results.
    """
    def setUp(self):
        self.template_dir = 'tests/formrenderingtools/form_layouts'
        self._change_settings()
    
    def tearDown(self):
        self._restore_settings()
    
    def _change_settings(self):
        """
        Loads default settings, so that the project configuration does not
        affects the test process.
        """
        self.previous_settings = {}
        for key, value in default_settings.iteritems():
            self.previous_settings[key] = getattr(settings, key) 
            setattr(settings, key, value)
        setattr(settings, 'FORMRENDERINGTOOLS_TEMPLATE_DIR', self.template_dir)
    
    def _restore_settings(self):
        """
        Restores the settings that were in use before running this test suite.
        """
        for key, value in self.previous_settings.iteritems():
            setattr(settings, key, value)
    
    def _render_string_to_string(self, template_code, context):
        """
        Renders template code to a string and removes some whitespaces, so that
        the comparison between theoric output and effective one can be compared
        with more flexibility.
        
        This fits HTML needs. You may not use it for any "whitespace sensitive"
        code.
        """
        t = Template(template_code)
        c = Context(context)
        return strip_spaces_between_tags(t.render(c)).strip()
    
    def _test_template_output(self, code, context):
        """
        Renders a template /form_layouts/<code>_source.html with the given
        context and validates that it matches the content of the
        /form_layouts/<code>_output.html file.
        """
        theory = render_to_string('tests/formrenderingtools/%s_output.html' % code, {})
        theory = strip_spaces_between_tags(theory).strip()
        reality = render_to_string('tests/formrenderingtools/%s_source.html' % code, context)
        reality = strip_spaces_between_tags(reality).strip()
        self.assertEquals(reality, theory)
    
    def test_template_dir_setting(self):
        """
        Tests the FORMRENDERINGTOOLS_TEMPLATE_DIR setting.
        """
        form = ContactForm()
        
        # Setting FORMRENDERINGTOOLS_TEMPLATE_DIR to something which does not
        # exist must raise an exception
        setattr(settings, 'FORMRENDERINGTOOLS_TEMPLATE_DIR', 'tests/formrenderingtools/form_layouts/wrong_directory')
        try:
            self._render_string_to_string(
                '{% load form_layouts %}{% form %}',
                {'form': form},
            )
        except:
            pass
        else:
            self.fail('The FORMRENDERINGTOOLS_TEMPLATE_DIR has no effect')
        
        # Setting FORMRENDERINGTOOLS_TEMPLATE_DIR to something which exists
        # must work.
        # The "default test form layout" begins with a specific text
        # which is not in the "default production form layout". This text
        # is used to make sure that the test templates are used rather than the
        # default ones.
        setattr(settings, 'FORMRENDERINGTOOLS_TEMPLATE_DIR', 'tests/formrenderingtools/form_layouts')
        test_text = u'<p>This is a test template for django-formrenderingtools</p>'
        output = self._render_string_to_string(
            '{% load form_layouts %}{% form %}',
            {'form': form, 'test_text': test_text},
        )
        self.assertTrue(output.startswith(test_text))
    
    def _test_template_tag(self, tag_name):
        """
        Sets up a form, render a template and assert it matches the expected
        output.
        """
        default_form = ContactForm()
        error_form = ContactForm({'subject': u'test'})
        context = {'form': default_form,
                   'error_form': error_form,
                   }
        self._test_template_output(tag_name, context)
    
    def test_form(self):
        """
        Tests the {% form %} template tag.
        """
        self._test_template_tag('form')
    
    def test_field_list(self):
        """
        Tests the {% field_list %} template tag.
        """
        self._test_template_tag('field_list')
    
    def test_field(self):
        """
        Tests the {% field %} template tag.
        """
        self._test_template_tag('field')
    
    def test_label(self):
        """
        Tests the {% label %} template tag.
        """
        self._test_template_tag('label')
