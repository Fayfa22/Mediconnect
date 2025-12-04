from django.conf import settings
from django.db import models


class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    specialization = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    license_number = models.CharField(max_length=100)
    clinic_name = models.CharField(max_length=255)
    clinic_address = models.TextField()
    working_hours = models.CharField(max_length=255)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"


class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[("M", "Male"), ("F", "Female")])
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name()
    
class MedicalRecord(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="medical_records")
    file = models.FileField(upload_to="medical_records/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class MedicalForm(models.Model):
    patient = models.OneToOneField('PatientProfile', on_delete=models.CASCADE)

    # Maladies chroniques
    chronic_diseases_yes_no = models.BooleanField(default=False)
    chronic_diseases = models.JSONField(blank=True, null=True)  # Stocke la liste des maladies
    chronic_diseases_other = models.TextField(blank=True)

    # Allergies
    allergies_yes_no = models.BooleanField(default=False)
    allergies = models.TextField(blank=True)

    # Vaccins
    vaccines_done = models.JSONField(blank=True, null=True)  # Liste des vaccins
    vaccines_other = models.TextField(blank=True)

    # Historique familial
    family_history_yes_no = models.BooleanField(default=False)
    family_history = models.JSONField(blank=True, null=True)
    family_history_other = models.TextField(blank=True)

    def __str__(self):
        return f"MEDICA for {self.patient.user.get_full_name()}"