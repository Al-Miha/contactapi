from django.contrib import admin
from .models import Contact

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    # Display these fields in the list view in the admin interface
    list_display = ['company_name', 'email', 'markets', 'message']

    # Allow filtering by these fields
    list_filter = ['markets']

    # Allow searching by these fields
    search_fields = ['company_name', 'email', 'markets', 'message']

    # Specify which fields should be shown on the form for adding/editing a contact
    fields = ['company_name', 'email', 'markets', 'message']

    # Optionally, you can add ordering to the list view
    ordering = ['company_name']

admin.site.register(Contact,ContactAdmin)