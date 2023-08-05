import re
import unicodedata
from django import forms as django_forms
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


class FieldsetError(ValueError):
    pass


def slugify(value):
    # stolen from django.template.defaultfilters.slugify
    # only difference is this functions is substituting
    # spaces with underscores instead of hyphens
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '_', value)


class Fieldset(object):
    "Simple iterable for holding fieldset information."

    def __init__(self, form, title=None, fields=(),
                 description=None, extra_content=None):
        self.form = form
        self.title = title
        self.fields = fields
        self.description = description
        self.extra_content = extra_content or {}

    def __iter__(self):
        "Iterates through fields in the fieldset."
        for field in self.fields:
            yield django_forms.forms.BoundField(self.form,
                                                self.form.fields[field],
                                                field)

    def _html_output(self,
                     fieldset_html,
                     title_html,
                     description_html,
                     normal_row,
                     error_row,
                     row_ender,
                     help_text_html,
                     errors_on_separate_row,
                     top_errors=None,
                     error_class=django_forms.util.ErrorList,
                     label_suffix=u':'):
        output, hidden_fields = [], []
        # top_errors is not supplied when the
        # fieldset is rendered individually
        if top_errors is None:
            top_errors = []
            top_errors_on_fieldset = True
        else:
            top_errors_on_fieldset = False
        for bf in self:
            # Escape and cache in local variable.
            bf_errors = error_class([escape(error) for error in bf.errors])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' %
                                       (bf.name, force_unicode(e))
                                       for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_unicode(bf_errors))
                if bf.label:
                    label = escape(force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if label_suffix:
                        if label[-1] not in u':?.!':
                            label += label_suffix
                    label = bf.label_tag(label) or u''
                else:
                    label = u''
                if bf.field.help_text:
                    help_text = help_text_html % force_unicode(
                                                           bf.field.help_text)
                else:
                    help_text = u''
                output.append(normal_row % {'errors': force_unicode(bf_errors),
                                            'label': force_unicode(label),
                                            'field': unicode(bf),
                                            'help_text': help_text})
        if hidden_fields:
            # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>')
                # and insert the hidden fields.
                output[-1] = last_row[:-len(row_ender)] + \
                                str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append
                # the hidden fields.
                output.append(str_hidden)
        # Render fieldset
        if self.title:
            title = title_html % escape(force_unicode(self.title))
        else:
            title = u''
        if self.description:
            description = description_html % force_unicode(self.description)
        else:
            description = u''
        if top_errors_on_fieldset and top_errors:
            output.insert(0, error_row % force_unicode(top_errors))
        return mark_safe(fieldset_html % {'title': title,
                                          'description': description,
                                          'fields': u'\n'.join(output)})

    def as_table(self):
        "Returns this fieldset's fields rendered as HTML <tr>s -- " \
        "excluding the <table></table>."
        return self._html_output(*self.form._tmpl_table)

    def as_ul(self):
        "Returns this fieldset's fields rendered as HTML <li>s -- " \
        "excluding the <ul></ul>."
        return self._html_output(*self.form._tmpl_ul)

    def as_p(self):
        "Returns this fieldset's fields rendered as HTML <p>s."
        return self._html_output(*self.form._tmpl_p)


class FieldsetMixin(object):
    _tmpl_table = (
        u'<tr><th colspan="2">%(title)s%(description)s</th></tr>%(fields)s',
        u'<h2>%s</h2>',
        u'<div class="description">%s</div>',
        u'<tr><th>%(label)s</th><td>%(errors)s' \
                                          u'%(field)s%(help_text)s</td></tr>',
        u'<tr><td colspan="2">%s</td></tr>',
        u'</td></tr>',
        u'<br />%s',
        False,
    )
    _tmpl_ul = (
        u'<li>%(title)s%(description)s<ul>%(fields)s</ul></li>',
        u'<h2>%s</h2>',
        u'<div class="description">%s</div>',
        u'<li>%(errors)s%(label)s %(field)s%(help_text)s</li>',
        u'<li>%s</li>',
        u'</li>',
        u' %s',
        False,
    )
    _tmpl_p = (
        u'<div>%(title)s%(description)s%(fields)s</div>',
        u'<h2>%s</h2>',
        u'<div class="description">%s</div>',
        u'<p>%(label)s %(field)s%(help_text)s</p>',
        u'%s',
        u'</p>',
        u' %s',
        True,
    )

    def _validate_fieldsets(self):
        valid = False
        fields_defined = sum((fset[1]['fields'] for fset in self.fieldsets),
                             ())
        fields_set = set(fields_defined)
        # Fieldsets are valid if:
        #  * Each field is defined in a Fieldset
        #  * Each field is defined only once.
        if len(fields_defined) == len(fields_set) and \
                                        set(self.fields.keys()) == fields_set:
            valid = True
        return valid

    def validate_fieldsets(self, force=False):
        "Return ``True`` if ``fieldsets`` is defined properly."
        if force or not hasattr(self, '__fieldsets_valid'):
            self.__fieldsets_valid = self._validate_fieldsets()
        if not self.__fieldsets_valid:
            raise FieldsetError('Fieldset definition for %s is invalid. ' \
                                'Each field must be defined in one and ' \
                                'only one Fieldset.' % self.__class__.__name__)
        else:
            return True

    def iter_fieldsets(self):
        "Iterates fieldsets."
        self.validate_fieldsets()
        for title, options in self.fieldsets:
            yield Fieldset(self, title, **options)

    @property
    def fieldset_dict(self):
        # No need to call validate_fieldsets() since we
        # are using iter_fieldsets.
        if not hasattr(self, '__fieldset_dict'):
            self.__fieldset_dict = dict((slugify(fset.title), fset) for \
                                                fset in self.iter_fieldsets())
        return self.__fieldset_dict

    def _html_fieldset_output(self,
                              fieldset_html,
                              title_html,
                              description_html,
                              normal_row,
                              error_row,
                              row_ender,
                              help_text_html,
                              errors_on_separate_row):
        "Helper function for outputting fieldsets as HTML. " \
        "Used by as_fieldset_table(), as_fieldset_ul(), as_fieldset_p()."

        # Errors that should be displayed above all fields.
        top_errors = self.non_field_errors()
        output = []
        for fieldset in self.iter_fieldsets():
            fieldset_output = fieldset._html_output(
                fieldset_html,
                title_html,
                description_html,
                normal_row,
                error_row,
                row_ender,
                help_text_html,
                errors_on_separate_row,
                top_errors,
                error_class=self.error_class,
                label_suffix=self.label_suffix)
            output.append(fieldset_output)
        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))
        return mark_safe(u'\n'.join(output))

    def as_fieldset_table(self):
        "Returns this form's fieldsets rendered as HTML <tr>s -- " \
        "excluding the <table></table>."
        return self._html_fieldset_output(*self._tmpl_table)

    def as_fieldset_ul(self):
        "Returns this form's fieldsets rendered as HTML <li>s -- " \
        "excluding the <ul></ul>."
        return self._html_fieldset_output(*self._tmpl_ul)

    def as_fieldset_p(self):
        "Returns this form's fieldsets rendered as HTML <p>s."
        return self._html_fieldset_output(*self._tmpl_p)
