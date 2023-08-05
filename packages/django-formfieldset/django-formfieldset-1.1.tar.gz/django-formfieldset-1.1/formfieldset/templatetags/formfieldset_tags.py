from django import template
from django.conf import settings


register = template.Library()


DEFAULT_FORM_TEMPLATE = getattr(settings,
                                'FORMFIELDSET_DEFAULT_FORM_TEMPLATE',
                                'formfieldset/form.html')


@register.filter
def renderform(form, template_name=None):
    """Render form.

       If optional argument ``template_name`` is given that template will be
       used for rendering. Otherwise ``formfieldset/form.html`` will be used.
    """
    tmpl = template.loader.get_template(template_name or DEFAULT_FORM_TEMPLATE)
    return tmpl.render(template.Context({'form': form}))
