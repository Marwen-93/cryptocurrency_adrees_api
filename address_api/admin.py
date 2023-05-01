from django.contrib import admin
from .models import ValidAddress

class ValidAddressAdmin(admin.ModelAdmin):
    list_display = ['currency','address','public_key']

admin.site.register(ValidAddress, ValidAddressAdmin)