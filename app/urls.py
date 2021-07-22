from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/worker/', register_worker, name='register_worker'),
    path('register/patient/', register_patient, name='register_patient'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name = 'profile'),
    path('patient/profile/<int:pk>', view_patient, name = 'view_patient_profile'),
    path('patient/encounter/<int:pk>/', encounter_detail, name='encounter_detail'),
    path('dashboard', dashboard, name ='dashboard'),
    path('create-encounter', create_encounter, name = 'create_encounter')

]