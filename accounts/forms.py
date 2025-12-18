from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import DoctorProfile, PatientProfile,MedicalForm, MedicalRecord


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class DoctorSignupForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = DoctorProfile
        fields = [
            "phone",
            "specialization",
            "experience_years",
            "license_number",
            "clinic_name",
            "clinic_address",
            "working_hours",
        ]

    def save(self, commit=True):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = self.data.get("full_name", "")
        if commit:
            user.save()
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return user


class PatientSignupForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = PatientProfile
        fields = ["phone", "date_of_birth", "gender", "city", "country"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm_password"):
            self.add_error("confirm_password", "Passwords do not match")
        return cleaned

    def save(self, commit=True):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = self.data.get("full_name", "")
        if commit:
            user.save()
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return user
    
# Listes possibles
CHRONIC_DISEASES_CHOICES = [
    ("Diabetes", "Diabetes"),
    ("Hypertension", "Hypertension"),
    ("Asthma", "Asthma"),
    ("Heart Disease", "Heart Disease"),
    ("Cancer", "Cancer"),
    ("Kidney Disease", "Kidney Disease"),
    ("Liver Disease", "Liver Disease"),
    ("Other", "Other"),
]

VACCINES_CHOICES = [
    ("BCG", "BCG"),
    ("Hepatitis B", "Hepatitis B"),
    ("Polio", "Polio"),
    ("MMR", "Measles, Mumps, Rubella"),
    ("Tetanus", "Tetanus"),
    ("Influenza", "Influenza"),
    ("COVID-19", "COVID-19"),
]

FAMILY_HISTORY_CHOICES = [
    ("Diabetes", "Diabetes"),
    ("Hypertension", "Hypertension"),
    ("Cancer", "Cancer"),
    ("Heart Disease", "Heart Disease"),
    ("Other", "Other"),
]
    
class MedicalFormForm(forms.ModelForm):
    chronic_diseases_yes_no = forms.ChoiceField(
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect,
        label="Do you have chronic diseases?"
    )
    chronic_diseases = forms.MultipleChoiceField(
        choices=CHRONIC_DISEASES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select your chronic diseases"
    )
    chronic_diseases_other = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":2}), label="Other chronic diseases")

    allergies_yes_no = forms.ChoiceField(
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect,
        label="Do you have allergies?"
    )
    allergies = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":2}), label="Specify your allergies")

    vaccines_done = forms.MultipleChoiceField(
        choices=VACCINES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Vaccines received"
    )
    vaccines_other = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":2}), label="Other vaccines")

    family_history_yes_no = forms.ChoiceField(
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect,
        label="Do you have a family history of diseases?"
    )
    family_history = forms.MultipleChoiceField(
        choices=FAMILY_HISTORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select family history"
    )
    family_history_other = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":2}), label="Other family history")

    class Meta:
        model = MedicalForm
        fields = [
            "chronic_diseases_yes_no", "chronic_diseases", "chronic_diseases_other",
            "allergies_yes_no", "allergies",
            "vaccines_done", "vaccines_other",
            "family_history_yes_no", "family_history", "family_history_other",
        ]

    def clean(self):
        cleaned = super().clean()

        # Si "oui" pour maladies chroniques, vérifier qu'il y a au moins un choix ou texte libre
        if cleaned.get("chronic_diseases_yes_no") == "yes":
            if not cleaned.get("chronic_diseases") and not cleaned.get("chronic_diseases_other"):
                self.add_error("chronic_diseases", "Please select or specify at least one chronic disease.")

        # Même logique pour allergies
        if cleaned.get("allergies_yes_no") == "yes":
            if not cleaned.get("allergies"):
                self.add_error("allergies", "Please specify your allergies.")

        # Même logique pour family history
        if cleaned.get("family_history_yes_no") == "yes":
            if not cleaned.get("family_history") and not cleaned.get("family_history_other"):
                self.add_error("family_history", "Please select or specify family history.")

        return cleaned

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ["file"]