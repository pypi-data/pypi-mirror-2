from django.test import TestCase
from django import forms as django_forms
import forms


class FieldsetValidationTestCase(TestCase):
    def setUp(self):
        class BaseForm(django_forms.Form, forms.FieldsetMixin):
            test_field1 = django_forms.CharField()
            test_field2 = django_forms.CharField()
            test_field3 = django_forms.CharField()

        self.base_form = BaseForm

    def test_missing_fields(self):
        class TestForm(self.base_form):
            fieldsets = (
                (u'Fieldset1', {'fields': ('test_field1',)}),
                (u'Fieldset2', {'fields': ('test_field2',)}),
            )

        self.assertRaises(forms.FieldsetError, TestForm().validate_fieldsets)

    def test_duplicate_fields(self):
        class TestForm(self.base_form):
            fieldsets = (
                (u'Fieldset1', {'fields': ('test_field1', 'test_field3')}),
                (u'Fieldset2', {'fields': ('test_field2', 'test_field3')}),
            )

        self.assertRaises(forms.FieldsetError, TestForm().validate_fieldsets)

    def test_valid_fieldset(self):
        class TestForm(self.base_form):
            fieldsets = (
                (u'Fieldset1', {'fields': ('test_field1',)}),
                (u'Fieldset2', {'fields': ('test_field2', 'test_field3')}),
            )

        self.assertEqual(TestForm().validate_fieldsets(), True)


class FieldsetAccessTestCase(TestCase):
    def setUp(self):
        class BaseForm(django_forms.Form, forms.FieldsetMixin):
            test_field1 = django_forms.CharField()
            test_field2 = django_forms.CharField()
            test_field3 = django_forms.CharField()

            fieldsets = (
                (u'Fieldset1', {'fields': ('test_field1',)}),
                (u'Fieldset2', {'fields': ('test_field2', 'test_field3')}),
            )

        self.base_form = BaseForm

    def test_iter_fieldsets(self):
        fieldsets = [fset.title for fset in self.base_form().iter_fieldsets()]
        self.assertEqual(len(fieldsets), 2)
        self.assertEqual('Fieldset1' in fieldsets, True)
        self.assertEqual('Fieldset2' in fieldsets, True)

    def test_fieldset_dict(self):
        fset_dict = self.base_form().fieldset_dict
        self.assertEqual(len(fset_dict), 2)
        self.assertEqual('fieldset1' in fset_dict.keys(), True)
        self.assertEqual('fieldset2' in fset_dict.keys(), True)
        self.assertRaises(AttributeError,
                          self.base_form().__setattr__, 'fieldset_dict', {})


class FieldsetRenderTestCase(TestCase):
    def setUp(self):
        class TestForm(django_forms.Form, forms.FieldsetMixin):
            test_field1 = django_forms.CharField()
            test_field2 = django_forms.CharField()
            test_field3 = django_forms.CharField()
            test_field4 = django_forms.CharField(
                                      widget=django_forms.widgets.HiddenInput)

            fieldsets = (
                (u'Fieldset1', {
                    'description': u'Test Description<sup>1</sup>',
                    'fields': ('test_field1',),
                }),
                (u'Fieldset2', {
                    'fields': ('test_field2', 'test_field3', 'test_field4'),
                }),
            )

            def clean_test_field2(self):
                if self.cleaned_data['test_field2'] != u'':
                    raise django_forms.ValidationError(
                                    [u'Test Error - Field Level - 1',
                                     u'Test Error - Field Level - 2'])

            def clean_test_field4(self):
                raise django_forms.ValidationError(
                                                 u'Test Error - Hidden Field')

            def clean(self):
                raise django_forms.ValidationError(u'Test Error - Top Level')
        self.test_form = TestForm

    def test_fieldset_render(self):
        """Test if the form is being rendered at all and all the elements are
           in the result.
        """
        form = self.test_form(data={'test_field2': u'Test Value',
                                    'test_field4': u'Test Value'})
        self.assertEqual(form.is_valid(), False)
        for method in ('as_fieldset_table', 'as_fieldset_ul', 'as_fieldset_p'):
            rendered = getattr(form, method)()
            # Are all errors rendered somehow?
            self.assertTrue(u'Test Error - Top Level' in rendered)
            self.assertTrue(u'Test Error - Hidden Field' in rendered)
            self.assertTrue(u'Test Error - Field Level - 1' in rendered)
            self.assertTrue(u'Test Error - Field Level - 2' in rendered)
            # Are all fields present?
            for field in form.fields.keys():
                bf= django_forms.forms.BoundField(form,
                                                  form.fields[field],
                                                  field)
                self.assertTrue(unicode(bf) in rendered)
            # Check for fieldset titles & decriptions
            self.assertTrue(u'Fieldset1' in rendered)
            self.assertTrue(u'Fieldset2' in rendered)
            self.assertTrue(u'Test Description<sup>1</sup>' in rendered)

    def test_individual_fieldset_render(self):
        form = self.test_form(data={'test_field2': u'Test Value',
                                    'test_field4': u'Test Value'})
        fieldset1 = form.fieldset_dict['fieldset1']
        fieldset2 = form.fieldset_dict['fieldset2']
        self.assertEqual(form.is_valid(), False)
        for method in ('as_table', 'as_ul', 'as_p'):
            rendered1 = getattr(fieldset1, method)()
            rendered2 = getattr(fieldset2, method)()
            # Are all errors rendered somehow?
            self.assertTrue(u'Test Error - Field Level - 1' in rendered2)
            self.assertTrue(u'Test Error - Field Level - 2' in rendered2)
            self.assertTrue(u'Test Error - Hidden Field' in rendered2)
            # Are all fields present?
            for fieldset, rendered in ((fieldset1, rendered1),
                                       (fieldset2, rendered2)):
                for field in fieldset.fields:
                    bf= django_forms.forms.BoundField(form,
                                                      form.fields[field],
                                                      field)
                    self.assertTrue(unicode(bf) in rendered)
            # Check for fieldset titles & decriptions
            self.assertTrue(u'Fieldset1' in rendered1)
            self.assertTrue(u'Fieldset2' in rendered2)
            self.assertTrue(u'Test Description' in rendered1)
