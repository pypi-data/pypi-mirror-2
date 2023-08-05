from __future__ import absolute_import

from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class StopamWidget(forms.Widget):
    token_name = u'{0}_token'
    
    # This token will be set by the field when the question
    # is changed. Django doesn't have a mechanism to
    # change the value and the label of a bound field
    token = '' 
    
    def render(self, name, value, attrs=None):
        token_html = forms.HiddenInput().render(
            self.token_name.format(name), 
            self.token, 
            attrs={'id': u'id_{0}_token'.format(name)})
        
        answer_id = attrs['id'] if 'id' in attrs else u'id_{0}'.format(name)
        answer_html = forms.TextInput().render(name=name,
                                               value=None,
                                               attrs={'id': answer_id})
        
        output = [token_html, answer_html]
        
        return mark_safe(u'\n'.join(output))
    
    def value_from_datadict(self, data, files, name):
        token = data.get(self.token_name.format(name))
        answer = data.get(name)
        
        return {'token': token, 'answer': answer}
        

class StopamField(forms.Field):
    default_error_messages = {
        'required': _(u'An answer to the question is required.'),
        'invalid': _(u'The answer doesn\'t seem to be correct.'),
    }
    
    widget = StopamWidget
    
    def __init__(self, service, *args, **kwargs):
        self.service = service
        
        super(StopamField, self).__init__(*args, **kwargs)
        
        self._ask()
        
    def _ask(self):
        """Loads a new question"""
        
        new_question = self.service.ask()
        
        self.label = new_question.question
        
        # This seems to be the only way to replace the value of a
        # bound field
        self.widget.token = new_question.token    
        
    def validate(self, value):
        # Validate the current submission
        token, answer = value.get('token'), value.get('answer')
        
        if not answer:
            raise ValidationError(self.error_messages['required'])
        
        super(StopamField, self).validate(answer)
        
        if not self.service.verify(token, answer):
            raise ValidationError(self.error_messages['invalid'])
        
    def __deepcopy__(self, *args, **kwargs):
        # This is the only method I can hook into to execute
        # code on every form creation
        
        self._ask()
        return super(StopamField, self).__deepcopy__(*args, **kwargs)