from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, DoctorSignupForm, PatientSignupForm, MedicalFormForm, MedicalRecordForm
from .models import PatientProfile, MedicalForm, MedicalRecord
from django.contrib.auth.models import User


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")  # placeholder
    else:
        form = LoginForm(request)
    return render(request, "accounts/login.html", {"form": form})


def signup_choose_role(request):
    return render(request, "accounts/signup_choose_role.html")


def signup_doctor(request):
    if request.method == "POST":
        form = DoctorSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = DoctorSignupForm()
    return render(request, "accounts/signup_doctor.html", {"form": form})


def signup_patient(request):
    if request.method == "POST":
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Redirection vers le formulaire MEDICA juste après la création du compte
            return redirect("complete_medica", user_id=user.id)
    else:
        form = PatientSignupForm()
    return render(request, "accounts/signup_patient.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")


def complete_medica(request, user_id):
    user = get_object_or_404(User, id=user_id)
    patient_profile = user.patientprofile

    # Vérifier si le MEDICA a déjà été rempli
    if hasattr(patient_profile, "medicaform"):
        return redirect("login")  # Si déjà rempli, redirection login

    if request.method == "POST":
        medica_form = MedicalFormForm(request.POST)
        record_form = MedicalRecordForm(request.POST, request.FILES)
        if medica_form.is_valid() and record_form.is_valid():
            medica = medica_form.save(commit=False)
            medica.patient = patient_profile
            medica.save()

            record = record_form.save(commit=False)
            record.patient = patient_profile
            record.save()

            return redirect("login")  # Terminer création et rediriger login
    else:
        medica_form = MedicalFormForm()
        record_form = MedicalRecordForm()

    return render(request, "accounts/complete_medica.html", {
        "medica_form": medica_form,
        "record_form": record_form
    })