from django.db import models
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.db.models.fields import DateField
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class MedUser(AbstractUser):
  USER_TYPE_CHOICES = (
      (1, 'worker'),
      (2, 'patient'),

  )

  user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True)








class Encounter(models.Model):

    visit = (
        ('First Time Visit', 'First Time Visit'),
        ('First Time Visit', 'Repeat Visit')

    )

    diagnosis = (
        ('Hypertension', 'Hypertension'),
        ('Diabetes', 'Diabetes'),
        ('Pneumonia', 'Pneumonia'),
        ('Malaria', 'Malaria')
    )

    patient = models.ForeignKey(MedUser, on_delete=models.CASCADE, related_name='record_encounter')
    worker = models.ForeignKey(MedUser, on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    time = models.TimeField()
    visit = models.CharField(max_length=30, choices=visit)
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    height = models.DecimalField(max_digits=4, decimal_places=1)
    bp = models.DecimalField(max_digits=4, decimal_places=1)
    temp = models.DecimalField(max_digits=4, decimal_places=1)
    rr = models.DecimalField(max_digits=4, decimal_places=1)
    complaints = models.TextField()
    diagnosis = models.CharField(max_length=50, choices=diagnosis)
    treatment_plan = models.TextField()


    # method to automatically calculate BMI
    def bmi(self):
        return round((float(self.weight)/float(self.height)), 1)


# model for health worker
class Worker(models.Model):
    gender = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female')
    )

    worker = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    name = models.CharField(max_length=20, blank=False)
    surname = models.CharField(max_length=20, blank=False)
    age = models.IntegerField()
    gender  = models.CharField(max_length=10, choices=gender)
    cadre = models.CharField(max_length=20)
    dept = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.surname


# model for patient/record
class Patient(models.Model):

    gender = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female')
    )

    patient = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient')
    worker = models.ForeignKey(MedUser, on_delete=models.CASCADE, related_name='patients')
    name = models.CharField(max_length=30, blank=False)
    surname = models.CharField(max_length=30, blank=False)
    age = models.IntegerField()
    gender = models.CharField(max_length=15, choices=gender)
    height = models.DecimalField(max_digits=4, decimal_places=1)
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    ward = models.CharField(max_length=50)
    lga = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='images/')
    

    def __str__(self):
        return self.patient.username

    # method to automatically calculate BMI
    def bmi(self):
        return round((float(self.weight)/float(self.height)), 1)