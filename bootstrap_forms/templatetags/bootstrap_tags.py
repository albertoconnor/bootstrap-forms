from django import template
from django.template import Template, Context


register = template.Library()

default_field_template = '''<div class="form-group">
  <label for="{{ field.html_name }}" class="control-label{% if field.field.required %} required{% endif %}">{{ field.label }}</label>
  <div class="controls{% if field.field.widget.inline %} form-inline{% endif %}">
    {{ field }}
    {% if field.errors %}
    <div class="field_errors">
          {{ field.errors }}
    </div>
    {% endif %}
    {% if field.help_text %}
    <span class="help-block">{{ field.help_text }}</span>
    {% endif %}
  </div>
</div>
'''

@register.filter(is_safe=True)
def as_bootstrap(field):
    template = Template(default_field_template)
    ctx = Context(dict(field=field))
    return template.render(ctx)
