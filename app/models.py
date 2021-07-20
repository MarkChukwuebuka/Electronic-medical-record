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


visit = (
    ('FTV' , 'First Time Visit'),
    ('RV', 'Repeat Visit')

)

diagnosis = (
    ('ht', 'Hypertension'),
    ('db', 'Diabetes'),
    ('pm', 'Pneumonia'),
    ('ml', 'Malaria')
)

gender = (
    ('M', 'Male'),
    ('F', 'Female')
)

class Encounter(models.Model):
    patient = models.ForeignKey(MedUser, on_delete=models.CASCADE, related_name='record_encounter')
    worker = models.ForeignKey(MedUser, on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    time = models.TimeField()
    visit = models.CharField(max_length=30, choices=visit)
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    height = models.DecimalField(max_digits=4, decimal_places=2)
    bp = models.DecimalField(max_digits=4, decimal_places=2)
    temp = models.DecimalField(max_digits=4, decimal_places=2)
    rr = models.DecimalField(max_digits=4, decimal_places=2)
    complaints = models.TextField()
    diagnosis = models.CharField(max_length=50, choices=diagnosis)
    treatment_plan = models.TextField()

    def bmi(self):
        return float(self.weight)/float(self.height)


# model for health worker
class Worker(models.Model):
    worker = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    name = models.CharField(max_length=20, blank=False)
    surname = models.CharField(max_length=20, blank=False)
    age = models.IntegerField()
    gender  = models.CharField(max_length=10, choices=gender)
    cadre = models.CharField(max_length=20)
    dept = models.CharField(max_length=20, blank=False)



# model for patient/record
class Patient(models.Model):
    patient = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient')
    worker = models.ForeignKey(MedUser, on_delete=models.CASCADE, related_name='patients')
    age = models.IntegerField()
    gender = models.CharField(max_length=15, choices=gender)
    height = models.DecimalField(max_digits=4, decimal_places=2)
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    ward = models.CharField(max_length=50)
    lga = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='images/')
    

    def __str__(self):
        return self.user.username


    def bmi(self):
        return float(self.weight)/float(self.height)