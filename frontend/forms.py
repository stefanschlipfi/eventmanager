from django import forms
from backend.models import EventUser

class EventUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]
                #remove label for as_p
                field.label = ''
    
    class Meta:
        model = EventUser
        fields = ['action']