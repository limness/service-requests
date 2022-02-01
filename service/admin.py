from django.contrib import admin

# Register your models here.
from .models import User, DiagnosticRequest


admin.site.register(User)
admin.site.register(DiagnosticRequest)
