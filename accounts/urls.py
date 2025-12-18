from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("signup/", views.signup_choose_role, name="signup_choose_role"),
    path("signup/doctor/", views.signup_doctor, name="signup_doctor"),
    path("signup/patient/", views.signup_patient, name="signup_patient"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("complete_medica/<int:user_id>/", views.complete_medica, name="complete_medica"),
    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("chatbot/", views.chatbot, name="chatbot"),
]