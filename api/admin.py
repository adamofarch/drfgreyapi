from django.contrib import admin
from .models import Patient_Record, Department, User, Doctor, Patient

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Patient_Record)
admin.site.register(Department)

