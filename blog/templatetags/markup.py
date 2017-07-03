import markdown
from django import template
from django.conf import settings
from django.utils.encoding import force_text, force_unicode
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def my_markdown(value):
    return mark_safe(markdown.markdown(value,
                                       tab_length=2,
                                       extensions=['markdown.extensions.fenced_code'],
                                       safe_mode=False,
                                       enable_attributes=False))
