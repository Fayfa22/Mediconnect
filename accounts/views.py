import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, DoctorSignupForm, PatientSignupForm, MedicalFormForm, MedicalRecordForm
from .models import PatientProfile, MedicalForm, MedicalRecord
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


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
    if hasattr(request.user, "patientprofile"):
        return redirect("patient_dashboard")
    if hasattr(request.user, "doctorprofile"):
        return redirect("doctor_dashboard")


def complete_medica(request, user_id):
    user = get_object_or_404(User, id=user_id)
    patient_profile = user.patientprofile

    # Vérifier si le MEDICA a déjà été rempli
    try:
        patient_profile.medicaform
        return redirect("login")
    except ObjectDoesNotExist:
        pass  # Si déjà rempli, redirection login

    if request.method == "POST":
        medica_form = MedicalFormForm(request.POST)
        record_form = MedicalRecordForm(request.POST, request.FILES)

        if medica_form.is_valid() and record_form.is_valid():
            medica = medica_form.save(commit=False)

             # CONVERSION YES / NO → BOOLEAN (LA PARTIE MANQUANTE)
            cleaned = medica_form.cleaned_data
            medica.chronic_diseases_yes_no = cleaned["chronic_diseases_yes_no"] == "yes"
            medica.allergies_yes_no = cleaned["allergies_yes_no"] == "yes"
            medica.family_history_yes_no = cleaned["family_history_yes_no"] == "yes"

            # Attacher le patient
            medica.patient = patient_profile
            medica.save()

            # Medical record
            record = record_form.save(commit=False)
            record.patient = patient_profile
            record.save()


            login(request, user)
            return redirect("dashboard")
  # Terminer création et rediriger login
    else:
        medica_form = MedicalFormForm()
        record_form = MedicalRecordForm()

    return render(request, "accounts/complete_medica.html", {
        "medica_form": medica_form,
        "record_form": record_form
    })

@login_required
def patient_dashboard(request):
    patient_profile = get_object_or_404(PatientProfile, user=request.user)

    return render(request, "accounts/patient_profile.html", {
        "patient_profile": patient_profile
    })

@login_required
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        message = data.get("message", "").strip()

        if not message:
            return JsonResponse({"reply": "Please type a message."})

        reply = generate_bot_reply(message)
        return JsonResponse({"reply": reply})

    except Exception:
        return JsonResponse(
            {"reply": "Server error. Please try again."},
            status=500
        )


def generate_bot_reply(message):
    message = message.lower()

    if "appointment" in message:
        return "You can check your appointments in the Appointments section."
    if "doctor" in message:
        return "You can browse doctors from the Doctors section."
    if "prescription" in message:
        return "Your prescriptions are available in your medical records."
    if "hello" in message or "hi" in message:
        return "Hello! How can I help you today?"

    return "I'm here to help. Please be more specific."