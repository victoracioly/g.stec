from django import template
register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    existing_attrs = field.field.widget.attrs.copy()
    existing_class = existing_attrs.get('class', '')
    combined_class = f"{existing_class} {css_class}".strip()
    return field.as_widget(attrs={**existing_attrs, 'class': combined_class})

@register.filter(name='attr')
def attr(field, arg):
    try:
        key, val = arg.split(':', 1)
        existing_attrs = field.field.widget.attrs.copy()
        existing_attrs[key] = val
        return field.as_widget(attrs=existing_attrs)
    except:
        return field