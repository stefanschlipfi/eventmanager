from django.utils.translation import gettext_lazy as _

class EventUserValidator:
    """
    Validator that check if user_id / event_id is passed
    """
    message = _('This field is required.')
    requires_context = True

    def __init__(self, queryset, message=None, lookup='exact'):
        self.queryset = queryset
        self.message = message or self.message
        self.lookup = lookup

    
    def __call__(self, value, serializer_field):
        # Determine the underlying model field name. This may not be the
        # same as the serializer field name if `source=<>` is set.
        field_name = serializer_field.source_attrs[-1]
        # Determine the existing instance, if this is an update operation.
        instance = getattr(serializer_field.parent, 'instance', None)

        queryset = self.queryset
        print('field_name: {}'.format(field_name))
        print('value: {}'.format(value))
        
        #queryset = self.filter_queryset(value, queryset, field_name)
        #queryset = self.exclude_current_instance(queryset, instance)
        #if qs_exists(queryset):
        #    raise ValidationError(self.message, code='unique')

    #def __repr__(self):
    #    return '<%s(queryset=%s)>' % (
    #        self.__class__.__name__,
    #        smart_repr(self.queryset)
    #    )

