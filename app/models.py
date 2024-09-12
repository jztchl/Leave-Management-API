from django.db import models
from django.contrib.auth.models import AbstractUser

class users(AbstractUser):
    ROLE_CHOICES = (
        ('HR', 'HR'),
        ('MANAGER', 'MANAGER'),
        ('EMPLOYEE', 'EMPLOYEE'),
    )
    
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

class leavelist(models.Model):
    employee = models.ForeignKey(users, on_delete=models.CASCADE)
    paidleave = models.IntegerField(default=0)
    unpaidleave = models.IntegerField(default=0)

class leaveRequest(models.Model):
    employee = models.ForeignKey(users, on_delete=models.CASCADE, related_name='employee_leaves')
    AssignedManager = models.ForeignKey(users, on_delete=models.CASCADE, limit_choices_to={'role': 'MANAGER'}, related_name='manager_assigned_leaves')
    reason = models.CharField(max_length=100)
    ManagerApproval = models.BooleanField(default=False)
