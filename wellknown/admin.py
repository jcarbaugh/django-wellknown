from django.contrib import admin
from wellknown.models import Registration

class RegistrationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Registration, RegistrationAdmin)