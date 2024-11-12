from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# frAom django.db.models.signals import post_save
# from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        DOCTOR = "DOCTOR", 'Doctor'
        PATIENT = "PATIENT", 'Patient'

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)
    
    def save(self, *args, **kwargs):
        if not self.role:
            self.role = self.base_role
        return super().save(*args, **kwargs)

class DoctorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.DOCTOR)

class Doctor(User):
    base_role = User.Role.DOCTOR
    
    doctor = DoctorManager()
    
    class Meta:
        proxy = True

class PatientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.PATIENT)

class Patient(User):
    base_role = User.Role.PATIENT

    patient = PatientManager()
    class Meta:
        proxy = True

class Department(models.Model):
    name = models.CharField(max_length=50, blank=False)
    diagnostics = models.TextField(max_length=500)
    location = models.CharField(max_length=200)
    specialization = models.CharField(max_length=100,blank=False)
    # groups = models.ManyToManyField(Group, related_name="departments")

    def __str__(self):
        return self.name

class Patient_Record(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    diagnostics = models.TextField(max_length=1000)
    observations = models.TextField(max_length=300)
    treatments = models.TextField(max_length=300)
    department_id = models.ForeignKey(Department, on_delete=models.PROTECT)
    misc = models.TextField(max_length=500) 

    def __str__(self):
        return str(self.patient_id)

# @receiver(post_save, sender=Doctor)
# def add_doctor_to_the_group(sender, instance, created, **kwargs):
#     if created:
#         doctors_group, created = Group.objects.get(name="Doctors")
#         instance.user.groups.add(doctors_group)
#
# @receiver(post_save, sender=Patient)
# def add_patient_to_the_group(sender, instance, created, **kwargs):
#     if created:
#         patients_group, created = Group.objects.get(name="Patients")
#         instance.user.groups.add(patients_group)
