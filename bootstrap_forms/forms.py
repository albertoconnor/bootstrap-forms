from django import forms
from django.template import Template, Context
from django.utils.html import format_html, format_html_join
from django.utils.encoding import force_text, python_2_unicode_compatible


default_template = '''
{% if form.non_field_errors %}
<div class="form_errors">
{% for error in form.non_field_errors %}
<div class="error">{{ error }}</div>
{% endfor %}
{% endif %}
{% for field in form.visible_fields %}
<div class="form-group">
  <label for="{{ field.html_name }}" class="control-label{% if field.field.required %} required{% endif %}">{{ field.label }}</label>
  <div class="controls">
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

# Mixin
class BootstrapForm(object):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            field = self.fields[field]
           
            to_continue = False
            for widget_class in (forms.CheckboxSelectMultiple, forms.CheckboxInput):
                if isinstance(field.widget, widget_class):
                    to_continue = True
                    break
            if to_continue: continue

            classes = ['form-control']
            if 'class' in field.widget.attrs:
                classes.append(field.widget.attrs['class'])
            field.widget.attrs.update(
                {'class' : ' '.join(classes)}
            )

    def as_bootstrap(self):
        template = Template(default_template)
        ctx = Context(dict(form=self))
        return template.render(ctx)

class BootstrapRadioInput(forms.widgets.RadioInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if 'id' in self.attrs:
            label_for = format_html(' for="{0}_{1}"', self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = force_text(self.choice_label)
        return format_html(
            '<label{0} class="radio inline">{1} {2}</label>', 
            label_for,
            self.tag(),
            self.choice_label
        )


@python_2_unicode_compatible
class BootStrapRadioRenderer(forms.widgets.RadioFieldRenderer):
    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield BootstrapRadioInput(self.name, self.value, self.attrs.copy(), choice, i)

    def render(self):
        return format_html(
            '{0}',
            format_html_join('\n', '{0}', [(force_text(w),) for w in self])
        )
        
    def __str__(self):
        return b''


class BootStrapRadioSelect(forms.RadioSelect):
    renderer = BootStrapRadioRenderer
