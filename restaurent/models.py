from django.db import models
from django.contrib.auth.models import User

class Table(models.Model):
    table_number = models.IntegerField()
    capacity = models.IntegerField()

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    time_slot = models.TimeField()
    guests = models.IntegerField()
