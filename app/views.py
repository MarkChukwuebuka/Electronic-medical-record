from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from .forms import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.base_user import BaseUserManager
from .decorators import *
from .models import *
from django.contrib import messages
from .serializers import *
from rest_framework import generics


# Create your views here.

#home page
def home(request):
    return render(request, "index.html")


# login view for both patients and workers
def login(request):
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            u = login_form.cleaned_data['username']
            p = login_form.cleaned_data['password']
            user = authenticate(username=u, password=p)

            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                login_form.add_error(None, "Login information is wrong or your account is not active.")
    else:
        login_form = UserLoginForm()

    context = {'form': login_form}

    return render(request, 'login.html', context)



# worker registration view
def register_worker(request):
    if request.method == "POST":
        user_form = UserRegistrationForm1(request.POST)
        worker_form = WorkerRegistrationForm(request.POST)

        if user_form.is_valid() and worker_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 1
            user.is_active = True
            user.save()
            worker = worker_form.save(commit=False)
            worker.worker = user
            worker.name = user.first_name
            worker.surname = user.last_name 
            worker.save()

            u = user_form.cleaned_data['username']
            p = user_form.cleaned_data['password1']
            user = authenticate(username=u, password=p)

            if user is not None:
                messages.success(request, "Your registration was successful")
                auth.login(request, user)
                return redirect("/")
            
    else:
        user_form = UserRegistrationForm1()
        worker_form = WorkerRegistrationForm()

    context = {'user_form': user_form, 'user_type_form': worker_form}

    return render(request, "register.html", context)



# patient registration view 
@worker_login_required
def register_patient(request):
    if request.method == "POST":
        user_form = UserRegistrationForm2(request.POST)
        patient_form = PatientRegistrationForm(request.POST, request.FILES)

        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 2
            usrn = user.first_name[0] + user.last_name
            i=1
            while MedUser.objects.filter(username=usrn).exists():
                usrn = user.first_name[0] + user.last_name
                usrn = usrn + str(i)
                i = i+1
            user.username = usrn
            pwd = BaseUserManager().make_random_password()
            user.set_password(pwd)
            user.save()
            patient = patient_form.save(commit=False)
            patient.patient = user
            patient.worker = MedUser.objects.get(username = request.user)
            patient.name = user.first_name
            patient.surname = user.last_name
            patient.age = patient.age
            patient.gender = patient.gender
            patient.height = patient.height
            patient.weight = patient.weight
            patient.ward = patient.ward
            patient.lga = patient.lga
            patient.state = patient.state
            patient.picture = patient.picture
            patient.save()

            messages.success(request, "Patient registered with username = {} with random password = {}"
                                .format(user.username,pwd))
            
            return redirect("/")

    else:
        user_form = UserRegistrationForm2()
        patient_form = PatientRegistrationForm()

    context = {'user_form': user_form, 'user_type_form': patient_form}

    return render(request, "register.html", context)



# logout view 
def logout(request):
    auth.logout(request)
    return redirect('/')




# patient profile page after patient logs in
@login_required(login_url="/login")
def profile(request):
    context = {
        'patient':Patient.objects.get(patient=request.user)
    }

    return render(request, "profile.html", context)

@worker_login_required
def view_patient(request, pk):

    context = {
        'patient': get_object_or_404(Patient, pk=pk)
    }

    return render(request, 'profile.html', context)

# create encounter for patient
@worker_login_required
def create_encounter(request):

    if request.method == 'POST':
        encounter_form = EncounterCreationForm(request.POST)

        if encounter_form.is_valid():
            encounter = encounter_form.save(commit=False)
            pat = MedUser.objects.get(username=encounter_form.cleaned_data['patient_username'])
            encounter.patient = pat
            encounter.date = encounter.date
            encounter.time = encounter.time
            encounter.visit = encounter.visit
            encounter.weight = encounter.weight
            encounter.height = encounter.height
            encounter.bp = encounter.bp
            encounter.temp = encounter.bp
            encounter.rr = encounter.rr
            encounter.complaints = encounter.complaints
            encounter.diagnosis = encounter.diagnosis
            encounter.treatment_plan = encounter.treatment_plan
            encounter.worker = MedUser.objects.get(username=request.user)
            encounter.save()
            
            return redirect("/patient/encounter/{id}".format(id=encounter.id))
    else:
        encounter_form = EncounterCreationForm(request.POST)

    context = {'encounter_form': encounter_form}

    return render(request, "create_encounter.html", context)


# page to display details of an encounter
@worker_login_required
def encounter_detail(request, pk):

    context = {
        'encounter' : Encounter.objects.get(id=pk)
    }

    return render(request, 'encounter-detail.html', context)


# worker's dashboard for analysis
@worker_login_required
def dashboard(request):

    context = {
        'patients' : Patient.objects.all()
    }

    return render(request, 'dashboard.html', context)

class PatientListView(generics.ListAPIView):
    queryset = Patient.objects.all()
    # queryset = queryset.order_by('-id')
    serializer_class = PatientSerializer