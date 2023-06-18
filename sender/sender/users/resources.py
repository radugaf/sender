from import_export import resources

from .models import Contacts


class ContactsResource(resources.ModelResource):
    class Meta:
        model = Contacts
