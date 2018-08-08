import types

from django import forms
from django.template import Template, Context


default_template = u'''
{% if form.non_field_errors %}
<div class="form_errors">
{% for error in form.non_field_errors %}
<div class="error">{{ error }}</div>
{% endfor %}
</div>
{% endif %}
{% for field in form.visible_fields %}
<div class="form-group">
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
{% endfor %}
{% for field in form.hidden_fields %}
{{ field }}
{% endfor %}
'''

default_field_template = u'''<div class="form-group">
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


def as_bootstrap(self):
    template = Template(default_field_template)
    ctx = Context(dict(field=self))
    return template.render(ctx)


# Mixin
class BootstrapForm(object):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for bfield in self:
            # Bind a helper method to each field to render as bootstrap
            bfield.as_bootstrap = types.MethodType(as_bootstrap, bfield)

            field = self.fields[bfield.name]
            to_continue = False
            for widget_class in (forms.CheckboxSelectMultiple, forms.CheckboxInput):
                if isinstance(field.widget, widget_class):
                    to_continue = True
                    break
            if to_continue:
                continue

            classes = ['form-control']
            if 'class' in field.widget.attrs:
                classes.append(field.widget.attrs['class'])
            field.widget.attrs.update(
                {'class': ' '.join(classes)}
            )

    def as_bootstrap(self):
        template = Template(default_template)
        ctx = Context(dict(form=self))
        return template.render(ctx)
