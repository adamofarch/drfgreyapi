from django.urls import path
from . import views

urlpatterns = [
    path('doctors/', views.ListDoctors.as_view()),
    path('doctors/<int:pk>', views.doctor_details),
    path('patients/', views.ListPatients.as_view()),
    path('login/', views.user_login),
    path('register/', views.user_signup),
    path('patient_records/', views.ListPatientRecords.as_view()),
    

]
