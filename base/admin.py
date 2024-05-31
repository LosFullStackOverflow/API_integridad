from django.contrib import admin

# Register your models here.
from .models import Cliente, Estado

admin.site.register(Cliente)
admin.site.register(Estado)
